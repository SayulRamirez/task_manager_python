from dto.project_dto import CreateProject
from models.project import Project


class ProjectRepository:
    __proyects: list[Project] = []
    __id_count = 0

    def save(self, request: CreateProject):
        self.__id_count += 1
        self.__proyects.append(Project(id=self.__id_count,
                                       status='PENDING',
                                       **request.model_dump()))

    def find_by_id(self, id):
        for proyect in self.__proyects:
            if proyect.id == id:
                return proyect
        return None
    
    def get_all(self, id_leader):
        return [proyect for proyect in self.__proyects if proyect.leader == id_leader]

    def changed_status(self, id, status):
        proyect = self.find_by_id(id)

        if proyect:
            proyect.status = status
            return proyect
        return None
    
    def deleted(self, id):
        for proyect in self.__proyects:
            if proyect.id == id:
                self.__proyects.remove(proyect)
                return True
        return False