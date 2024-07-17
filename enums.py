from enum import Enum

class UserRole:
    ADMIN = 1,
    EMPLOYEE = 2,
    INTERN = 3

class MenuType(Enum):
    MEAL = 1
    DRINK = 2

class UserFeatures(Enum):
    RESTAURANT_MANAGER = 1,
    MENU_MANAGER = 2,
    MENU_ITEM_MANAGER = 3,
    TABLE_MANAGER = 4,
    SIGN_OUT = 5

