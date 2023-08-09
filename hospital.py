from typing import Tuple

from patient import Patient, PATIENT_STATUSES


class Hospital:
    def __init__(self, patients=None):
        if patients:
            self._patients = patients
        else:
            self._patients = [Patient(i) for i in range(1, 201)]

        self._max_status_id = max(PATIENT_STATUSES.keys())
        self._min_status_id = min(PATIENT_STATUSES.keys())

    def get_patient_by_id(self, patient_id: int) -> Patient or None:
        for patient in self._patients:
            if patient.id == patient_id:
                return patient
        return None

    def get_status_name_by_patient_id(self, patient_id: int) -> str:
        patient = self.get_patient_by_id(patient_id)
        return patient.status_name if patient else None

    def patient_status_down(self, patient_id: int) -> Tuple[Patient, bool]:
        patient = self.get_patient_by_id(patient_id)
        if patient.status_id <= self._min_status_id:
            return patient, False
        else:
            patient.status_id -= 1
            return patient, True

    def patient_status_up(self, patient_id: int) -> Tuple[Patient, bool]:
        patient = self.get_patient_by_id(patient_id)
        if patient.status_id >= self._max_status_id:
            return patient, False
        else:
            patient.status_id += 1
            return patient, True

    def discharge(self, patient_id):
        patient = self.get_patient_by_id(patient_id)
        if patient in self._patients:
            self._patients.remove(patient)

    def _calculate_statistics(self) -> dict:
        status_count = {0: 0, 1: 0, 2: 0, 3: 0}
        for patient in self._patients:
            status_count[patient.status_id] += 1

        return status_count

    def _statistics_to_str(self, status_count: dict) -> str:
        statistics = f'В больнице на данный момент находится {len(self._patients)} чел., из них:\n'
        for status_code, count in status_count.items():
            if count > 0:
                statistics += f'- в статусе "{PATIENT_STATUSES[status_code]}": {count} чел.\n'

        return statistics

    def display_statistics(self) -> str:
        status_count = self._calculate_statistics()
        str_stats = self._statistics_to_str(status_count)
        return str_stats
