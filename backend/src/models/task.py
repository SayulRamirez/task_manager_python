from datetime import date


class Task:
    def __init__(self, id: int, title: str, description: str, id_responsible: int, status: str, project: int, estimated_delivery: date, priority: str, create_date: date):
        self.id = id
        self.title = title
        self.description = description
        self.id_responsible = id_responsible
        self.status = status
        self.project = project
        self.estimated_delivery = estimated_delivery
        self.priority = priority
        self.create_date = create_date