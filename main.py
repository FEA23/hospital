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
            print('Неизвестная команда! Попробуйте ещё раз')
            continue

        if command.is_statistic():
            hospital_stats = hospital.display_statistics()
            print(hospital_stats)
            continue

        if command.is_stop():
            print('Сеанс завершён.')
            break

        patient_id = dialogue.user_input_patient_id()
        if patient_id is None:
            print('Ошибка. ID пациента должно быть числом (целым, положительным)')
            continue

        patient = hospital.get_patient_by_id(patient_id)
        if not patient:
            print('Ошибка. В больнице нет пациента с таким ID')
            continue

        if command.is_discharge():
            command_handlers.discharge(patient_id)

        if command.is_get_status():
            command_handlers.get_status(patient_id)

        if command.is_down_status():
            command_handlers.status_down(patient_id)

        if command.is_up_status():
            command_handlers.status_up(patient_id)
