# page_routes/page_invite.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core.utils.auth_utils import require_roles, get_current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["Pages"])

@router.get("/invite/accept", response_class=HTMLResponse)
def invite_accept_page(request: Request):
    return templates.TemplateResponse("invite_accept.html", {"request": request})

@router.get("/invites", response_class=HTMLResponse, dependencies=[Depends(require_roles("superadmin", "admin", "manager"))])
async def invites_page(request: Request, current_user=Depends(get_current_user)):
    """Render the invites management page for admins."""
    return templates.TemplateResponse("invites.html", {
        "request": request,
        "user": current_user
    })



