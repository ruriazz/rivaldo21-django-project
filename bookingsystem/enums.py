from enum import Enum

class UserRoles(Enum):
    ADMIN = 'admin'
    DEPARTMENT_CHIEF = 'department_chief'
    DIRECTOR = "director"
    EXECUTIVE = 'executive'
    STAFF = 'staff'
    DRIVER = 'driver'  

    @staticmethod
    def choices():
        return [(role.value, role.value) for role in UserRoles]