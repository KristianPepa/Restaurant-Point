from model import Restaurant, MenuList, MenuItemList, TableList
from enums import MenuType
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import psycopg2

class RestaurantManagerController:

    def add_restaurant(self, restaurants, restaurant_data):
        restaurants_list = restaurants
        new_restaurant = Restaurant(
            restaurant_data[0],
            restaurant_data[1],
            [],
            []
        )

        restaurants_list.append(new_restaurant)
        restaurants = restaurants_list

    def update_restaurant(self, restaurants, new_data, old_data):
        restaurants_list = restaurants

        for restaurant in restaurants_list:
            if restaurant.restaurant_name == old_data[0]:
                restaurant.restaurant_name = new_data[0]
                restaurant.restaurant_address = new_data[1]
        restaurants = restaurants_list
        
    def delete_restaurant(self, restaurants, restaurant_to_delete):
        restaurants_list = restaurants

        for restaurant in restaurants_list:
            if restaurant.restaurant_name == restaurant_to_delete[0]:
                restaurants_list.remove(restaurant_to_delete)
                restaurants = restaurants_list
                break

class MenuManagerController:
    def add_menu(self, menus, menu_data):
        menu_list = menus

        new_menu = MenuList(
            menu_data[0],
            []
        )

        menu_list.append(new_menu)
        menus = menu_list

    def update_menu(self, menus, menu_data):
        menu_list = menus

        for menu in menu_list:
            if menu.menu_name == menu_data[0]:
                menu.menu_name = menu_data[0]
        
    def delete_menu(self, menus, menu_to_delete):
        menu_list = menus

        for menu in menu_list:
            if menu.menu_name == menu_to_delete[0]:
                menu_list.remove(menu)
                menus = menu_list
                break

class MenuItemManagerController:
    def add_menu_item(self, menu_item_list, new_menu_item):
        item_list = menu_item_list

        new_menu = MenuItemList(
            new_menu_item[0],
            new_menu_item[1],
            new_menu_item[2],
            new_menu_item[3]
        )

        item_list.append(new_menu)
        menu_item_list = item_list

    def update_menu_item(self, menu_item_list, new_menu_item):
        item_list = menu_item_list

        for menu in item_list:
            if menu.menu_item_id == new_menu_item[0]:
                menu.menu_item_id = new_menu_item[0]
                menu.menu_item_name = new_menu_item[1]
                menu.menu_item_price = new_menu_item[2]
                menu.menu_item_type = new_menu_item[3]

    def delete_menu_item(self, menu_item_list, menu_to_delete):
        item_list = menu_item_list

        for item in item_list:
            if item.menu_item_id == menu_to_delete[0]:
                item_list.remove(item)
                menu_item_list = item_list
                break

class TableListController:

    def add_table(self, table_list, new_data):
        tables = table_list

        new_table = TableList(
            new_data[0],
            new_data[1]
        )

        tables.append(new_table)
        table_list = tables

    def update_table(self, table_list, new_data):
        tables = table_list

        for table in tables:
            if table.table_id == new_data[0]:
                table.table_id = new_data[0]
                table.seats = new_data[1]

    def delete_table(self, table_list, table_to_delete):
        tables = table_list

        for table in tables:
            if table.table_id == table_to_delete[0]:
                tables.remove(table)
                table_list = tables
                break

class RestaurantDatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname = dbname,
            user = user,
            password = password,
            host = host,
            port = port
        )

        self.cursor = self.conn.cursor()

    def create_table(self):
        create_restaurants_table_query = "CREATE TABLE IF NOT EXISTS restaurants ( id SERIAL PRIMARY KEY, name VARCHAR(30), address VARCHAR(30))"
        self.cursor.execute(create_restaurants_table_query)
        self.conn.commit()

        create_menus_table_query = "CREATE TABLE IF NOT EXISTS menus ( id SERIAL PRIMARY KEY, name VARCHAR(20), res_fk INT REFERENCES restaurants(id))"
        self.cursor.execute(create_menus_table_query)
        self.conn.commit()
        
        create_items_table_query = "CREATE TABLE IF NOT EXISTS items ( id SERIAL PRIMARY KEY, menu_id VARCHAR(20), name VARCHAR(20), price VARCHAR(20), type VARCHAR(20), menu_fk INT REFERENCES menus(id))"
        self.cursor.execute(create_items_table_query)
        self.conn.commit()
        
        create_tables_table_query = "CREATE TABLE IF NOT EXISTS tables ( id SERIAL PRIMARY KEY, table_id VARCHAR(20), seats VARCHAR(20), res_fk INT REFERENCES restaurants(id))"
        self.cursor.execute(create_tables_table_query)
        self.conn.commit()

    def create_restaurant(self, restaurant_name, restaurant_address):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            print("Restaurant already exists")
        else:
            query = f"INSERT INTO restaurants (name, address) VALUES ('{restaurant_name}', '{restaurant_address}')"
            self.cursor.execute(query)
            self.conn.commit()


    def create_menus(self, restaurant_name, menu_name):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]

            sql = f"SELECT id FROM menus WHERE name = '{menu_name}'"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                print("Menu already exists for this restaurant!")
            else:
                query = f"INSERT INTO menus (name, res_fk) VALUES ('{menu_name}', '{restaurant_id}')"
                self.cursor.execute(query)
                self.conn.commit()

        else:
            print("Restaurant not found!")

    def create_menu_items(self, restaurant_name, selected_menu_name, menu_item_id, menu_item_name, menu_item_price, menu_item_type):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            sql = f"SELECT id FROM menus WHERE name = '{selected_menu_name}'"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                menu_id = menu_result[0]

                sql = f"SELECT id FROM items WHERE name = '{menu_item_name}'"
                self.cursor.execute(sql)
                menu_item_result = self.cursor.fetchone()

                if menu_item_result:
                    print("Menu item already exists.")
                else:
                    query = f"INSERT INTO items (menu_id, name, price, type, menu_fk) VALUES ({menu_item_id}, '{menu_item_name}', {menu_item_price}, '{menu_item_type}', '{menu_id}')"
                    self.cursor.execute(query)
                    self.conn.commit()
            else:
                print("Menu not found!")
        else:
            print("Restaurant not found!")

    def create_table_items(self, restaurant_name, table_id, table_name):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]

            sql = f"SELECT id FROM tables WHERE seats = '{table_name}'"
            self.cursor.execute(sql)
            table_results = self.cursor.fetchone()

            if table_results:
                print("Table already exists")
            else:
                query = f"INSERT INTO tables (table_id, seats, res_fk) VALUES ({table_id}, '{table_name}', '{restaurant_id}')"
                self.cursor.execute(query)
                self.conn.commit()

                print("Table created successfully")
        else:
            print("Restaurant not found")

    def create_restaurants(self):
        self.create_restaurant("Restaurant #1", "Address #1")
        self.create_restaurant("Restaurant #2", "Address #2")
        self.create_restaurant("Restaurant #3", "Address #3")

    def create_menu_for_restaurant(self):
        self.create_menus("Restaurant #1", "Menu #1")
        self.create_menus("Restaurant #1", "Menu #2")
        self.create_menus("Restaurant #1", "Menu #3")

        self.create_menus("Restaurant #2", "Menu #4")
        self.create_menus("Restaurant #2", "Menu #5")
        self.create_menus("Restaurant #2", "Menu #6")

        self.create_menus("Restaurant #3", "Menu #7")
        self.create_menus("Restaurant #3", "Menu #8")
        self.create_menus("Restaurant #3", "Menu #9")
    
    def create_menu_item_for_restaurant(self):
        self.create_menu_items("Restaurant #1", "Menu #1", 100, "Meal #1", "3.0", MenuType.MEAL.value)
        self.create_menu_items("Restaurant #1", "Menu #1", 200, "Drink #1", "5.0", MenuType.DRINK.value)
        
        self.create_menu_items("Restaurant #1", "Menu #2", 200, "Drink #2", "5.0", MenuType.DRINK.value)
        self.create_menu_items("Restaurant #1", "Menu #2", 100, "Meal #2", "3.0", MenuType.MEAL.value)
        
        self.create_menu_items("Restaurant #2", "Menu #4", 100, "Meal #3", "3.0", MenuType.MEAL.value)
        self.create_menu_items("Restaurant #2", "Menu #4", 200, "Drink #3", "5.0", MenuType.DRINK.value)
        
        self.create_menu_items("Restaurant #2", "Menu #5", 200, "Drink #4", "5.0", MenuType.DRINK.value)
        self.create_menu_items("Restaurant #2", "Menu #5", 100, "Meal #4", "3.0", MenuType.MEAL.value)

        self.create_menu_items("Restaurant #3", "Menu #7", 100, "Meal #5", "3.0", MenuType.MEAL.value)
        self.create_menu_items("Restaurant #3", "Menu #7", 200, "Drink #5", "5.0", MenuType.DRINK.value)
        
        self.create_menu_items("Restaurant #3", "Menu #8", 200, "Drink #6", "5.0", MenuType.DRINK.value)
        self.create_menu_items("Restaurant #3", "Menu #8", 100, "Meal #6", "3.0", MenuType.MEAL.value)

    def create_tables(self):
        self.create_table_items("Restaurant #1", 1, "Table 1")
        self.create_table_items("Restaurant #1", 2, "Table 2")

        self.create_table_items("Restaurant #2", 3, "Table 3")
        self.create_table_items("Restaurant #2", 4, "Table 4")

        self.create_table_items("Restaurant #3", 5, "Table 5")
        self.create_table_items("Restaurant #3", 6, "Table 6")

    # NOTE: ADD, DELETE, UPDATE for RESTAURANT MANAGER
    def add_new_restaurant(self, restaurant_list, restaurant_data):
        new_menu = []
        new_restaurant = Restaurant(
            restaurant_data[0],
            restaurant_data[1],
            [],
            []
        )
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_data[0]}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            self._show_error_message("Invaid Data", "Restaurant already exists")
        else:
            query = f"INSERT INTO restaurants (name, address) VALUES ('{new_restaurant.restaurant_name}', ('{new_restaurant.restaurant_address}'))"
            self.cursor.execute(query)
            self.conn.commit()
            
            new_restaurant_list = self.get_restaurant_list()
            for restaurant in new_restaurant_list:
                new_menu.append((restaurant.restaurant_name, restaurant.restaurant_address),)

        restaurant_list.row_data = new_menu

    def delete_restaurant(self, restaurant_list, condition):
        restaurant_menu_child = self.get_menu_list(condition[0])
        restaurant_table_child = self.get_table_list(condition[0])
        if restaurant_menu_child:
            self._show_error_message("Error", "Delete the items inside the restaurant first.")
        elif restaurant_table_child:
            self._show_error_message("Error", "Delete the items inside the table first.")
        else:
            query = f"DELETE FROM restaurants WHERE name = '{condition[0]}'"
            self.cursor.execute(query)
            self.conn.commit()

            restaurants = self.get_restaurant_list()
            new_restaurant_list = []
            for restaurant in restaurants:
                # print(restaurant.)
                new_restaurant_list.append((restaurant.restaurant_name, restaurant.restaurant_address))

            restaurant_list.row_data = new_restaurant_list

    def update_restaurant(self, restaurant_list, restaurant_data, old_restaurant_data):
        restaurants = restaurant_list
        sql = f"SELECT id FROM restaurants WHERE name = '{old_restaurant_data[0]}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            query = f"UPDATE restaurants SET name = '{restaurant_data[0]}', address = '{restaurant_data[1]}' WHERE name = '{old_restaurant_data[0]}'"
            self.cursor.execute(query)
            self.conn.commit()

            for restaurant in restaurants:
                if restaurant.restaurant_name == old_restaurant_data[0]:
                    restaurant.restaurant_name = restaurant_data[0]
                    restaurant.restaurant_address = restaurant_data[1]
        else:
            print("Restaurant not Found ")

        restaurant_list = restaurants

    # NOTE: ADD, DELETE, UPDATE for MENU MANAGER
    def add_menu(self, restaurant_name, menu_list, menu_data):
        new_menu = MenuList(
            menu_data[0],
            []
        )

        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT id FROM menus WHERE name = '{new_menu.menu_name}' AND  res_fk = {restaurant_id}"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                self._show_error_message("Invalid Data", "Menu already exists!")
            else:
                sql = f"INSERT INTO menus (name, res_fk) VALUES ('{new_menu.menu_name}', {restaurant_id})"
                self.cursor.execute(sql)
                self.conn.commit()

                menu_list.row_data.append(menu_data)

        else:
            print("Restaurant doesn't exist!")    
        
    def update_menu(self, restaurant_name, menu_list, new_menu_name, old_menu_data):
        menus = []
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]

            sql = f"SELECT id FROM menus WHERE name = '{old_menu_data[0]}' AND res_fk = {restaurant_id}"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                query = f"UPDATE menus SET name = '{new_menu_name}' WHERE name = '{old_menu_data[0]}' AND res_fk = {restaurant_id}"
                self.cursor.execute(query)
                self.conn.commit()

                new_menu_list = self.get_menu_list(restaurant_name)
                if new_menu_list:
                    for menu in new_menu_list:
                        menus.append((menu.menu_name, ""))
                menu_list.row_data = menus
        else:
            print("Restaurant doesn't exist.")

    def delete_menu(self, restaurant_name, menu_list, menu_to_delete):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()
        if restaurant_result:
            restaurant_id = restaurant_result[0]
            menu_items = self.get_menu_items_list(restaurant_name , menu_to_delete[0])

            if menu_items:
                self._show_error_message("Error", "Delete the menu items inside the Menu")
            else:

                query = f"DELETE FROM menus WHERE name = '{menu_to_delete[0]}' AND res_fk = {restaurant_id}"
                self.cursor.execute(query)
                self.conn.commit()

                new_menu_list = []
                menu_new_data = self.get_menu_list(restaurant_name)

                if menu_new_data:
                    for menu in menu_new_data:
                        new_menu_list.append((menu.menu_name, ""))
                
                menu_list.row_data = new_menu_list
        else:
            print("Restaurant doesn't exist.")

    # NOTE: ADD, DELETE, UPDATE for MENU ITEM MANAGER
    def add_menu_item(self, restaurant_name, menu_name, menu_item_list, menu_item_data, menu_type):
        new_menu_item = MenuItemList(
            menu_item_data[0],
            menu_item_data[1],
            menu_item_data[2],
            menu_type
        )

        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_results = self.cursor.fetchone()

        if restaurant_results:
            restaurant_id = restaurant_results[0]
            sql = f"SELECT id FROM menus WHERE name = '{menu_name}' AND res_fk = {restaurant_id}"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                menu_id = menu_result[0]
                sql = f"SELECT id FROM items WHERE name = '{new_menu_item.menu_item_name}' AND menu_fk = {menu_id}"
                self.cursor.execute(sql)
                menu_item = self.cursor.fetchone()

                if menu_item:
                    self._show_error_message("Invalid Data", "Menu item already exists")
                else:
                    sql = f"INSERT INTO items (menu_id, name, price, type, menu_fk) VALUES ({new_menu_item.menu_item_id}, '{new_menu_item.menu_item_name}', {new_menu_item.menu_item_price}, {new_menu_item.menu_item_type}, {menu_id})"
                    self.cursor.execute(sql)
                    self.conn.commit()

                    new_item_list = self.get_menu_items_list(restaurant_name, menu_name)

                    item_list = []
                    if new_item_list:
                        for menu in new_item_list:
                            item_list.append((menu.menu_item_id, menu.menu_item_name, menu.menu_item_price, menu.menu_item_type))

                    menu_item_list.row_data = item_list
            else:
                print("Menu not found")
        else: 
            print("Restaurant not found")

    def update_menu_item(self, restaurant_name, menu_name, menu_item_list,  new_menu_item_data, old_menu_item_data):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT id FROM menus WHERE name = '{menu_name}' AND res_fk = {restaurant_id}"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                menu_id = menu_result[0]
                sql = f"SELECT id FROM items WHERE name = '{old_menu_item_data[1]}'"
                self.cursor.execute(sql)
                menu_item = self.cursor.fetchone()

                if menu_item:
                    query = f"UPDATE items SET menu_id = '{new_menu_item_data[0]}', name = '{new_menu_item_data[1]}', price = '{new_menu_item_data[2]}', type = '{new_menu_item_data[3]}' WHERE name = '{old_menu_item_data[1]}' AND menu_fk = '{menu_id}'"
                    self.cursor.execute(query)
                    self.conn.commit()

                    new_updated_list = self.get_menu_items_list(restaurant_name, menu_name)

                    new_item_list = []
                    if new_updated_list:
                        for item in new_updated_list:
                            new_item_list.append((item.menu_item_id, item.menu_item_name, item.menu_item_price, item.menu_item_type))

                    menu_item_list.row_data = new_item_list
                else:
                    print("Menu item doesnt exist ")
            else:
                print("Menu doesnt exist")
        else:
            print("Restaurant doesnt exist")

    def delete_menu_item(self, restaurant_name, menu_name, menu_item_list, menu_item_to_delete):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT id FROM menus WHERE name = '{menu_name}' AND res_fk = {restaurant_id}"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                menu_id = menu_result[0]

                query = f"DELETE FROM items WHERE name = '{menu_item_to_delete[1]}' AND menu_fk = {menu_id}"
                self.cursor.execute(query)
                self.conn.commit()

                new_item_list = []
                updated_item_list = self.get_menu_items_list(restaurant_name, menu_name)

                if updated_item_list:
                    for item in updated_item_list:
                        new_item_list.append((item.menu_item_id, item.menu_item_name, item.menu_item_price, item.menu_item_type))

                menu_item_list.row_data = new_item_list
            else:
                print("Menu doesnt exist")
        else:
            print("Restaurant doesnt exist") 

    # NOTE: ADD, DELETE, UPDATE for TABLE MANAGER
    def add_table(self, restaurant_name, table_list, table_data):
        new_data = TableList(
            table_data[0],
            table_data[1]
        )

        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT id FROM tables WHERE seats = '{new_data.seats}' AND  res_fk = '{restaurant_id}'"
            self.cursor.execute(sql)
            table_result = self.cursor.fetchone()

            if table_result:
                self._show_error_message("Invalid Data", "Table already exists!")
            else:        
                sql = f"INSERT INTO tables (table_id, seats, res_fk) VALUES ('{new_data.table_id}', '{new_data.seats}', '{restaurant_id}')"
                self.cursor.execute(sql)
                self.conn.commit()

                table_list.row_data.append(table_data)

    def update_table(self, restaurant_name, table_list, table_data, old_table_data):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]

            sql = f"SELECT id FROM tables WHERE seats = '{old_table_data[1]}' AND res_fk = {restaurant_id}"
            self.cursor.execute(sql)
            table_result = self.cursor.fetchone()       

            if table_result:
                query = f"UPDATE tables SET table_id = '{table_data[0]}', seats = '{table_data[1]}' WHERE seats = '{old_table_data[1]}' AND res_fk = {restaurant_id}"
                self.cursor.execute(query)
                self.conn.commit()

                new_table_list = self.get_table_list(restaurant_name)
                
                updated_list = []
                if new_table_list:
                    for table in new_table_list:
                        updated_list.append((table.table_id, table.seats))
                
                table_list.row_data = updated_list
        else:
            print("Restaurant doesn't exist.") 
    
    def delete_table(self, restaurant_name, table_list, table_to_delete):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()
        if restaurant_result:
            restaurant_id = restaurant_result[0]

            query = f"DELETE FROM tables WHERE seats = '{table_to_delete[1]}' AND res_fk = {restaurant_id}"
            self.cursor.execute(query)
            self.conn.commit()

            new_table_list = []
            table_new_data = self.get_table_list(restaurant_name)

            if table_new_data:
                for table in table_new_data:
                    new_table_list.append((table.table_id, table.seats))
            
            table_list.row_data = new_table_list
        else:
            print("Restaurant doesn't exist.")
    
    def get_restaurant_list(self):
        self.create_table()
        self.create_restaurants()
        self.create_menu_item_for_restaurant()
        self.create_menu_for_restaurant()
        self.create_tables()

        sql = f"SELECT * FROM restaurants"
        self.cursor.execute(sql)
        restaurants_name = self.cursor.fetchall()

        restaurant_list = []

        for row in restaurants_name:
            menu_list = []
            table_list = []
            restaurant_list.append(Restaurant(row[1], row[2], menu_list, table_list))

        return restaurant_list
    
    def get_menu_list(self, restaurant):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT * FROM menus WHERE res_fk = '{restaurant_id}'"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchall()
            menu_list = []
            for menu in menu_result:
                menu_item_list = []
                menu_list.append(MenuList(menu[1], menu_item_list))

            return menu_list

    def get_menu_items_list(self, restaurant, menu_name):
        menu_item_list = []
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT id FROM menus WHERE name = '{menu_name}' AND res_fk = '{restaurant_id}'"
            self.cursor.execute(sql)
            menu_result = self.cursor.fetchone()

            if menu_result:
                menu_id = menu_result[0]
                query = f"SELECT * FROM items WHERE menu_fk = '{menu_id}'"
                self.cursor.execute(query)
                menu_item_result = self.cursor.fetchall()
                
                for item in menu_item_result:
                    menu_item_list.append(MenuItemList(item[1], item[2], item[3], MenuType(int(item[4])).name))

                return menu_item_list
            else:
                print("Menu doesnt exist")
        else:
            print("Restaurant not found")
   
    def get_table_list(self, restaurant_name):
        sql = f"SELECT id FROM restaurants WHERE name = '{restaurant_name}'"
        self.cursor.execute(sql)
        restaurant_result = self.cursor.fetchone()

        if restaurant_result:
            restaurant_id = restaurant_result[0]
            sql = f"SELECT * FROM tables WHERE res_fk = '{restaurant_id}'"
            self.cursor.execute(sql)
            tables_result = self.cursor.fetchall()

            table_list = []
            for table in tables_result:
                table_list.append(TableList(table[1], table[2]))

            return table_list
        
    def _show_error_message(self, title, content):
        popup = Popup(
            title = title,
            content = Label(
                text = content
            ),
            size_hint = (None, None),
            size = (400, 200)
        )

        popup.open()