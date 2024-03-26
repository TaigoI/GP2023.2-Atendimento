from __future__ import annotations
from typing import List

# Dataclasses Imports
from dataclasses import dataclass
from dataclasses_json import dataclass_json

# ORM Imports
from sqlalchemy import update
from sqlalchemy import ForeignKey, String, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship




class Base(DeclarativeBase):
    pass




@dataclass
@dataclass_json
class Appointment(Base):
    __tablename__ = 'appointment'

    id: Mapped[int] = mapped_column(primary_key=True)

    scheduling_id: Mapped[int] = mapped_column(Integer) #Ignoring... just for registering, is not used currently

    icd10s: Mapped[List[ICD10]] = relationship(secondary="appointment_icd10")

    items: Mapped[List[PrescriptionItem]] = relationship()

    annotation: Mapped[str] = mapped_column(String(1000))



# Many to many association table
appointment_icd10 = Table(
    "appointment_icd10",
    Base.metadata,
    Column("icd10_id",       ForeignKey("icd10.id"),       primary_key=True),
    Column("appointment_id", ForeignKey("appointment.id"), primary_key=True),
)




@dataclass
@dataclass_json
class PrescriptionItem(Base):
    __tablename__ = "prescription_item"

    id: Mapped[int] = mapped_column(primary_key=True)

    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointment.id"))

    medicine: Mapped[str] = mapped_column(String(300))
    dosage: Mapped[str] = mapped_column(String(300))
    frequency: Mapped[str] = mapped_column(String(300))
    doses: Mapped[str] = mapped_column(String(300))




@dataclass
@dataclass_json
class ICD10(Base):
    __tablename__ = 'icd10'

    id: Mapped[int] = mapped_column(primary_key=True)

    description: Mapped[str] = mapped_column()