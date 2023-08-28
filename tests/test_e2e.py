from application import Application
from commands import CommandHandlers
from dialogue import Dialogue
from hospital import Hospital
from mock_console import MockConsole


def make_application(hospital, console):
    dialogue = Dialogue(console)
    command_handlers = CommandHandlers(hospital, dialogue)
    app = Application(dialogue, command_handlers)
    return app


def test_positive_scenario():
    hospital = Hospital([1, 1, 0, 2, 1])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    console.add_expected_output_message('Статус пациента: "Тяжело болен"')

    console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '1')
    console.add_expected_output_message('Новый статус пациента: "Слегка болен"')

    console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_output_message('Новый статус пациента: "Тяжело болен"')

    console.add_expected_request_and_response('Введите команду: ', 'рассчитать статистику')
    console.add_expected_output_message("В больнице на данный момент находится 5 чел., из них:\n" +
        "\t- в статусе \"Тяжело болен\": 2 чел.\n" +
        "\t- в статусе \"Болен\": 1 чел.\n" +
        "\t- в статусе \"Слегка болен\": 2 чел.\n" +
        "\t- в статусе \"Готов к выписке\": 0 чел.")

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(hospital, console)

    app.main()

    console.verify_all_calls_have_been_made()
    assert hospital._patients == [2, 0, 0, 2, 1]


def test_discharge_patient():
    hospital = Hospital([1, 2, 3, 0])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'discharge')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_output_message('Пациент выписан из больницы')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(hospital, console)

    app.main()

    console.verify_all_calls_have_been_made()
    assert hospital._patients == [1, 3, 0]


def test_unknown_command():
    hospital = Hospital([1, 2, 3])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'неизвестная команда')
    console.add_expected_output_message('Неизвестная команда! Попробуйте ещё раз')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(hospital, console)

    app.main()

    console.verify_all_calls_have_been_made()


def test_work_patient_statuses():
    hospital = Hospital([1, 0, 3, 1, 3])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'status down')
    console.add_expected_request_and_response('Введите ID пациента: ', '1')
    console.add_expected_output_message('Новый статус пациента: "Тяжело болен"')

    console.add_expected_request_and_response('Введите команду: ', 'status down')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_output_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    console.add_expected_request_and_response('Введите команду: ', 'status up')
    console.add_expected_request_and_response('Введите ID пациента: ', '4')
    console.add_expected_output_message('Новый статус пациента: "Слегка болен"')

    console.add_expected_request_and_response('Введите команду: ', 'status up')
    console.add_expected_request_and_response('Введите ID пациента: ', '5')
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'Нет')
    console.add_expected_output_message('Пациент остался в статусе "Готов к выписке"')

    console.add_expected_request_and_response('Введите команду: ', 'status up')
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'Да')
    console.add_expected_output_message('Пациент выписан из больницы')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(hospital, console)

    app.main()

    console.verify_all_calls_have_been_made()
    assert hospital._patients == [0, 0, 2, 3]

