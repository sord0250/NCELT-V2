import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from . import crud, models
from .db import SessionLocal, engine

# Ensure data folders exist
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EVIDENCE_DIR = DATA_DIR / "evidence"
OUTBOX_DIR = DATA_DIR / "outbox"
os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(OUTBOX_DIR, exist_ok=True)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["timedelta"] = timedelta
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

SESSION_SECRET = os.getenv("SESSION_SECRET_KEY", "dev-only-change-me")
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="ncelt_session",
    max_age=60 * 60 * 12,
    same_site="lax",
    https_only=False,
)


@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_optional(request: Request, db: Session) -> models.User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    user = crud.get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        request.session.pop("user_id", None)
        return None
    return user


def require_user(request: Request, db: Session) -> models.User:
    user = get_current_user_optional(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def require_manager(request: Request, db: Session) -> models.User:
    user = require_user(request, db)
    if not user.is_manager:
        raise HTTPException(status_code=403, detail="Manager role required")
    return user


def render_template(request: Request, name: str, context: dict, db: Session):
    current_user = get_current_user_optional(request, db)
    merged_context = {"request": request, "current_user": current_user, "today": date.today(), **context}
    return templates.TemplateResponse(name, merged_context)


def get_review_status(review_dt: datetime | None, lifecycle_length: int | None, today: date) -> str | None:
    if not review_dt or lifecycle_length is None:
        return None
    next_review = review_dt + timedelta(days=lifecycle_length)
    days_until = (next_review.date() - today).days
    if days_until <= 3:
        return "red"
    if days_until <= 21:
        return "yellow"
    return "green"


def get_next_review_date(review_dt: datetime | None, lifecycle_length: int | None) -> datetime | None:
    if not review_dt or lifecycle_length is None:
        return None
    return review_dt + timedelta(days=lifecycle_length)


@app.get("/setup")
def setup_page(request: Request, db: Session = Depends(get_db)):
    users = crud.list_users(db)
    if users:
        return RedirectResponse(url="/login", status_code=303)
    return render_template(request, "setup.html", {}, db)


@app.post("/setup")
def setup_handler(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    users = crud.list_users(db)
    if users:
        return RedirectResponse(url="/login", status_code=303)
    if len(password) < 8:
        return render_template(
            request,
            "setup.html",
            {"error": "Password must be at least 8 characters."},
            db,
        )
    existing = crud.get_user_by_username(db, username)
    if existing:
        return render_template(request, "setup.html", {"error": "Username already exists."}, db)

    manager = crud.create_user(db, username=username, password=password, is_manager=True)
    request.session["user_id"] = manager.user_id
    return RedirectResponse(url="/", status_code=303)


@app.get("/login")
def login_page(request: Request, db: Session = Depends(get_db), next_path: str = Query("/", alias="next")):
    if not crud.list_users(db):
        return RedirectResponse(url="/setup", status_code=303)

    current_user = get_current_user_optional(request, db)
    if current_user:
        return RedirectResponse(url="/", status_code=303)

    return render_template(request, "login.html", {"next": next_path}, db)


@app.post("/login")
def login_handler(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next_path: str = Form("/"),
    db: Session = Depends(get_db),
):
    user = crud.authenticate_user(db, username=username, password=password)
    if not user:
        return render_template(
            request,
            "login.html",
            {"error": "Invalid username or password.", "next": next_path},
            db,
        )
    request.session["user_id"] = user.user_id
    return RedirectResponse(url=next_path if next_path.startswith("/") else "/", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/")
def dashboard(
    request: Request,
    review_status: str = Query("all"),
    owner_id: str | None = Query(None),
    db: Session = Depends(get_db),
):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/", status_code=303)
    today = date.today()
    evidence = crud.list_evidence(db)
    owners = crud.get_owners(db)
    selected_owner_id = int(owner_id) if owner_id and owner_id.isdigit() else None

    filtered_evidence = []
    for item in evidence:
        if selected_owner_id is not None and item.owner_id != selected_owner_id:
            continue
        dt = item.last_reviewed_at if item.last_reviewed_at else item.uploaded_at
        item.review_status = get_review_status(dt, item.lifecycle_length, today)
        if review_status != "all" and item.review_status != review_status:
            continue
        filtered_evidence.append(item)

    return render_template(
        request,
        "dashboard.html",
        {
            "evidence": filtered_evidence,
            "owners": owners,
            "selected_review_status": review_status,
            "selected_owner_id": selected_owner_id,
        },
        db,
    )


@app.get("/framework")
def framework_dashboard(
    request: Request,
    review_status: str = Query("all"),
    evidence_presence: str = Query("all"),
    db: Session = Depends(get_db),
):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/", status_code=303)
    today = date.today()
    outcomes = crud.get_outcomes(db)
    filtered_outcomes = []
    for outcome in outcomes:
        latest = None
        last_dt = None
        for ev in outcome.evidence_items:
            ev_dt = ev.last_reviewed_at if ev.last_reviewed_at else ev.uploaded_at
            if ev_dt and (last_dt is None or ev_dt > last_dt):
                latest = ev
                last_dt = ev_dt

        outcome.latest_evidence = latest
        outcome.last_review_dt = last_dt
        outcome.review_status = get_review_status(last_dt, latest.lifecycle_length if latest else None, today)
        outcome.has_evidence = latest is not None

        if evidence_presence == "missing" and outcome.has_evidence:
            continue
        if evidence_presence == "present" and not outcome.has_evidence:
            continue
        if review_status != "all":
            if outcome.review_status != review_status:
                continue
        filtered_outcomes.append(outcome)

    return render_template(
        request,
        "framework.html",
        {
            "outcomes": filtered_outcomes,
            "selected_review_status": review_status,
            "selected_evidence_presence": evidence_presence,
        },
        db,
    )


@app.get("/evidence-record/{evidence_id}", name="evidence_detail")
def evidence_detail_page(request: Request, evidence_id: int, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url=f"/login?next=/evidence-record/{evidence_id}", status_code=303)

    evidence = crud.get_evidence_by_id(db, evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    review_dt = evidence.last_reviewed_at if evidence.last_reviewed_at else evidence.uploaded_at
    next_review = get_next_review_date(review_dt, evidence.lifecycle_length)
    review_status = get_review_status(review_dt, evidence.lifecycle_length, date.today())
    return render_template(
        request,
        "evidence_detail.html",
        {
            "evidence": evidence,
            "review_dt": review_dt,
            "next_review": next_review,
            "review_status": review_status,
        },
        db,
    )


@app.post("/evidence-record/{evidence_id}/review")
def update_evidence_review(
    request: Request,
    evidence_id: int,
    last_reviewed_date: date = Form(...),
    db: Session = Depends(get_db),
):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url=f"/login?next=/evidence-record/{evidence_id}", status_code=303)

    evidence = crud.get_evidence_by_id(db, evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    last_reviewed_at = datetime.combine(last_reviewed_date, datetime.min.time())
    crud.update_evidence_last_reviewed(db, evidence_id=evidence_id, last_reviewed_at=last_reviewed_at)
    return RedirectResponse(url=f"/evidence-record/{evidence_id}", status_code=303)


@app.post("/evidence-record/{evidence_id}/delete")
def delete_evidence_record(request: Request, evidence_id: int, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url=f"/login?next=/evidence-record/{evidence_id}", status_code=303)

    evidence = crud.get_evidence_by_id(db, evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    file_path = evidence.file_path
    crud.delete_evidence(db, evidence_id)

    if file_path:
        try:
            os.remove(os.path.join(EVIDENCE_DIR, file_path))
        except FileNotFoundError:
            pass

    return RedirectResponse(url="/", status_code=303)


@app.get("/owners/new")
def owner_create_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/owners/new", status_code=303)
    return render_template(request, "create_owner.html", {}, db)


@app.post("/owners/new")
def owner_create_handler(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    jobrole: str | None = Form(None),
    db: Session = Depends(get_db),
):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/owners/new", status_code=303)

    existing_email = email.strip().lower()
    if db.query(models.Owner).filter(models.Owner.email == existing_email).first():
        return render_template(
            request,
            "create_owner.html",
            {"error": "Owner with that email already exists."},
            db,
        )

    crud.create_owner(db, name=name, email=existing_email, jobrole=jobrole, created_by_user_id=user.user_id)
    return RedirectResponse(url="/upload", status_code=303)


@app.get("/users/new")
def user_create_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/users/new", status_code=303)
    if not user.is_manager:
        raise HTTPException(status_code=403, detail="Manager role required")

    users = crud.list_users(db)
    return render_template(request, "create_user.html", {"users": users}, db)


@app.post("/users/new")
def user_create_handler(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    is_manager: bool = Form(False),
    db: Session = Depends(get_db),
):
    manager = get_current_user_optional(request, db)
    if not manager:
        return RedirectResponse(url="/login?next=/users/new", status_code=303)
    if not manager.is_manager:
        raise HTTPException(status_code=403, detail="Manager role required")

    if len(password) < 8:
        users = crud.list_users(db)
        return render_template(
            request,
            "create_user.html",
            {"error": "Password must be at least 8 characters.", "users": users},
            db,
        )

    if crud.get_user_by_username(db, username):
        users = crud.list_users(db)
        return render_template(
            request,
            "create_user.html",
            {"error": "Username already exists.", "users": users},
            db,
        )

    crud.create_user(db, username=username, password=password, is_manager=is_manager)
    return RedirectResponse(url="/users/new", status_code=303)


def secure_filename_fallback(filename: str) -> str:
    if not filename:
        return "upload"
    filename = os.path.basename(filename)
    filename = re.sub(r"\s+", "_", filename)
    filename = re.sub(r"[^A-Za-z0-9._-]", "", filename)
    return filename or "upload"


def make_safe_filename(orig: str) -> str:
    base = secure_filename_fallback(orig)
    return f"{uuid4().hex}_{base}"


@app.get("/upload")
def upload_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/upload", status_code=303)

    owners = crud.get_owners(db)
    outcomes = crud.get_outcomes(db)
    return render_template(request, "upload.html", {"owners": owners, "outcomes": outcomes}, db)


@app.post("/upload")
async def upload_handler(
    request: Request,
    title: str = Form(...),
    description: str | None = Form(None),
    owner_id: int = Form(...),
    outcome_ids: List[str] | None = Form(None),
    lifecycle_months: int = Form(3),
    last_reviewed_date: date = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login?next=/upload", status_code=303)

    if not title:
        raise HTTPException(status_code=400, detail="Title required")

    safe_base = make_safe_filename(file.filename or "upload")
    filename = safe_base
    dest_path = os.path.join(EVIDENCE_DIR, filename)

    try:
        with open(dest_path, "wb") as out_f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                out_f.write(chunk)
    except Exception as exc:
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to save file: {exc}")

    outcome_ids_parsed: List[str] = []
    if outcome_ids:
        outcome_ids_parsed = [s for s in outcome_ids if isinstance(s, str) and s.strip()]
    lifecycle_months = max(1, lifecycle_months)
    lifecycle_length = lifecycle_months * 30
    last_reviewed_at = datetime.combine(last_reviewed_date, datetime.min.time())

    try:
        crud.create_evidence(
            db=db,
            title=title,
            file_path=filename,
            owner_id=owner_id,
            outcome_ids=outcome_ids_parsed,
            description=description,
            last_reviewed_at=last_reviewed_at,
            lifecycle_length=lifecycle_length,
        )
    except Exception as exc:
        try:
            os.remove(dest_path)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"DB error: {exc}")

    return RedirectResponse(url="/", status_code=303)


def secure_name(fname: str) -> str:
    if not fname:
        return ""
    return os.path.basename(fname)


@app.get("/evidence/{filename}", name="evidence_file")
def evidence_file(filename: str):
    safe = secure_name(filename)
    if not safe:
        raise HTTPException(status_code=404, detail="Not found")

    full_path = os.path.join(EVIDENCE_DIR, safe)
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path, media_type=None, filename=safe)
