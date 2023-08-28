from unittest.mock import MagicMock

import pytest

from custom_exceptions import PatientIdNotIntegerAndPositiveError
from dialogue import Dialogue
from mock_console import MockConsole


def test_format_user_response():
    console = MagicMock()
    dialogue = Dialogue(console)
    command_for_user = 'Введите команду:'
    expected_answer = 'Ответ'
    console.input.return_value = expected_answer
    result = dialogue._format_user_response(command_for_user)
    assert result == expected_answer.lower().strip()
    console.input.assert_called_once_with(command_for_user)


def test_user_print_message():
    console = MagicMock()
    dialogue = Dialogue(console)
    message = 'get status'
    dialogue.user_print_message(message)
    console.print.assert_called_once_with(message)


def test_user_input_patient_id():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', '10')
    dialogue = Dialogue(console)
    assert dialogue.user_input_patient_id() == 10


def test_negative_user_input_patient_id():
    console = MockConsole()
    console.add_expected_request_and_response('Введите ID пациента: ', 'abc')
    dialogue = Dialogue(console)
    with pytest.raises(PatientIdNotIntegerAndPositiveError) as err:
        dialogue.user_input_patient_id()
    assert str(err.value) == 'Ошибка ввода. ID пациента должно быть числом (целым, положительным)'


def test_user_input_need_discharge_patient():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'Да')
    dialogue = Dialogue(console)
    assert dialogue.user_input_need_discharge_patient()


def test_negative_user_input_need_discharge_patient():
    console = MockConsole()
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'Нет')
    dialogue = Dialogue(console)
    assert not dialogue.user_input_need_discharge_patient()


def test_user_input_command():
    console = MagicMock()
    dialogue = Dialogue(console)
    dialogue._format_user_response = MagicMock(return_value='get status')
    result = dialogue.user_input_command()
    dialogue._format_user_response.assert_called_once_with(dialogue._main_command_text_for_user)
    assert result.command == 'get status'
