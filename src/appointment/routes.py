from src.appointment import bp
from flask import request, jsonify

import src.appointment.service as service

@bp.get('/')
def list_appointments():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    filters = request.args.to_dict()
    filters.pop('page', None)
    filters.pop('per_page', None)
    appointments = service.list_appointments(filters, page, per_page)
    return appointments

@bp.get('/<int:appointment_id>')
def get_appointment(appointment_id):
    appointment = service.get_appointment_by_id(appointment_id)
    if appointment:
        return appointment
    else:
        return jsonify({'error': 'Appointment not found'}), 404

@bp.post('/')
def create_appointment():
    data = request.json

    if('scheduling_id' not in data):
        return jsonify({'error': 'scheduling_id is required'}), 400

    scheduling_id = data.get('scheduling_id')
    icd10_ids = data.get('icd10_ids', [])
    annotation = data.get('annotation', '')
    appointment = service.create_appointment(scheduling_id, icd10_ids, annotation)
    return appointment

@bp.put('/<int:appointment_id>')
def update_appointment(appointment_id):
    data = request.json
    annotation = data.get('annotation', '')
    appointment = service.update_appointment(appointment_id, annotation)
    return appointment

@bp.post('/<int:appointment_id>/add-item')
def add_prescription_item(appointment_id):
    data = request.json
    medicine = data.get('medicine', '')
    dosage = data.get('dosage', '')
    frequency = data.get('frequency', '')
    doses = data.get('doses', '')
    prescription_item = service.add_prescription_item(appointment_id, medicine, dosage, frequency, doses)
    return prescription_item

@bp.delete('/<int:appointment_id>/items/<int:prescription_item_id>')
def remove_prescription_item(appointment_id:int, prescription_item_id:int):
    return service.remove_prescription_item(appointment_id, prescription_item_id)

@bp.patch('/<int:appointment_id>/items/<int:prescription_item_id>')
def update_prescription_item(appointment_id:int, prescription_item_id:int):
    data = request.json

    medicine = data.get('medicine')
    dosage = data.get('dosage')
    frequency = data.get('frequency')
    doses = data.get('doses')

    prescription_item = service.update_prescription_item(appointment_id, prescription_item_id, medicine, dosage, frequency, doses)
    return prescription_item

@bp.get('/icds')
def list_icd10s():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    icd10s = service.list_icd10s(page, per_page)
    return icd10s

@bp.post('/<int:appointment_id>/icds/<int:icd10_id>')
def add_icd(appointment_id:int, icd10_id:int):
    return service.add_icd(appointment_id, icd10_id)

@bp.delete('/<int:appointment_id>/icds/<int:icd10_id>')
def remove_icd(appointment_id:int, icd10_id:int):
    return service.remove_icd(appointment_id, icd10_id)
