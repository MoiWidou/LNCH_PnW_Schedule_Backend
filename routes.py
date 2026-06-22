from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import GarciaRosarioSchedule, LNHCSchedule, Member, TangwaySchedule
from db import engine
from schemas.schemas import GarciaRosarioScheduleCreate, TangwayScheduleCreate, LNHCScheduleCreate
from services.scheduling_service import SchedulingService
from datetime import date
import uuid

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


# =====================
# Getting Members on DB for the PnW Members
# =====================

@router.get("/members")
def get_members(session: Session = Depends(get_session)):
    statement = select(Member).where(Member.is_active == True)
    results = session.exec(statement).all()
    return results


# =====================
# Getting Availability of the PnW For Conflict (Not sure if needed)
# =====================

@router.get("/availability")
def check_availability(
    member_id: uuid.UUID,
    date: date,
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

# =====================
# Adding Schedule LNCH
# =====================

@router.post("/lnhc")
def create_lnhc_schedule(
    payload: LNHCScheduleCreate,
    session: Session = Depends(get_session)
):

    # Step 1: gather all members in the schedule
    member_ids = [
        payload.song_leader_id,
        payload.backup_id,
        payload.lead_guitar_id,
        payload.acoustic_id,
        payload.bass_id,
        payload.keyboard_id,
        payload.drummer_id,
        payload.sound_tech_id,
        payload.easy_worship_id,
    ]

    # Step 2: conflict check
    if not SchedulingService.validate_members(session, member_ids, payload.date):
        raise HTTPException(
            status_code=400,
            detail="Member already scheduled on this date"
        )

    # Step 3: save to DB
    schedule = LNHCSchedule(**payload.model_dump()())

    return SchedulingService.save(session, schedule)

# =====================
# Adding Schedule Tangway
# =====================

@router.post("/tangway")
def create_tangway_schedule(
    payload: TangwayScheduleCreate,
    session: Session = Depends(get_session)
):

    member_ids = [
        payload.song_leader_id,
        payload.musician_id,
        payload.multimedia_id,
        payload.sound_tech_id,
    ]

    if not SchedulingService.validate_members(session, member_ids, payload.date):
        raise HTTPException(
            status_code=400,
            detail="Member already scheduled on this date"
        )

    schedule = TangwaySchedule(**payload.model_dump()())

    return SchedulingService.save(session, schedule)

# =====================
# Adding Schedule Garcia/Rosario
# =====================

@router.post("/garcia-rosario")
def create_gr_schedule(
    payload: GarciaRosarioScheduleCreate,
    session: Session = Depends(get_session)
):

    member_ids = [
        payload.singer_id,
        payload.musicians_id,
    ]

    if not SchedulingService.validate_members(session, member_ids, payload.date):
        raise HTTPException(
            status_code=400,
            detail="Member already scheduled on this date"
        )

    schedule = GarciaRosarioSchedule(**payload.model_dump()())

    return SchedulingService.save(session, schedule)