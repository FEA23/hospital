

class Commands:
    GET_STATUS = ('узнать статус пациента', 'get status')
    STATUS_UP = ('повысить статус пациента', 'status up')
    STATUS_DOWN = ('понизить статус пациента', 'status down')
    DISCHARGE = ('выписать пациента', 'discharge')
    CALCULATE_STATISTICS = ('рассчитать статистику', 'calculate statistic')
    STOP = ('стоп', 'stop')

    def __init__(self, command: str):
        self.command = command
        self.commands = (
            self.GET_STATUS,
            self.STATUS_UP,
            self.STATUS_DOWN,
            self.DISCHARGE,
            self.CALCULATE_STATISTICS,
            self.STOP
        )

    def correct(self):
        for command_tuple in self.commands:
            if self.command in command_tuple:
                return True

        return False

    def is_get_status(self):
        return self.command in self.GET_STATUS

    def is_up_status(self):
        return self.command in self.STATUS_UP

    def is_down_status(self):
        return self.command in self.STATUS_DOWN

    def is_discharge(self):
        return self.command in self.DISCHARGE

    def is_statistic(self):
        return self.command in self.CALCULATE_STATISTICS

    def is_stop(self):
        return self.command in self.STOP


class CommandHandlers:

    def __init__(self, dialogue, hospital) -> None:
        self._dialogue = dialogue
        self._hospital = hospital

    def get_status(self, patient_id: int):
        patient_status_name = self._hospital.get_status_name_by_patient_id(patient_id)
        print('Статус пациента: {}'.format(patient_status_name))

    def discharge(self, patient_id: int):
        self._hospital.discharge(patient_id)
        print('Пациент выписан из больницы')

    def status_down(self, patient_id: int):
        patient, down_is_succesfully = self._hospital.patient_status_down(patient_id)
        if down_is_succesfully:
            print('Новый статус пациента: {}'.format(patient.status_name))
        else:
            print('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    def status_up(self, patient_id: int):
        patient, up_is_succesfully = self._hospital.patient_status_up(patient_id)
        if up_is_succesfully:
            print('Новый статус пациента: {}'.format(patient.status_name))
        else:
            need_discharge = self._dialogue.user_input_need_discharge_patient()
            if need_discharge:
                self.discharge(patient_id)
            else:
                print('Пациент остался в статусе "{}"'.format(patient.status_name))
