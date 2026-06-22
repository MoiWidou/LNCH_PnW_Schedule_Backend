from pydantic import BaseModel
from datetime import date
from typing import Optional
import uuid

class LNHCScheduleCreate(BaseModel):
    date: date
    song_leader_id: Optional[uuid.UUID]
    backup_id: Optional[uuid.UUID]
    lead_guitar_id: Optional[uuid.UUID]
    acoustic_id: Optional[uuid.UUID]
    bass_id: Optional[uuid.UUID]
    keyboard_id: Optional[uuid.UUID]
    drummer_id: Optional[uuid.UUID]
    sound_tech_id: Optional[uuid.UUID]
    easy_worship_id: Optional[uuid.UUID]

class TangwayScheduleCreate(BaseModel):
    date: date

    song_leader_id: Optional[uuid.UUID] = None
    musician_id: Optional[uuid.UUID] = None
    multimedia_id: Optional[uuid.UUID] = None
    sound_tech_id: Optional[uuid.UUID] = None

class GarciaRosarioScheduleCreate(BaseModel):
    date: date

    singer_id: Optional[uuid.UUID] = None
    musicians_id: Optional[uuid.UUID] = None