from typing import Union
from patient import Patient, PATIENT_STATUSES
from custom_exceptions import MinStatusCannotDownError, MaxStatusCannotUpError, PatientNotExistsError


class Hospital:
    def __init__(self, patients=None):
        if patients:
            self._patients = patients
        else:
            self._patients = [Patient(i) for i in range(1, 201)]

        self._max_status_id = max(PATIENT_STATUSES.keys())
        self._min_status_id = min(PATIENT_STATUSES.keys())

    def _get_patient_by_id(self, patient_id: int) -> Patient or None:
        for patient in self._patients:
            if patient.id == patient_id:
                return patient
        return None

    def get_status_name_by_patient_id(self, patient_id: int) -> Union[str, None]:
        self._verify_patient_exists(patient_id)
        patient = self._get_patient_by_id(patient_id)
        return patient.status_name if patient else None

    def can_status_down(self, patient_id: int) -> bool:
        patient = self._get_patient_by_id(patient_id)
        return patient.status_id > self._min_status_id

    def patient_status_down(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        if not self.can_status_down(patient_id):
            raise MinStatusCannotDownError
        patient = self._get_patient_by_id(patient_id)
        patient.status_id -= 1

    def can_status_up(self, patient_id: int) -> bool:
        patient = self._get_patient_by_id(patient_id)
        return patient.status_id < self._max_status_id

    def patient_status_up(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        if not self.can_status_up(patient_id):
            raise MaxStatusCannotUpError
        patient = self._get_patient_by_id(patient_id)
        patient.status_id += 1

    def discharge(self, patient_id: int):
        self._verify_patient_exists(patient_id)
        patient = self._get_patient_by_id(patient_id)
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

    def patient_exists(self, patient_id):
        patient = self._get_patient_by_id(patient_id)
        return patient is not None

    def _verify_patient_exists(self, patient_id):
        if not self.patient_exists(patient_id):
            raise PatientNotExistsError
