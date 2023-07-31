from patient import Patient, PATIENT_STATUSES


class Hospital:
    _PATIENTS = [Patient(i) for i in range(1, 201)]

    def get_patient_by_id(self, id: int) -> Patient or None:
        for patient in self._PATIENTS:
            if patient.id == id:
                return patient
        return None

    def discharge(self, patient_id):
        patient = self.get_patient_by_id(patient_id)
        if patient is not None and patient in self._PATIENTS:
            return self._PATIENTS.remove(patient)

    def calculate_statistics(self):
        status_count = {0: 0, 1: 0, 2: 0, 3: 0}
        for patient in self._PATIENTS:
            status_count[patient.status_id] += 1

        statistics = f'В больнице на данный момент находится {len(self._PATIENTS)} чел., из них:\n'
        for status_code, count in status_count.items():
            if count > 0:
                statistics += f'- в статусе "{PATIENT_STATUSES[status_code]}": {count} чел.\n'

        return statistics