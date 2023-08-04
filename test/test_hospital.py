from hospital import Hospital
from patient import Patient


def test_discharge():
    hospital = Hospital()
    hospital.discharge(123)
    assert hospital.get_patient_by_id(123) is None


def test_calculate_statistics():
    hospital = Hospital()
    hospital._PATIENTS = [
        Patient(23, status_id=0),
        Patient(77, status_id=1),
        Patient(123, status_id=2),
        Patient(200, status_id=3)
    ]
    stats = hospital._calculate_statistics()
    assert stats == {0: 1, 1: 1, 2: 1, 3: 1}


def test_statistics_to_str():
    hospital = Hospital()
    result = hospital._statistics_to_str(hospital._calculate_statistics())
    expected_result = (
        "В больнице на данный момент находится 200 чел., из них:\n"
        "- в статусе \"Болен\": 200 чел.\n"
    )
    assert expected_result in result