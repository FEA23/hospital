from hospital import Hospital
from patient import Patient


def test_discharge():
    hospital = Hospital()
    assert hospital.get_patient_by_id(123) is not None
    assert len(hospital._patients) == 200
    hospital.discharge(123)
    assert hospital.get_patient_by_id(123) is None
    assert len(hospital._patients) == 199


def test_calculate_statistics():
    hospital = Hospital([
        Patient(id=1, status_id=0),
        Patient(id=2, status_id=1),
        Patient(id=3, status_id=1),
        Patient(id=4, status_id=3)
    ])
    stats = hospital._calculate_statistics()
    assert stats == {0: 1, 1: 2, 2: 0, 3: 1}


def test_statistics_to_str():
    hospital = Hospital([
        Patient(id=1, status_id=0),
        Patient(id=2, status_id=1),
        Patient(id=3, status_id=1),
        Patient(id=4, status_id=3)
    ])
    result = hospital._statistics_to_str({0: 1, 1: 2, 2: 0, 3: 1})
    expected_result = (
        "В больнице на данный момент находится 4 чел., из них:\n"
        "- в статусе \"Тяжело болен\": 1 чел.\n"
        "- в статусе \"Болен\": 2 чел.\n"
        "- в статусе \"Готов к выписке\": 1 чел.\n"
    )
    assert expected_result == result


def test_get_status_name_by_patient_id():
    hospital = Hospital(patients=[Patient(id=77, status_id=0)])
    assert hospital.get_status_name_by_patient_id(77) == 'Тяжело болен'


def test_status_up():
    hospital = Hospital(patients=[Patient(id=77, status_id=1)])
    patient, up_is_succesfully = hospital.patient_status_up(77)
    assert up_is_succesfully
    assert patient.status_id == 2


def test_negative_status_up():
    hospital = Hospital(patients=[Patient(id=77, status_id=3)])
    patient, up_is_succesfully = hospital.patient_status_up(77)
    assert not up_is_succesfully
    assert patient.status_id == 3


def test_status_down():
    hospital = Hospital(patients=[Patient(id=77, status_id=1)])
    patient, down_is_succesfully = hospital.patient_status_down(77)
    assert down_is_succesfully
    assert patient.status_id == 0


def test_negative_status_down():
    hospital = Hospital(patients=[Patient(id=77, status_id=0)])
    patient, down_is_succesfully = hospital.patient_status_down(77)
    assert not down_is_succesfully
    assert patient.status_id == 0
