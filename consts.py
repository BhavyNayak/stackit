from enum import Enum

class UserTypeEnum(str, Enum):
    guest = "guest"
    user = "user"
    admin = "admin"


