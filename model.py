class Users:
    def __init__(self, username, password, user_role):
        self.__username = username
        self.__password = password
        self.__user_role = user_role

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def user_role(self):
        return self.__user_role
    
    @user_role.setter
    def user_role(self, value):
        self.__user_role = value

class Restaurant:
    def __init__(self, restaurant_name, restaurant_address, menu_list, table_list):
        self.__restaurant_name = restaurant_name
        self.__restaurant_address = restaurant_address
        self.__menu_list = menu_list
        self.__table_list = table_list

    @property
    def restaurant_name(self):
        return self.__restaurant_name
    
    @restaurant_name.setter
    def restaurant_name(self, value):
        self.__restaurant_name = value

    @property
    def restaurant_address(self):
        return self.__restaurant_address
    
    @restaurant_address.setter
    def restaurant_address(self, value):
        self.__restaurant_address = value

    @property 
    def menu_list(self):
        return self.__menu_list
    
    @menu_list.setter
    def menu_list(self, value):
        self.__menu_list = value

    @property
    def table_list(self):
        return self.__table_list

    @table_list.setter
    def table_list(self, value):
        self.__table_list = value

class MenuList:
    def __init__(self, menu_name, menu_item_list):
        self.__menu_name = menu_name
        self.__menu_item_list = menu_item_list

    @property
    def menu_name(self):
        return self.__menu_name
    
    @menu_name.setter
    def menu_name(self, value):
        self.__menu_name = value

    @property
    def menu_item_list(self):
        return self.__menu_item_list

    @menu_item_list.setter
    def menu_item_list(self, value):
        self.__menu_item_list = value

class MenuItemList:
    def __init__(self, menu_item_id, menu_item_name, menu_item_price, menu_item_type):
        self.__menu_item_id = menu_item_id
        self.__menu_item_name = menu_item_name
        self.__menu_item_price = menu_item_price
        self.__menu_item_type = menu_item_type

    @property
    def menu_item_id(self):
        return self.__menu_item_id
    
    @menu_item_id.setter
    def menu_item_id(self, value):
        self.__menu_item_id = value

    @property
    def menu_item_name(self):
        return self.__menu_item_name
    
    @menu_item_name.setter
    def menu_item_name(self, value):
        self.__menu_item_name = value

    @property
    def menu_item_price(self):
        return self.__menu_item_price
    
    @menu_item_price.setter
    def menu_item_price(self, value):
        self.__menu_item_price = value

    @property
    def menu_item_type(self):
        return self.__menu_item_type
    
    @menu_item_type.setter
    def menu_item_type(self, value):
        self.__menu_item_type = value

class TableList:
    def __init__(self, table_id, seats):
        self.__table_id = table_id
        self.__seats = seats

    @property
    def table_id(self):
        return self.__table_id
    
    @table_id.setter
    def table_id(self, value):
        self.__table_id = value
    
    @property
    def seats(self):
        return self.__seats
    
    @seats.setter
    def seats(self, value):
        self.__seats = value