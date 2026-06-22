from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import Member
from db import engine
from services.scheduling_service import SchedulingService

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session

@router.get("/members")
def get_members(session: Session = Depends(get_session)):
    statement = select(Member).where(Member.is_active == True)
    results = session.exec(statement).all()
    return results

@router.get("/availability")
def check_availability(
    member_id: str,
    date: str,
    session: Session = Depends(get_session),
):
    available = SchedulingService.is_member_available(
        session,
        member_id,
        date
    )

    return {
        "member_id": member_id,
        "date": date,
        "available": available
    }