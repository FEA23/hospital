import pytest

from patient import Patient


def test_create_patient():
    patient = Patient(id=77, status_id=1)
    assert patient.id == 77
    assert patient.status_id == 1
    assert patient.status_name == 'Болен'


@pytest.mark.parametrize("status_id, status_name", [
    (0, 'Тяжело болен'),
    (1, 'Болен'),
    (2, 'Слегка болен'),
    (3, 'Готов к выписке')
])
def test_status_name(status_id, status_name):
    patient = Patient(id=77)
    patient.status_id = status_id
    assert patient.status_name == status_name
