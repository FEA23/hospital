
PATIENT_STATUSES = {
        0: 'Тяжело болен',
        1: 'Болен',
        2: 'Слегка болен',
        3: 'Готов к выписке'
}


class Patient:

    def __init__(self, id: int, status_id=1):
        self.id = id
        self.status_id = status_id

    @property
    def status_name(self):
        return PATIENT_STATUSES.get(self.status_id)
