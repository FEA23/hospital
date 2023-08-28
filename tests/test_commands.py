from unittest.mock import MagicMock

from commands import Commands, CommandHandlers
from custom_exceptions import PatientIdNotIntegerAndPositiveError, PatientNotExistsError
from hospital import Hospital


def test_correct():
    commands = Commands('get status')
    assert commands.correct()


def test_not_correct():
    commands = Commands('show status')
    assert not commands.correct()


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


def test_handlers_get_status():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(return_value=2)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.get_status()
    command_handlers._dialogue.user_print_message.assert_called_with('Статус пациента: "Слегка болен"')


def test_handlers_get_status_not_integer():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.get_status()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')


def test_handlers_get_status_not_exists():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientNotExistsError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.get_status()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_down():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(return_value=2)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_down()
    command_handlers._dialogue.user_print_message.assert_called_with('Новый статус пациента: "Болен"')


def test_handlers_status_down_not_exists():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientNotExistsError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_down()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_handlers_status_down_not_integer():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_down()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')


def test_handler_discharge():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(return_value=2)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.discharge()
    command_handlers._dialogue.user_print_message.assert_called_with('Пациент выписан из больницы')


def test_handlers_discharge_not_integer():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.discharge()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')


def test_handlers_discharge_not_exists():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientNotExistsError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.discharge()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_status_up():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(return_value=1)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_up()
    command_handlers._dialogue.user_print_message.assert_called_with('Новый статус пациента: "Слегка болен"')


def test_processing_max_status_up_if_yes():
    hospital = Hospital([1, 3, 1])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(return_value=2)
    command_handlers._dialogue.user_input_need_discharge_patient = MagicMock(return_value=True)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_up()
    command_handlers._dialogue.user_print_message.assert_called_with('Пациент выписан из больницы')


def test_processing_max_status_up_if_not():
    hospital = Hospital([1, 3, 1])
    dialogue = MagicMock()
    cmd = CommandHandlers(hospital=hospital, dialogue=dialogue)
    cmd._dialogue.user_input_patient_id = MagicMock(return_value=2)
    cmd._dialogue.user_input_need_discharge_patient = MagicMock(return_value=False)
    cmd._dialogue.user_print_message = MagicMock()
    cmd.status_up()
    cmd._dialogue.user_print_message.assert_called_with('Пациент остался в статусе "Готов к выписке"')


def test_handlers_status_up_not_exists():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientNotExistsError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_up()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка. В больнице нет пациента с таким ID')


def test_handlers_status_up_not_integer():
    hospital = Hospital([1, 2, 3])
    dialogue = MagicMock()
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)
    command_handlers._dialogue.user_input_patient_id = MagicMock(side_effect=PatientIdNotIntegerAndPositiveError)
    command_handlers._dialogue.user_print_message = MagicMock()
    command_handlers.status_up()
    command_handlers._dialogue.user_print_message.assert_called_with('Ошибка ввода. ID пациента должно быть числом (целым, положительным)')