from hospital import Hospital
from dialogue import Dialogue
from commands import Commands, CommandHandlers
from console import Console

hospital = Hospital()
dialogue = Dialogue(Console)

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

        if command.is_discharge():
            command_handlers.discharge()

        if command.is_get_status():
            command_handlers.get_status()

        if command.is_down_status():
            command_handlers.status_down()

        if command.is_up_status():
            command_handlers.status_up()
