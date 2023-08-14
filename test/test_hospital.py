import pytest

from hospital import Hospital, CantLowerStatusError, CantIncreaseStatusError
from patient import Patient


def test_discharge():
    hospital = Hospital()
    assert hospital._get_patient_by_id(123) is not None
    assert len(hospital._patients) == 200
    hospital.discharge(123)
    assert hospital._get_patient_by_id(123) is None
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
    hospital = Hospital()
    result = hospital._statistics_to_str({0: 1, 1: 2, 2: 0, 3: 1})
    expected_result = (
        "В больнице на данный момент находится 200 чел., из них:\n"
        "- в статусе \"Тяжело болен\": 1 чел.\n"
        "- в статусе \"Болен\": 2 чел.\n"
        "- в статусе \"Готов к выписке\": 1 чел.\n"
    )
    assert result == expected_result


def test_get_status_name_by_patient_id():
    hospital = Hospital(patients=[Patient(id=77, status_id=0)])
    assert hospital.get_status_name_by_patient_id(77) == 'Тяжело болен'


def test_can_status_up():
    hospital = Hospital([Patient(id=77, status_id=1)])
    result = hospital.can_status_up(77)
    assert result


def test_negative_can_status_up():
    hospital = Hospital([Patient(id=77, status_id=3)])
    result = hospital.can_status_up(77)
    assert not result


def test_status_up():
    hospital = Hospital(patients=[Patient(id=77, status_id=1)])
    hospital.patient_status_up(77)
    status = hospital._get_patient_by_id(77).status_id
    assert status == 2


def test_negative_status_up():
    hospital = Hospital(patients=[Patient(id=77, status_id=3)])
    with pytest.raises(CantIncreaseStatusError):
        hospital.patient_status_up(77)


def test_can_status_down():
    hospital = Hospital([Patient(id=77, status_id=1)])
    result = hospital.can_status_up(77)
    assert result


def test_negative_can_status_down():
    hospital = Hospital(patients=[Patient(id=77, status_id=0)])
    result = hospital.can_status_down(77)
    assert not result


def test_status_down():
    hospital = Hospital(patients=[Patient(id=77, status_id=1)])
    hospital.patient_status_down(77)
    status = hospital._get_patient_by_id(77).status_id
    assert status == 0


def test_negative_status_down():
    hospital = Hospital(patients=[Patient(id=77, status_id=0)])
    with pytest.raises(CantLowerStatusError):
        hospital.patient_status_down(77)


def test_patient_exists():
    hospital = Hospital()
    assert hospital.patient_exists(1)


def test_negative_patient_exists():
    hospital = Hospital()
    assert not hospital.patient_exists(201)
