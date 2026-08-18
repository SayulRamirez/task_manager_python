from typing import Annotated

from fastapi import Depends

from config.auth_depends import RoleChecker
from models.user import Role, User


admin = RoleChecker([Role.ADMIN])
required_admin = Annotated[User, Depends(admin)]

user = RoleChecker([Role.USER])
required_user = Annotated[User, Depends(user)]
