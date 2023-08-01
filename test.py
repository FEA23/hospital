import random

from commands import Commands


def test_discharge(hospital):
    random_patient_id = random.randint(1, 200)
    hospital.discharge(random_patient_id)
    assert random_patient_id not in hospital.PATIENTS


def test_calculate_statistics(hospital):
    assert isinstance(hospital.calculate_statistics(), str)


def test_init(patient):
    assert patient.id == 1
    assert patient.status_id == 1


def test_status_name(patient):
    patient.status_id = 0
    assert patient.status_name == 'Тяжело болен'

    patient.status_id = 1
    assert patient.status_name == 'Болен'

    patient.status_id = 2
    assert patient.status_name == 'Слегка болен'

    patient.status_id = 3
    assert patient.status_name == 'Готов к выписке'


def test_status_up(patient):
    patient.status_id = 0
    for i in range(1, 4):
        assert patient.status_up() is True
        assert patient.status_id == i

    patient.status_id = 3
    assert patient.status_up() is False
    assert patient.status_id == 3


def test_status_down(patient):
    patient.status_id = 3
    for i in range(4, 1):
        assert patient.status_down() is True
        assert patient.status_id == i

    patient.status_id = 0
    assert patient.status_down() is False
    assert patient.status_id == 0


def test_user_input_patient_id(dialogue, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3")
    patient_id = dialogue.user_input_patient_id()
    assert isinstance(patient_id, int)
    assert patient_id == 3


def test_user_input_main_command(dialogue, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "status up")
    command = dialogue.user_input_main_command()
    assert isinstance(command, Commands)
    assert command.is_up_status() is True


def test_user_input_need_discharge_patient(dialogue, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "да")
    need_discharge = dialogue.user_input_need_discharge_patient()
    assert isinstance(need_discharge, bool)
    assert need_discharge is True
