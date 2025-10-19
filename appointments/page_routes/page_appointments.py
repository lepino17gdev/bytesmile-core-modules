# modules/appointments/page_routes/appointments_page.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/appointments", tags=["Appointments Pages"])

@router.get("/", response_class=HTMLResponse)
async def appointments_page(request: Request):
    """Renders the main Appointments page."""
    return templates.TemplateResponse("appointments.html", {"request": request})
