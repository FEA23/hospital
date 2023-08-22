from commands import Commands
from custom_exceptions import PatientIdNotIntegerAndPositiveError


class Dialogue:
    def __init__(self, console):
        self._console = console
        self._main_command_text_for_user = 'Введите команду: '
        self._discharge_question_for_user = 'Желаете этого клиента выписать? (да/нет): '
        self._patient_id_text_for_user = 'Введите ID пациента: '

    def _format_user_response(self, command_for_user: str) -> str:
        user_answer = self._console.input_user(command_for_user)
        return user_answer.lower().strip()   

    def user_print_message(self, message):
        self._console.print_user(message)

    def user_input_patient_id(self) -> int:
        patient_id = self._format_user_response(self._patient_id_text_for_user)
        if not patient_id.isdigit():
            raise PatientIdNotIntegerAndPositiveError

        return int(patient_id)

    def user_input_need_discharge_patient(self) -> bool:
        need_discharge = self._format_user_response(self._discharge_question_for_user)
        return need_discharge == 'да'
    
    def user_input_main_command(self) -> Commands:
        command = self._format_user_response(self._main_command_text_for_user)
        command = Commands(command)
        return command


