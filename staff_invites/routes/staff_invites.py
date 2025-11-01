"""
core/routes/invite.py
---------------------
Handles invite-only user registration links using core_invites table.
"""

from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel, EmailStr
from datetime import datetime
from werkzeug.security import generate_password_hash
from core.utils.auth_utils import require_roles
from core.utils.utils_staff_invites import create_invite_token, decode_invite_token
from core.models.role import Role
from core.models.model_staff_invites import Invites
from core.utils.smtp_utils import send_email
from core.models.user import User
from core.db import SessionLocal
import os


router = APIRouter(prefix="/api/staff_invites", tags=["Invitations"])
MY_DOMAIN = os.getenv("MY_DOMAIN")


class InviteRequest(BaseModel):
    email: EmailStr
    role: str

class AcceptInviteRequest(BaseModel):
    token: str
    password: str

@router.post("/create", dependencies=[Depends(require_roles("superadmin","admin", "manager"))])
def create_invite(data: InviteRequest):
    """
    Create an invitation link for a new staff member and store it in core_invites.
    """
    db = SessionLocal()
    role = db.query(Role).filter_by(name=data.role).first()
    if not role:
        db.close()
        raise HTTPException(status_code=400, detail=f"Role '{data.role}' does not exist")

    # Check if there's an existing unexpired invite
    existing = db.query(Invites).filter_by(email=data.email, role_id=role.id, accepted=False).first()
    if existing and not existing.is_expired():
        db.close()
        raise HTTPException(status_code=400, detail="An active invite already exists for this email and role")

    # Create and store invite
    token = create_invite_token(data.email, data.role)
    invite = Invites(email=data.email, role_id=role.id, token=token)
    db.add(invite)
    db.commit()
    db.refresh(invite)
    db.close()

    invite_link = f"{MY_DOMAIN}/staff_invites/accept_page?token={token}"
    email_body = f"""
        <h3>You’ve been invited to join ByteSmile</h3>
        <p>You’ve been invited to register as a <b>{data.role}</b>.</p>
        <p>Click the button below to complete your registration:</p>
        <a href="{invite_link}" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007BFF;
            text-decoration: none;
            border-radius: 5px;
        ">Complete Registration</a>
        <p>This link expires on <b>{invite.expires_at.strftime('%Y-%m-%d %H:%M:%S')}</b>.</p>
    """

    send_email(data.email, "ByteSmile Invitation", email_body)
    # TODO: Send invite email here using your email service
    return {
        "message": "Invites created successfully",
        "invite_link": invite_link,
        "expires_at": invite.expires_at.isoformat()
    }


@router.get("/verify")
def verify_invite(token: str):
    """
    Verify if an invite token is valid and not expired.
    """
    db = SessionLocal()
    data = decode_invite_token(token)
    if not data:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid or expired invite token")

    invite = db.query(Invites).filter_by(token=token).first()
    if not invite:
        db.close()
        raise HTTPException(status_code=404, detail="Invites not found")

    if invite.is_expired():
        db.close()
        raise HTTPException(status_code=400, detail="Invites expired")

    db.close()
    return {"valid": True, "email": data["email"], "role": data["role"]}


@router.post("/accept")
def accept_invite_api(token: str = Form(...), password: str = Form(...)):
    """
    Accept an invite, register a new user, and mark the invite as accepted.
    Compatible with upgraded User model.
    """
    db = SessionLocal()
    try:
        data_decoded = decode_invite_token(token)
        if not data_decoded:
            raise HTTPException(status_code=400, detail="Invalid or expired invite token")

        invite = db.query(Invites).filter_by(token=token).first()
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")

        if invite.is_expired():
            raise HTTPException(status_code=400, detail="Invite expired")

        if invite.accepted:
            raise HTTPException(status_code=400, detail="Invite already used")

        role = db.query(Role).filter_by(id=invite.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role")

        # Prevent duplicates by email or username
        existing_user = db.query(User).filter(
            (User.username == invite.email) | (User.email == invite.email)
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # ✅ Capture invite data before closing session
        user_email = invite.email
        username = user_email.split("@")[0]
        role_name = role.name

        # Create the new staff user
        new_user = User(
            username=username,
            email=user_email,
            full_name=username.title(),
            password_hash=generate_password_hash(password),
            role_id=invite.role_id,
            position_title=role_name.title(),
            department="Clinic",
            is_active=True,
            created_at=datetime.utcnow(),
        )

        invite.accepted = True
        db.add(new_user)
        db.commit()

        return {
            "message": f"✅ Invite accepted. User '{username}' created successfully as '{role_name}'."
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error during invite acceptance: {e}")
    finally:
        db.close()


@router.get("/list")
def list_invites():
    db = SessionLocal()
    # Join roles to get their names
    staff_invites = db.query(Invites, Role.name.label("role_name")).join(Role, Invites.role_id == Role.id).all()

    data = []
    for invite, role_name in staff_invites:
        data.append({
            "email": invite.email,
            "role": role_name,
            "created_at": invite.created_at.strftime("%Y-%m-%d %H:%M"),
            "expires_at": invite.expires_at.strftime("%Y-%m-%d %H:%M"),
            "accepted": invite.accepted,
            "expired": invite.is_expired(),
            "token": invite.token
        })
    db.close()
    return data

@router.delete("/revoke")
def revoke_invite(token: str):
    db = SessionLocal()
    invite = db.query(Invites).filter_by(token=token).first()
    if not invite:
        db.close()
        raise HTTPException(status_code=404, detail="Invites not found")
    db.delete(invite)
    db.commit()
    db.close()
    return {"message": "Invites revoked successfully"}


@router.get("/roles")
def get_roles():
    """Return all available roles for invites dropdown."""
    db = SessionLocal()
    roles = db.query(Role).order_by(Role.name.asc()).all()
    data = [{"id": r.id, "name": r.name} for r in roles]
    db.close()
    return data