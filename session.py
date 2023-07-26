from hospital import Hospital
from patient import IsMaxDiseaseStatus, IsMinDiseaseStatus
from commands import Commands


class Session:
    def __init__(self, hospital: Hospital):
        self.get_command = "Введите команду: "
        self.new_status = 'Новый статус пациента: {}'
        self.current_status = 'Статус пациента: {}'
        self.stay_in_status = 'Пациент остался в статусе "{}"'
        self.discharge = 'Пациент выписан из больницы'
        self.not_patient_id = 'Ошибка. В больнице нет пациента с таким ID'
        self.uncorrect_patient_id = 'Ошибка. ID пациента должно быть числом (целым, положительным)'
        self.discharge_the_client = 'Желаете этого клиента выписать? (да/нет): '
        self.get_patient_id = 'Введите ID пациента: '
        self.uncorrect_command = 'Неизвестная команда! Попробуйте ещё раз'
        self.min_status = 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'
        self.stop_session = 'Сеанс завершён.'
        self.hospital = hospital

    def input_patient_id(self):
        patient_id = input(self.get_patient_id)
        if patient_id.isdigit():
            return int(patient_id)
        else:
            print(self.uncorrect_patient_id)
            return None

    def discharge_input(self, patient_id):
        discharge_input = input(self.discharge_the_client)
        if discharge_input.lower() == 'да':
            self.hospital.discharge(patient_id)
            print(self.discharge)
        else:
            patient = self.hospital.get_patient_by_id(patient_id)
            print(self.stay_in_status.format(patient.status_name))

    def start(self):
        while True:
            user_command = input(self.get_command).lower()
            command = Commands(user_command)
            if not command.correct():
                print(self.uncorrect_patient_id)
                continue

            if command.is_statistic():
                print(self.hospital.calculate_statistics())
                continue

            if command.is_stop():
                print(self.stop_session)
                break

            patient_id = self.input_patient_id()
            if patient_id is None:
                continue

            patient = self.hospital.get_patient_by_id(patient_id)
            if patient is None:
                print(self.not_patient_id)
                continue

            if command.is_discharge():
                self.hospital.discharge(patient_id)
                print(self.discharge)
                continue

            if command.is_get_status():
                print(self.current_status.format(patient.status_name))
                continue

            if command.is_down_status():
                try:
                    patient.status_down()
                    print(self.new_status.format(patient.status_name))
                except IsMinDiseaseStatus:
                    print(self.min_status)
                continue

            if command.is_up_status():
                try:
                    patient.status_up()
                    print(self.new_status.format(patient.status_name))
                except IsMaxDiseaseStatus:
                    self.discharge_input(patient_id)

                continue
