from commands import Commands


class Application:
    def __init__(self, dialogue, command_handlers):
        self._dialogue = dialogue

        self._command_handlers = command_handlers

    def main(self):
        stop = False
        while not stop:
            command: Commands = self._dialogue.user_input_command()

            if not command.correct():
                self._dialogue.user_print_message('Неизвестная команда! Попробуйте ещё раз')
                continue

            if command.is_statistic():
                self._command_handlers.statistics()

            if command.is_stop():
                self._dialogue.user_print_message('Сеанс завершён.')
                break

            if command.is_discharge():
                self._command_handlers.discharge()

            if command.is_get_status():
                self._command_handlers.get_status()

            if command.is_down_status():
                self._command_handlers.status_down()

            if command.is_up_status():
                self._command_handlers.status_up()



