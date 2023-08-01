import pytest

from hospital import Hospital
from patient import Patient
from dialogue import Dialogue


@pytest.fixture(scope="class")
def hospital():
    return Hospital()


@pytest.fixture(scope="class")
def patient():
    return Patient(patient_id=1)


@pytest.fixture(scope="class")
def dialogue(hospital):
    return Dialogue(hospital)