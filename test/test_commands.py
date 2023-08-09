from commands import Commands, CommandHandlers
from patient import Patient
from hospital import Hospital
from dialogue import Dialogue


hospital = Hospital(patients=[
    Patient(id=1, status_id=1),
    Patient(id=2, status_id=3),
    Patient(id=3, status_id=0)
])
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
    assert not Commands('увеличить статус пациента').is_up_status()
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


def test_handler_get_status(capsys):
    command_handlers.get_status(2)
    captured_get_status = capsys.readouterr()
    assert captured_get_status.out == 'Статус пациента: Готов к выписке\n'


def test_handler_status_up(capsys):
    command_handlers.status_up(1)
    patient = hospital.get_patient_by_id(1)
    captured_status_up = capsys.readouterr()
    assert patient.status_id == 2
    assert captured_status_up.out == 'Новый статус пациента: Слегка болен\n'


def test_user_refused_status_up(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'нет')
    command_handlers.status_up(patient_id=2)
    patient = hospital.get_patient_by_id(patient_id=2)
    captured_status_up = capsys.readouterr()
    assert patient.status_id == 3
    assert captured_status_up.out == 'Пациент остался в статусе "Готов к выписке"\n'


def test_user_agreed_status_up(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'да')
    command_handlers.status_up(patient_id=2)
    captured_status_up = capsys.readouterr()
    assert hospital.get_patient_by_id(patient_id=2) is None
    assert captured_status_up.out == 'Пациент выписан из больницы\n'


def test_handler_status_down(capsys):
    command_handlers.status_down(patient_id=1)
    patient = hospital.get_patient_by_id(patient_id=1)
    captured_status_down = capsys.readouterr()
    assert patient.status_id == 0
    assert captured_status_down.out == 'Новый статус пациента: Тяжело болен\n'


def test_negative_handler_status_down(capsys):
    command_handlers.status_down(patient_id=3)
    patient = hospital.get_patient_by_id(patient_id=3)
    captured_status_down = capsys.readouterr()
    assert patient.status_id == 0
    expected_result = 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)\n'
    assert expected_result == captured_status_down.out


def test_handler_discharge(capsys):
    command_handlers.discharge(patient_id=1)
    captured_discharge = capsys.readouterr()
    assert hospital.get_patient_by_id(1) is None
    assert captured_discharge.out == 'Пациент выписан из больницы\n'
