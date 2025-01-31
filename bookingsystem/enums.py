from enum import Enum

class UserRoles(Enum):
    ADMIN = 'admin'
    DRIVER = 'driver'
    EXECUTIVE = 'executive'

    @staticmethod
    def choices():
        return [(role.value, role.value) for role in UserRoles]