from model import Restaurant, MenuList, MenuItemList, TableList, Users
from enums import MenuType, UserRole

class UserDataProvider:
    def __init__(self):
        self.__user_list = []
        self._create_user_list()

    def _create_user_list(self):
        user1 = Users("1","1", UserRole.ADMIN)
        user2 = Users("2","2", UserRole.EMPLOYEE)
        user3 = Users("3","3", UserRole.INTERN)
        self.__user_list.append(user1)
        self.__user_list.append(user2)
        self.__user_list.append(user3)

    @property
    def user_list(self):
        return self.__user_list

class DataProvider:
    def __init__(self):
        self.__restaurants = []
        self._create_restaurant_list()

    def _create_restaurant_list(self):
        # Create Restaurant 1 and menu list
        restaurant1_menu_list = self._create_restaurant1_menu_list()
        restaurant1 = Restaurant("Restaurant #1", "Address #1", restaurant1_menu_list, self.table_list1())

        # Create Restaurant 2 and menu list
        restaurant2_menu_list = self._create_restaurant2_menu_list()
        restaurant2 = Restaurant("Restaurant #2", "Address #2", restaurant2_menu_list, self.table_list2())

        # Create Restaurant 3 and menu list
        restaurant3_menu_list = self._create_restaurant3_menu_list()
        restaurant3 = Restaurant("Restaurant #3", "Address #3", restaurant3_menu_list, self.table_list3())
        
        # Add Restaurants in the list
        self.__restaurants.append(restaurant1)
        self.__restaurants.append(restaurant2)
        self.__restaurants.append(restaurant3)

    def _create_restaurant1_menu_list(self):
        menu_list = []
        menu_list.append(MenuList("Menu #1", self.menu_item_list1()))
        menu_list.append(MenuList("Menu #2", self.menu_item_list2()))
        menu_list.append(MenuList("Menu #3", self.menu_item_list3()))
        menu_list.append(MenuList("Menu #4", self.menu_item_list1()))
        menu_list.append(MenuList("Menu #5", self.menu_item_list2()))

        return menu_list
    
    def _create_restaurant2_menu_list(self):
        menu_list = []
        menu_list.append(MenuList("Menu #6", self.menu_item_list1()))
        menu_list.append(MenuList("Menu #7", self.menu_item_list2()))
        menu_list.append(MenuList("Menu #8", self.menu_item_list3()))
        menu_list.append(MenuList("Menu #9", self.menu_item_list1()))
        menu_list.append(MenuList("Menu #10", self.menu_item_list2()))

        return menu_list
    
    def _create_restaurant3_menu_list(self):
        menu_list = []
        menu_list.append(MenuList("Menu #11", self.menu_item_list1()))
        menu_list.append(MenuList("Menu #12", self.menu_item_list2()))
        menu_list.append(MenuList("Menu #13", self.menu_item_list3()))

        return menu_list
    
    def menu_item_list1(self):
        menu_item_list = []
        menu_item_list.append(MenuItemList(100, "Meal #1", 3.00, MenuType.MEAL))
        menu_item_list.append(MenuItemList(101, "Meal #2", 6.00, MenuType.MEAL))
        menu_item_list.append(MenuItemList(200, "Drink #1", 2.00, MenuType.DRINK))

        return menu_item_list
    
    def menu_item_list2(self):
        menu_item_list = []
        menu_item_list.append(MenuItemList(100, "Meal #1", 3.00, MenuType.MEAL))
        menu_item_list.append(MenuItemList(101, "Meal #2", 6.00, MenuType.MEAL))
        menu_item_list.append(MenuItemList(200, "Drink #1", 2.00, MenuType.DRINK))
        menu_item_list.append(MenuItemList(201, "Drink #2", 4.00, MenuType.DRINK))

        return menu_item_list
    
    def menu_item_list3(self):
        menu_item_list = []
        menu_item_list.append(MenuItemList(100, "Meal #1", 3.00, MenuType.MEAL))
        menu_item_list.append(MenuItemList(200, "Drink #1", 2.00, MenuType.DRINK))

        return menu_item_list
    
    def table_list1(self):
        table_list = []
        table_list.append(TableList(1,4))
        table_list.append(TableList(2,5))
        table_list.append(TableList(3,6))

        return table_list
    
    def table_list2(self):
        table_list = []
        table_list.append(TableList(7,10))
        table_list.append(TableList(8,11))
        table_list.append(TableList(9,12))

        return table_list
    
    def table_list3(self):
        table_list = []
        table_list.append(TableList(13,16))
        table_list.append(TableList(14,17))
        table_list.append(TableList(15,18))

        return table_list
    
    @property
    def restaurants_list(self):
        return self.__restaurants