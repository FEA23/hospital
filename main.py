from hospital import Hospital
from dialogue import Dialogue
from commands import Commands, CommandHandlers

hospital = Hospital()
dialogue = Dialogue()

command_handlers = CommandHandlers(dialogue, hospital)

if __name__ == '__main__':
    while True:
        command: Commands = dialogue.user_input_main_command()

        if not command.correct():
            dialogue.user_print_message('Неизвестная команда! Попробуйте ещё раз')
            continue

        if command.is_statistic():
            command_handlers.calculate_statistic()

        if command.is_stop():
            dialogue.user_print_message('Сеанс завершён.')
            break

        patient_id = dialogue.user_input_patient_id()
        if patient_id is None:
            dialogue.user_print_message('Ошибка. ID пациента должно быть числом (целым, положительным)')
            continue

        #Надо будет убрать hospital
        if not hospital.patient_exists(patient_id):
            dialogue.user_print_message('Ошибка. В больнице нет пациента с таким ID')
            continue

        if command.is_discharge():
            command_handlers.discharge(patient_id)

        if command.is_get_status():
            command_handlers.get_status(patient_id)

        if command.is_down_status():
            command_handlers.status_down(patient_id)

        if command.is_up_status():
            command_handlers.status_up(patient_id)
