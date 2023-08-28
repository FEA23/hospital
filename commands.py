from custom_exceptions import PatientNotExistsError, PatientIdNotIntegerAndPositiveError, MinStatusCannotDownError


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
    def __init__(self, hospital, dialogue):
        self._hospital = hospital
        self._dialogue = dialogue

    def get_status(self):
        try:
            patient_id = self._dialogue.user_input_patient_id()
            patient_status = self._hospital.get_status_by_patient_id(patient_id)
            self._dialogue.user_print_message(f'Статус пациента: "{patient_status}"')
        except (PatientNotExistsError, PatientIdNotIntegerAndPositiveError) as err:
            self._dialogue.user_print_message(str(err))

    def status_down(self):
        try:
            patient_id = self._dialogue.user_input_patient_id()
            self._hospital.status_down(patient_id)
            new_status = self._hospital.get_status_by_patient_id(patient_id)
            self._dialogue.user_print_message(f'Новый статус пациента: "{new_status}"')
        except (PatientNotExistsError, PatientIdNotIntegerAndPositiveError, MinStatusCannotDownError) as err:
            self._dialogue.user_print_message(str(err))

    def discharge(self):
        try:
            patient_id = self._dialogue.user_input_patient_id()
            self._hospital.discharge(patient_id)
            self._dialogue.user_print_message('Пациент выписан из больницы')
        except (PatientNotExistsError, PatientIdNotIntegerAndPositiveError) as err:
            self._dialogue.user_print_message(str(err))

    def status_up(self):
        try:
            patient_id = self._dialogue.user_input_patient_id()
            if self._hospital.can_status_up(patient_id):
                self._hospital.status_up(patient_id)
                new_status = self._hospital.get_status_by_patient_id(patient_id)
                self._dialogue.user_print_message(f'Новый статус пациента: "{new_status}"')
            else:
                need_discharge = self._dialogue.user_input_need_discharge_patient()
                if need_discharge:
                    self._hospital.discharge(patient_id)
                    self._dialogue.user_print_message('Пациент выписан из больницы')
                else:
                    self._dialogue.user_print_message('Пациент остался в статусе "Готов к выписке"')
        except (PatientNotExistsError, PatientIdNotIntegerAndPositiveError) as err:
            self._dialogue.user_print_message(str(err))

    def statistics(self):
        formatted_statistics = self._hospital.format_patient_statistics()
        self._dialogue.user_print_message(formatted_statistics)