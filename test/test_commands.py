import pytest

from commands import Commands, CommandHandlers
from patient import Patient
from hospital import Hospital
from dialogue import Dialogue

PATIENT_ID = 77

hospital = Hospital()
dialogue = Dialogue()
command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)


def test_is_get_status():
    assert Commands('get status').is_get_status()
    assert Commands('узнать статус пациента').is_get_status()


def test_negative_is_get_status():
    assert not Commands('покажи какой статус у пациента').is_get_status()
    assert not Commands('show status').is_get_status()


def test_is_status_up():
    assert Commands('status up').is_up_status()
    assert Commands('повысить статус пациента').is_up_status()


def test_negative_is_status_up():
    assert not Commands('увеличь статус пациента ').is_up_status()
    assert not Commands('increase status').is_up_status()


def test_is_status_down():
    assert Commands('status down').is_down_status()
    assert Commands('понизить статус пациента').is_down_status()


def test_negative_is_status_down():
    assert not Commands('уменьшить статус пациента').is_down_status()
    assert not Commands('reduce status').is_down_status()


def test_is_discharge():
    assert Commands('discharge').is_discharge()
    assert Commands('выписать пациента').is_discharge()


def test_negative_is_discharge():
    assert not Commands('удалить пациента').is_discharge()
    assert not Commands('delete').is_discharge()


def test_is_statistic():
    assert Commands('рассчитать статистику').is_statistic()
    assert Commands('calculate statistic').is_statistic()

def test_negative_is_statistic():
    assert not Commands('покажи статистику').is_statistic()
    assert not Commands('get statistics').is_statistic()


def test_is_stop():
    assert Commands('стоп').is_stop()
    assert Commands('stop').is_stop()


def test_negative_is_stop():
    assert not Commands('выключить').is_stop()
    assert not Commands('off').is_stop()


@pytest.mark.parametrize("status_id, status_name", [
    (0, 'Тяжело болен'),
    (1, 'Болен'),
    (2, 'Слегка болен'),
    (3, 'Готов к выписке')
])
def test_handler_get_status(capsys, status_id, status_name):
    patient = Patient(PATIENT_ID)
    patient.status_id = status_id
    expected_result = 'Статус пациента: {}'.format(status_name)
    command_handlers.get_status(patient)
    captured_get_status = capsys.readouterr()
    assert expected_result in captured_get_status.out


def test_handler_status_up(capsys):
    patient = Patient(PATIENT_ID, status_id=1)
    command_handlers.status_up(patient)
    expected_result = 'Новый статус пациента: Слегка болен'
    captured_status_up = capsys.readouterr()
    assert patient.status_id == 2
    assert expected_result in captured_status_up.out


def test_user_refused_status_up(capsys, monkeypatch):
    patient = Patient(PATIENT_ID, status_id=3)
    monkeypatch.setattr('builtins.input', lambda _: 'нет')
    command_handlers.status_up(patient)
    expected_result = 'Пациент остался в статусе "Готов к выписке"'
    captured_status_up = capsys.readouterr()
    assert patient.status_id == 3
    assert expected_result in captured_status_up.out


def test_user_agreed_status_up(capsys, monkeypatch):
    patient = Patient(PATIENT_ID, status_id=3)
    monkeypatch.setattr('builtins.input', lambda _: 'да')
    command_handlers.status_up(patient)
    captured_status_up = capsys.readouterr()
    assert hospital.get_patient_by_id(PATIENT_ID) is None
    assert 'Пациент выписан из больницы' in captured_status_up.out


def test_handler_status_down(capsys):
    patient = Patient(PATIENT_ID, status_id=1)
    command_handlers.status_down(patient)
    expected_result = 'Новый статус пациента: Тяжело болен'
    captured_status_down = capsys.readouterr()
    assert patient.status_id == 0
    assert expected_result in captured_status_down.out


def test_negative_handler_status_down(capsys):
    patient = Patient(PATIENT_ID, status_id=0)
    command_handlers.status_down(patient)
    expected_result = 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'
    captured_status_down = capsys.readouterr()
    assert patient.status_id == 0
    assert expected_result in captured_status_down.out


def test_handler_discharge(capsys):
    patient = Patient(PATIENT_ID)
    command_handlers.discharge(patient)
    expected_result = 'Пациент выписан из больницы'
    captured_discharge = capsys.readouterr()
    assert hospital.get_patient_by_id(PATIENT_ID) is None
    assert expected_result in captured_discharge.out
