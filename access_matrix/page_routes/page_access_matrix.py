from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/access_matrix", response_class=HTMLResponse)
def page_access_matrix(request: Request):
    return templates.TemplateResponse("access_matrix.html", {"request": request, "title": "Access Matrix"})
