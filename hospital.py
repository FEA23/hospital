from custom_exceptions import MaxStatusCannotUpError, MinStatusCannotDownError, PatientNotExistsError


class Hospital:

    def __init__(self, patients=None):

        if patients:
            self._patients = patients
        else:
            self._patients = [1 for x in range(200)]

        self.status = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    def get_status_by_patient_id(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        status_code = self._patients[patient_id - 1]
        return self.status.get(status_code)

    def status_up(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        if not self.can_status_up(patient_id):
            raise MaxStatusCannotUpError
        current_status = self._patients[patient_id - 1]
        new_status = current_status + 1
        self._patients[patient_id - 1] = new_status
        return new_status

    def status_down(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        if not self.can_status_down(patient_id):
            raise MinStatusCannotDownError
        current_status = self._patients[patient_id - 1]
        new_status = current_status - 1
        self._patients[patient_id - 1] = new_status
        return new_status

    def discharge(self, patient_id: int):
        return self._patients.pop(patient_id - 1)

    def _statistics(self):
        status_count = {status: 0 for status in self.status.values()}
        total_patients = 0

        for patient_status_code in self._patients:
            status_text = self.status[patient_status_code]
            status_count[status_text] += 1
            total_patients += 1

        return {"status_count": status_count, "total_patients": total_patients}

    def format_patient_statistics(self):
        statistics = self._statistics()
        total_patients = statistics["total_patients"]
        status_counts = statistics["status_count"]

        output = f"В больнице на данный момент находится {total_patients} чел., из них:"
        for status, count in status_counts.items():
            output += f"\n\t- в статусе \"{status}\": {count} чел."

        return output

    def can_status_up(self, patient_id: int):
        status = self.get_status_by_patient_id(patient_id)
        return status != "Готов к выписке"

    def can_status_down(self, patient_id: int):
        status = self.get_status_by_patient_id(patient_id)
        return status != "Тяжело болен"

    def patient_exists(self, patient_id):
        return patient_id <= len(self._patients)

    def _verify_patient_exists(self, patient_id):
        if not self.patient_exists(patient_id):
            raise PatientNotExistsError
