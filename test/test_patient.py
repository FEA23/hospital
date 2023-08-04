import pytest

from patient import Patient


def test_create_patient():
    patient = Patient(3)
    assert patient.id == 3
    assert patient.status_id == 1
    assert patient.status_name == 'Болен'


@pytest.mark.parametrize("status_id, status_name", [
    (0, 'Тяжело болен'),
    (1, 'Болен'),
    (2, 'Слегка болен'),
    (3, 'Готов к выписке')
])
def test_status_name(status_id, status_name):
    patient = Patient(77)
    patient.status_id = status_id
    assert patient.status_name == status_name


def test_status_up():
    patient = Patient(77, status_id=0)
    assert patient.status_up()
    assert patient.status_id == 1


def test_negative_status_up():
    patient = Patient(77, status_id=3)
    assert not patient.status_up()
    assert patient.status_id == 3


def test_status_down():
    patient = Patient(77, status_id=3)
    assert patient.status_down()
    assert patient.status_id == 2


def test_negative_status_down():
    patient = Patient(77, status_id=0)
    assert not patient.status_down()
    assert patient.status_id == 0
