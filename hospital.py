from patient import Patient, PATIENT_STATUSES


class Hospital:
    PATIENTS = [Patient(i) for i in range(1, 201)]

    def get_patient_by_id(self, id: int) -> Patient or None:
        for patient in self.PATIENTS:
            if patient.id == id:
                return patient
        return None

    def discharge(self, patient_id):
        patient = self.get_patient_by_id(patient_id)
        if patient is not None and patient in self.PATIENTS:
            return self.PATIENTS.remove(patient)

    def calculate_statistics(self):
        status_count = {0: 0, 1: 0, 2: 0, 3: 0}
        for patient in self.PATIENTS:
            status_count[patient.status_id] += 1

        return status_count

    def display_statistics(self):
        status_count = self.calculate_statistics()

        statistics = f'В больнице на данный момент находится {len(self.PATIENTS)} чел., из них:\n'
        for status_code, count in status_count.items():
            if count > 0:
                statistics += f'- в статусе "{PATIENT_STATUSES[status_code]}": {count} чел.\n'

        return statistics