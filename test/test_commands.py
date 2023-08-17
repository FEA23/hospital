from unittest.mock import MagicMock

from commands import Commands, CommandHandlers
from patient import Patient
from hospital import Hospital
from dialogue import Dialogue


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


def test_handler_get_status():
    hospital = Hospital(patients=[Patient(id=11, status_id=3)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_print_message = MagicMock()
    command_handlers.get_status(11)
    dialogue.user_print_message.assert_called_once_with('Статус пациента: Готов к выписке')


def test_handler_status_up():
    hospital = Hospital(patients=[Patient(id=10, status_id=1)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_print_message = MagicMock()
    command_handlers.status_up(10)
    patient = hospital._get_patient_by_id(10)
    assert patient.status_id == 2
    dialogue.user_print_message.assert_called_once_with('Новый статус пациента: Слегка болен')


def test_user_refused_status_up():
    hospital = Hospital(patients=[Patient(id=11, status_id=3)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_input_need_discharge_patient = MagicMock(return_value=False)
    dialogue.user_print_message = MagicMock()
    command_handlers.status_up(patient_id=11)
    patient = hospital._get_patient_by_id(patient_id=11)
    assert patient.status_id == 3
    dialogue.user_print_message.assert_called_once_with('Пациент остался в статусе "Готов к выписке"')


def test_user_agreed_status_up():
    hospital = Hospital(patients=[Patient(id=11, status_id=3)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_input_need_discharge_patient = MagicMock(return_value=True)
    dialogue.user_print_message = MagicMock()
    command_handlers.status_up(patient_id=11)
    assert hospital._get_patient_by_id(patient_id=11) is None
    dialogue.user_print_message.assert_called_once_with('Пациент выписан из больницы')


def test_handler_status_down():
    hospital = Hospital(patients=[Patient(id=10, status_id=1)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_print_message = MagicMock()
    command_handlers.status_down(patient_id=10)
    patient = hospital._get_patient_by_id(patient_id=10)
    assert patient.status_id == 0
    dialogue.user_print_message.assert_called_once_with('Новый статус пациента: Тяжело болен')


def test_negative_handler_status_down():
    hospital = Hospital(patients=[Patient(id=12, status_id=0)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_print_message = MagicMock()
    command_handlers.status_down(patient_id=12)
    patient = hospital._get_patient_by_id(patient_id=12)
    assert patient.status_id == 0
    dialogue.user_print_message.assert_called_once_with('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')


def test_handler_discharge(capsys):
    hospital = Hospital(patients=[Patient(id=10, status_id=1)])
    dialogue = Dialogue()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    dialogue.user_print_message = MagicMock()
    command_handlers.discharge(patient_id=10)
    assert hospital._get_patient_by_id(10) is None
    dialogue.user_print_message.assert_called_once_with('Пациент выписан из больницы')
