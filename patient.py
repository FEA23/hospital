
PATIENT_STATUSES = {
        0: 'Тяжело болен',
        1: 'Болен',
        2: 'Слегка болен',
        3: 'Готов к выписке'
}


class Patient:

    def __init__(self, patient_id: int):
        self.id = patient_id
        self.status_id = 1
        self.status_name = PATIENT_STATUSES.get(self.status_id)
        self.max_status_id = max(PATIENT_STATUSES.keys())
        self.min_status_id = min(PATIENT_STATUSES.keys())

    def _set_status(self, new_status_id: int) -> None:
        self.status_id = new_status_id
        self.status_name = PATIENT_STATUSES.get(new_status_id)

    def status_up(self) -> bool:
        status_up_succesfully = False

        new_status_id = self.status_id + 1
        if new_status_id <= self.max_status_id:
            self._set_status(new_status_id)
            status_up_succesfully = True

        return status_up_succesfully

    def status_down(self) -> bool:
        status_down_succesfully = False

        new_status_id = self.status_id - 1
        if new_status_id >= self.min_status_id:
            self._set_status(new_status_id)
            status_down_succesfully = True

        return status_down_succesfully