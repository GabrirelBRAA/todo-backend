from enum import Enum

class UserRole(int, Enum):
    NORMAL = 0
    ADMIN = 1
    SUPERADMIN = 2
