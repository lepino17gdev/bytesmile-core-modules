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
from core.utils.utils_invites import create_invite_token, decode_invite_token
from core.models.role import Role
from core.models.model_invites import Invites
from core.utils.smtp_utils import send_email
from core.models.user import User
from core.db import SessionLocal
import os


router = APIRouter(prefix="/api/invite", tags=["Invitations"])
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
    existing = db.query(Invite).filter_by(email=data.email, role_id=role.id, accepted=False).first()
    if existing and not existing.is_expired():
        db.close()
        raise HTTPException(status_code=400, detail="An active invite already exists for this email and role")

    # Create and store invite
    token = create_invite_token(data.email, data.role)
    invite = Invite(email=data.email, role_id=role.id, token=token)
    db.add(invite)
    db.commit()
    db.refresh(invite)
    db.close()

    invite_link = f"{MY_DOMAIN}/invite/accept_page?token={token}"
    email_body = f"""
    <h3>You’ve been invited to join ByteSmile</h3>
    <p>You’ve been invited to register as a <b>{data.role}</b>.</p>
    <p>Click the link below to complete your registration:</p>
    <a href="{invite_link}">{invite_link}</a>
    <p>This link expires on <b>{invite.expires_at.strftime('%Y-%m-%d %H:%M:%S')}</b>.</p>
    """
    send_email(data.email, "ByteSmile Invitation", email_body)
    # TODO: Send invite email here using your email service
    return {
        "message": "Invite created successfully",
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

    invite = db.query(Invite).filter_by(token=token).first()
    if not invite:
        db.close()
        raise HTTPException(status_code=404, detail="Invite not found")

    if invite.is_expired():
        db.close()
        raise HTTPException(status_code=400, detail="Invite expired")

    db.close()
    return {"valid": True, "email": data["email"], "role": data["role"]}


@router.post("/accept")
def accept_invite_api(token: str = Form(...), password: str = Form(...)):
    """
    Accept invite, register new user, and mark invite as accepted.
    """
    db = SessionLocal()
    data_decoded = decode_invite_token(token)
    if not data_decoded:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid or expired invite token")

    invite = db.query(Invite).filter_by(token=token).first()
    if not invite:
        db.close()
        raise HTTPException(status_code=404, detail="Invite not found")

    if invite.is_expired():
        db.close()
        raise HTTPException(status_code=400, detail="Invite expired")

    if invite.accepted:
        db.close()
        raise HTTPException(status_code=400, detail="Invite already used")

    role = db.query(Role).filter_by(id=invite.role_id).first()
    if not role:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid role")

    if db.query(User).filter_by(username=invite.email).first():
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")

    # ✅ Capture these before closing the session
    user_email = invite.email
    role_name = role.name

    # Create the new user
    new_user = User(
        username=user_email,
        password_hash=generate_password_hash(password),
        role_id=invite.role_id
    )
    invite.accepted = True
    db.add(new_user)
    db.commit()
    db.close()

    return {"message": f"Invite accepted, user '{user_email}' created successfully as '{role_name}'"}


@router.get("/list")
def list_invites():
    db = SessionLocal()
    invites = db.query(Invite).all()
    data = []
    for i in invites:
        data.append({
            "email": i.email,
            "role": i.role.name if i.role else None,
            "created_at": i.created_at.strftime("%Y-%m-%d %H:%M"),
            "expires_at": i.expires_at.strftime("%Y-%m-%d %H:%M"),
            "accepted": i.accepted,
            "expired": i.is_expired(),
            "token": i.token
        })
    db.close()
    return data

@router.delete("/revoke")
def revoke_invite(token: str):
    db = SessionLocal()
    invite = db.query(Invite).filter_by(token=token).first()
    if not invite:
        db.close()
        raise HTTPException(status_code=404, detail="Invite not found")
    db.delete(invite)
    db.commit()
    db.close()
    return {"message": "Invite revoked successfully"}

