from sqlmodel import Session, or_, select
from datetime import date
import uuid
from models import (
    LNHCSchedule,
    TangwaySchedule,
    GarciaRosarioSchedule,
)


class SchedulingService:

    @staticmethod
    def is_member_available(session: Session, member_id: uuid.UUID, date: date):
        """
        Returns True if member is NOT scheduled anywhere on that date.
        Returns False if conflict exists.
        """

        return not SchedulingService._has_conflict(session, member_id, date)

    @staticmethod
    def validate_members(session: Session, member_ids: list, date: date) -> bool:
        for member_id in member_ids:
            if member_id:
                if not SchedulingService.is_member_available(session, member_id, date):
                    return False
        return True

    @staticmethod
    def _has_conflict(session: Session, member_id: str, date) -> bool:

        # ---------- LNHC ----------
        lnhc_conflict = session.exec(
            select(LNHCSchedule).where(
                LNHCSchedule.date == date,
                or_(
                    LNHCSchedule.song_leader_id == member_id,
                    LNHCSchedule.backup_id == member_id,
                    LNHCSchedule.lead_guitar_id == member_id,
                    LNHCSchedule.acoustic_id == member_id,
                    LNHCSchedule.bass_id == member_id,
                    LNHCSchedule.keyboard_id == member_id,
                    LNHCSchedule.drummer_id == member_id,
                    LNHCSchedule.sound_tech_id == member_id,
                    LNHCSchedule.easy_worship_id == member_id,
                )
            )
        ).first()

        if lnhc_conflict:
            return True

        # ---------- TANGWAY ----------
        tangway_conflict = session.exec(
            select(TangwaySchedule).where(
                TangwaySchedule.date == date,
                or_(
                    TangwaySchedule.song_leader_id == member_id,
                    TangwaySchedule.musician_id == member_id,
                    TangwaySchedule.multimedia_id == member_id,
                    TangwaySchedule.sound_tech_id == member_id,
                )
            )
        ).first()

        if tangway_conflict:
            return True

        # ---------- GARCIA / ROSARIO ----------
        gr_conflict = session.exec(
            select(GarciaRosarioSchedule).where(
                GarciaRosarioSchedule.date == date,
                or_(
                    GarciaRosarioSchedule.singer_id == member_id,
                    GarciaRosarioSchedule.musicians_id == member_id,
                )
            )
        ).first()

        if gr_conflict:
            return True

        return False

    @staticmethod
    def save(session: Session, obj):
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj