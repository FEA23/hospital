import pytest

from hospital import Hospital
from custom_exceptions import MaxStatusCannotUpError, MinStatusCannotDownError, PatientNotExistsError


def test_create_hospital():
    hospital = Hospital([1, 2, 3])
    assert hospital._patients == [1, 2 ,3]
    assert hospital.status == {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}


def test_get_status_by_patient_id():
    hospital = Hospital([1, 2, 3, 0])
    assert hospital.get_status_by_patient_id(1) == "Болен"


def test_get_status_by_patient_id_not_exists():
    hospital = Hospital()
    with pytest.raises(PatientNotExistsError) as err:
        hospital.get_status_by_patient_id(201)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_status_up():
    hospital = Hospital([1, 1, 3])
    hospital.status_up(2)
    assert hospital._patients == [1, 2, 3]


def test_status_up_if_max():
    hospital = Hospital([1, 1, 3])
    with pytest.raises(MaxStatusCannotUpError) as err:
        hospital.status_up(3)
    assert hospital._patients == [1, 1, 3]
    assert str(err.value) == 'Ошибка. Нельзя повысить самый высокий статус. Но этого пациента можно выписать'


def test_status_up_not_exists():
    hospital = Hospital()
    with pytest.raises(PatientNotExistsError) as err:
        hospital.status_up(201)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_status_down():
    hospital = Hospital([2, 1, 2])
    hospital.status_down(3)
    assert hospital._patients == [2, 1, 1]


def test_status_down_if_min():
    hospital = Hospital([2, 0, 2])
    with pytest.raises(MinStatusCannotDownError) as err:
        hospital.status_down(2)
    assert hospital._patients == [2, 0, 2]
    assert str(err.value) == 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'


def test_status_donw_not_exists():
    hospital = Hospital()
    with pytest.raises(PatientNotExistsError) as err:
        hospital.status_up(201)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'


def test_discharge():
    hospital = Hospital([2, 1, 2])
    hospital.discharge(2)
    assert hospital._patients == [2, 2]


def test_statistics():
    hospital = Hospital([1, 2, 3, 0, 1])
    stats = hospital._statistics()
    expected_counts = {"Тяжело болен": 1, "Болен": 2, "Слегка болен": 1, "Готов к выписке": 1}
    assert stats == {"status_count": expected_counts, "total_patients": len(hospital._patients)}


def test_format_patient_statistics():
    hospital = Hospital([1, 2, 2, 0, 1])
    formatted_stats = hospital.format_patient_statistics()
    expected_output = (
        "В больнице на данный момент находится 5 чел., из них:\n" +
        "\t- в статусе \"Тяжело болен\": 1 чел.\n" +
        "\t- в статусе \"Болен\": 2 чел.\n" +
        "\t- в статусе \"Слегка болен\": 2 чел.\n" +
        "\t- в статусе \"Готов к выписке\": 0 чел."
    )

    assert formatted_stats == expected_output

def test_can_status_up():
    hospital = Hospital([2, 1, 2])
    assert hospital.can_status_up(2)


def test_negative_can_status_up():
    hospital = Hospital([2, 3, 2])
    assert not hospital.can_status_up(2)


def test_can_status_down():
    hospital = Hospital([2, 1, 2])
    assert hospital.can_status_down(2)


def test_negative_can_status_down():
    hospital = Hospital([2, 0, 2])
    assert not hospital.can_status_down(2)


def test_verify_patient_exists():
    hospital = Hospital()
    hospital._verify_patient_exists(10)


def test_verify_patient_not_exists():
    hospital = Hospital()
    with pytest.raises(PatientNotExistsError) as err:
        hospital._verify_patient_exists(201)
    assert str(err.value) == 'Ошибка. В больнице нет пациента с таким ID'
