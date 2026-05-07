from sqlalchemy.orm import Session, joinedload
from sqlalchemy import case
from datetime import datetime
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def list_users(db: Session):
    return db.query(models.User).order_by(models.User.username).all()


def create_user(db: Session, username: str, password: str, is_manager: bool = False):
    user = models.User(
        username=username.strip(),
        password_hash=hash_password(password),
        is_manager=is_manager,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username.strip())
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_owners(db: Session):
    return db.query(models.Owner).order_by(models.Owner.name).all()


def create_owner(db: Session, name: str, email: str, jobrole: str | None, created_by_user_id: int | None):
    owner = models.Owner(
        name=name.strip(),
        email=email.strip().lower(),
        jobrole=(jobrole or None),
        created_by_user_id=created_by_user_id,
    )
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner

FUNCTION_ORDER = {
    "Govern": 1,
    "Identify": 2,
    "Protect": 3,
    "Detect": 4,
    "Respond": 5,
    "Recover": 6,
}
def get_outcomes(db: Session):
    order_case = case(FUNCTION_ORDER, value=models.Outcome.function)
    return db.query(models.Outcome)\
        .options(joinedload(models.Outcome.evidence_items))\
        .order_by(order_case, models.Outcome.category, models.Outcome.subcat_id)\
        .all()

def list_evidence(db: Session):
    return db.query(models.Evidence).order_by(models.Evidence.uploaded_at.desc()).all()


def get_evidence_by_id(db: Session, evidence_id: int):
    return (
        db.query(models.Evidence)
        .options(joinedload(models.Evidence.owner), joinedload(models.Evidence.outcomes))
        .filter(models.Evidence.evidence_id == evidence_id)
        .first()
    )

def create_evidence(
    db: Session,
    title: str,
    file_path: str,
    owner_id: int,
    outcome_ids: list[str],
    description: str | None = None,
    last_reviewed_at: datetime | None = None,
    lifecycle_length: int = 90,
):
    ev = models.Evidence(
        title=title,
        description=description,
        file_path=file_path,
        owner_id=owner_id,
        last_reviewed_at=last_reviewed_at,
        lifecycle_length=lifecycle_length,
    )
    # attach outcomes
    if outcome_ids:
        outcomes = db.query(models.Outcome).filter(models.Outcome.subcat_id.in_(outcome_ids)).all()
        ev.outcomes = outcomes
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


def update_evidence_last_reviewed(db: Session, evidence_id: int, last_reviewed_at: datetime):
    evidence = get_evidence_by_id(db, evidence_id)
    if not evidence:
        return None
    evidence.last_reviewed_at = last_reviewed_at
    db.commit()
    db.refresh(evidence)
    return evidence


def delete_evidence(db: Session, evidence_id: int):
    evidence = get_evidence_by_id(db, evidence_id)
    if not evidence:
        return None
    db.delete(evidence)
    db.commit()
    return evidence
