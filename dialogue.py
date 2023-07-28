from typing import Union

from hospital import Hospital
from commands import Commands
from patient import Patient


class Dialogue:
    def __init__(self, hospital: Hospital):
        self.hospital = hospital

        self.main_command_text_for_user = 'Введите команду: '
        self.discharge_question_for_user = 'Желаете этого клиента выписать? (да/нет): '
        self.patient_id_text_for_user = 'Введите ID пациента: '

    def _format_user_response(self, command_for_user: str) -> str:
        user_answer = input(command_for_user)
        return user_answer.lower().strip()   

    def user_input_patient_id(self) -> Union[Patient, None]:
        patient_id = self._format_user_response(self.patient_id_text_for_user)
        if patient_id.isdigit():
            return int(patient_id)

        return None

    def user_input_need_discharge_patient(self) -> Union[Patient, None]:
        need_discharge = self._format_user_response(self.discharge_question_for_user)
        return True if need_discharge == 'да' else False
    
    def user_input_main_command(self) -> Commands:
        command = self._format_user_response(self.main_command_text_for_user)
        command = Commands(command)
        return command
    