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


# Used to keep login timing the same whether or not the username exists
_DUMMY_PASSWORD_HASH = pwd_context.hash("dummy-password-for-timing")

MIN_PASSWORD_LENGTH = 8

COMMON_PASSWORDS = {
    "password", "password1", "password12", "password123", "password1234", "passw0rd",
    "p@ssw0rd", "p@ssword", "12345678", "123456789", "1234567890", "0123456789",
    "87654321", "11111111", "00000000", "12341234", "11223344", "1q2w3e4r",
    "1qaz2wsx", "qwertyui", "qwerty12", "qwerty123", "qwertyuiop", "asdfghjk",
    "asdfasdf", "zxcvbnm1", "abcd1234", "abc12345", "abcdefgh", "iloveyou",
    "iloveyou1", "sunshine", "princess", "football", "baseball", "superman",
    "starwars", "whatever", "trustno1", "letmein1", "welcome1", "welcome123",
    "changeme", "changeme1", "changeme123", "admin123", "admin1234", "administrator",
    "manager1", "manager123", "computer", "internet", "michelle", "jennifer",
    "corvette", "mercedes", "dragon12", "monkey12", "master12", "shadow12",
    "football1", "baseball1", "1password", "secret12", "secret123", "default1",
    "letmein123", "qazwsxedc", "access14", "security", "security1",
}


def validate_password(password: str, username: str = "") -> str | None:
    """Return an error message if the password is unacceptable, otherwise None."""
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    if password.lower() in COMMON_PASSWORDS:
        return "That password is too common. Please choose a different one."
    if username and password.lower() == username.strip().lower():
        return "Password must not be the same as the username."
    return None


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
    if not user:
        verify_password(password, _DUMMY_PASSWORD_HASH)
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
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
