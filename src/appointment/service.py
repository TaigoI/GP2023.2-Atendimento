from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Optional
from flask import jsonify

from src.appointment.model import ICD10, Appointment, PrescriptionItem, Base

engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def list_icd10s(page: int = 1, per_page: int = 10) -> List[ICD10]:
    session = Session()
    try:
        query = session.query(ICD10)
        icd10s = query.limit(per_page).offset((page - 1) * per_page).all()
        return icd10s
    finally:
        session.expunge_all()
        session.close()


def create_appointment(scheduling_id: int, icd10_ids: List[int], annotation: str) -> Appointment:
    session = Session()
    try:
        icd10s = session.query(ICD10).filter(ICD10.id.in_(icd10_ids)).all() if len(icd10_ids) > 0 else []
        appointment = Appointment(scheduling_id=scheduling_id, icd10s=icd10s, annotation=annotation)
        session.add(appointment)
        session.commit()
        return jsonify(appointment)
    finally:
        session.expunge_all()
        session.close()


def update_appointment(appointment_id: int, annotation: str) -> Appointment:
    session = Session()
    try:
        appointment = session.query(Appointment).get(appointment_id)
        appointment.annotation = annotation
        session.commit()
        return jsonify(appointment)
    except NoResultFound:
        return jsonify({'error': 'Appointment not found'})
    finally:
        session.expunge_all()
        session.close()


def get_appointment_by_id(appointment_id: int) -> Optional[Appointment]:
    session = Session()
    try:
        appointment = session.query(Appointment).get(appointment_id)
        return jsonify(appointment)
    finally:
        session.expunge_all()
        session.close()


def list_appointments(filters: dict = None, page: int = 1, per_page: int = 10) -> List[Appointment]:
    session = Session()
    try:
        query = session.query(Appointment)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Appointment, key) == value)
        appointments = query.limit(per_page).offset((page - 1) * per_page).all()
        return jsonify(appointments)
    finally:
        session.expunge_all()
        session.close()


def add_prescription_item(appointment_id: int, medicine: str, dosage: str, frequency: str, doses: str) -> PrescriptionItem:
    session = Session()
    try:
        prescription_item = PrescriptionItem(appointment_id=appointment_id, medicine=medicine, dosage=dosage, frequency=frequency, doses=doses)
        session.add(prescription_item)
        session.commit()
        return jsonify(prescription_item)
    finally:
        session.expunge_all()
        session.close()


def remove_prescription_item(appointment_id: int, prescription_item_id: int) -> PrescriptionItem:
    session = Session()
    try:
        prescription_item = session.query(PrescriptionItem).get(prescription_item_id)

        if(not prescription_item or prescription_item.appointment_id != appointment_id):
            return jsonify({'error': 'Item not found'})

        session.delete(prescription_item)
        session.commit()
        return jsonify(prescription_item)
    finally:
        session.expunge_all()
        session.close()


def update_prescription_item(appointment_id: int, prescription_item_id: int, medicine: str = None, dosage: str = None, frequency: str = None, doses: str = None) -> PrescriptionItem:
    session = Session()
    try:
        prescription_item = session.query(PrescriptionItem).get(prescription_item_id)

        if(not prescription_item or prescription_item.appointment_id != appointment_id):
            return jsonify({'error': 'Item not found'})

        if medicine is not None:
            prescription_item.medicine = medicine
        if dosage is not None:
            prescription_item.dosage = dosage
        if frequency is not None:
            prescription_item.frequency = frequency
        if doses is not None:
            prescription_item.doses = doses
        session.commit()
        return jsonify(prescription_item)
    finally:
        session.expunge_all()
        session.close()

def add_icd(appointment_id: int, icd10_id: int) -> None:
    session = Session()
    try:
        appointment = session.query(Appointment).get(appointment_id)
        icd10 = session.query(ICD10).get(icd10_id)
        if icd10:
            if(icd10 in appointment.icd10s):
                return jsonify({'error': 'ICD already associated with the appointment'})
            appointment.icd10s.append(icd10)
            session.commit()
        else:
            return jsonify({'error': 'ICD not found'})
    finally:
        session.expunge_all()
        session.close()


def remove_icd(appointment_id: int, icd10_id: int) -> None:
    session = Session()
    try:
        appointment = session.query(Appointment).get(appointment_id)
        icd10 = session.query(ICD10).get(icd10_id)
        if icd10 in appointment.icd10s:
            appointment.icd10s.remove(icd10)
            session.commit()
            return jsonify(appointment)
        else:
            return jsonify({'error': 'ICD10 code not associated with the appointment'})
    finally:
        session.expunge_all()
        session.close()