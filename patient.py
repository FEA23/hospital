
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
        self._max_status_id = max(PATIENT_STATUSES.keys())
        self._min_status_id = min(PATIENT_STATUSES.keys())

    def _set_status(self, new_status_id: int) -> None:
        self.status_id = new_status_id

    @property
    def status_name(self) -> str:
        return PATIENT_STATUSES.get(self.status_id)

    def status_up(self) -> bool:
        if self.status_id == self._max_status_id:
            return False
        else:
            self._set_status(self.status_id + 1)
            return True

    def status_down(self) -> bool:
        if self.status_id == self._min_status_id:
            return False
        else:
            self._set_status(self.status_id - 1)
            return True