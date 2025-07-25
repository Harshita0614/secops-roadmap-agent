import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.agent_logic import run_agent

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_files(
    request: Request,
    sow_pdf: UploadFile = File(...),
    excel_tracker: UploadFile = File(...),
    email1: UploadFile = File(...),
    email2: UploadFile = File(...),
):
    # Save files
    paths = {}
    for file in [sow_pdf, excel_tracker, email1, email2]:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        paths[file.filename] = path

    # Run agent
    report = run_agent(
        pdf_path=paths[sow_pdf.filename],
        xlsx_path=paths[excel_tracker.filename],
        eml_paths=[paths[email1.filename], paths[email2.filename]]
    )

    return templates.TemplateResponse("report.html", {"request": request, "report": report})

