import pytest

from hospital import Hospital
from patient import Patient
from dialogue import Dialogue


@pytest.fixture
def hospital():
    return Hospital()


@pytest.fixture
def patient():
    return Patient(patient_id=1)


@pytest.fixture
def dialogue(hospital):
    return Dialogue(hospital)