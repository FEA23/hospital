
class IsMaxDiseaseStatus(Exception):
    pass


class IsMinDiseaseStatus(Exception):
    pass


class Patient:
    STATUSES = {
        0: 'Тяжело болен',
        1: 'Болен',
        2: 'Слегка болен',
        3: 'Готов к выписке'
    }

    def __init__(self, patient_id: int):
        self.id = patient_id
        self.status_id = 1
        self.status_name = self.STATUSES.get(self.status_id)
        self.max_status_id = max(self.STATUSES.keys())
        self.min_status_id = min(self.STATUSES.keys())

    def set_status_id(self, new_status_id: int):
        if new_status_id > self.max_status_id:
            raise IsMaxDiseaseStatus()

        if new_status_id < self.min_status_id:
            raise IsMinDiseaseStatus()

        self.status_id = new_status_id

    def set_status_name(self, new_status_name: str):
        self.status_name = new_status_name

    def status_up(self):
        new_status_id = self.status_id + 1
        self.set_status_id(new_status_id)
        self.set_status_name(self.STATUSES.get(new_status_id))

    def status_down(self):
        new_status_id = self.status_id - 1
        self.set_status_id(new_status_id)
        self.set_status_name(self.STATUSES.get(new_status_id))
