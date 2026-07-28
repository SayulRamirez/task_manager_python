from datetime import date
from enum import Enum


class Status(Enum):
    PENDING = 'Pendiente'
    IN_PROGRESS = 'En progreso'
    COMPLETE = 'Completa'

class Project:
    
    def __init__(self, id: int, title: str, description: str, leader: int, status: str, estimated_completion: date):
        self.id = id
        self.title = title
        self.description = description
        self.leader = leader
        self.status = status
        self.estimated_completion = estimated_completion

