from hospital import Hospital
from patient import Patient


def test_discharge():
    hospital = Hospital()
    patient_id = 123
    hospital.discharge(patient_id)
    assert hospital.get_patient_by_id(patient_id) == None


def test_calculate_statistics():
    patient_status_id = 2
    hospital = Hospital()
    patient = Patient(23)
    patient._set_status(patient_status_id)
    hospital.PATIENTS = [patient]
    stats = hospital.calculate_statistics()
    assert stats[patient_status_id] == 1


def test_display_statistics():
    hospital = Hospital()
    assert isinstance(hospital.display_statistics(), str)