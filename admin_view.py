from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.checkbox import CheckBox

from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable

from dataprovider import DataProvider
from model import Restaurant, MenuList, MenuItemList, TableList
from admin_controllers import RestaurantManagerController, MenuManagerController, MenuItemManagerController, TableListController, RestaurantDatabaseManager
from enums import MenuType

class RestaurantManager:
    selected_row = -1
    restaurant_list = DataProvider().restaurants_list
    restaurant_manager_controller = RestaurantManagerController()

    restaurant_database_manager = RestaurantDatabaseManager("restaurant_point", "postgres", "Eliseo2001!", "localhost", 5432)
    
    restaurant_list_database = restaurant_database_manager.get_restaurant_list()

    def create_content_panel(self):
        layout = GridLayout(
            cols = 2,
            spacing = 20
        )
        layout.size_hint_x = Window.width * 0.7
        layout.add_widget(self._create_management_panel())
        layout.add_widget(self._create_restaurant_list())
        return layout
    
    def _create_management_panel(self):
        management_panel_layout = GridLayout(
            cols = 1, 
            spacing = 20
        )
        management_panel_layout.add_widget(self._create_restaurant_input_data_panel())

        return management_panel_layout
    
    def _create_restaurant_input_data_panel(self):
        restaurant_input_data_panel_layout = GridLayout(
            cols = 1,
            spacing=20,
            padding=20,
        )
        # restaurant_input_data_panel_layout.size_hint_y = 0.1

        self.restaurant_name_input = MDTextField(
            hint_text = "Restaurant Name",
            mode = "rectangle",
            icon_left = "rename",
            helper_text = "Name for Restaurant"
        )

        self.restaurant_address_input = MDTextField(
            hint_text = "Restaurant Address",
            mode = "rectangle",
            helper_text = "Address for Restaurant",
            icon_left = "record-circle-outline"
        )
        restaurant_input_data_panel_layout.add_widget(self.restaurant_name_input)
        restaurant_input_data_panel_layout.add_widget(self.restaurant_address_input)
        restaurant_input_data_panel_layout.add_widget(self._create_button_component())
        # restaurant_input_data_panel_layout.add_widget(label)


        return restaurant_input_data_panel_layout
    
    def _create_button_component(self):
        buttons_layout = GridLayout(
            rows = 1,
            spacing = 10
        )
        add_button = Button(
            text = "Add",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        add_button.size = (0, 50)
        add_button.bind(on_press = self._add_restaurant) # type: ignore

        update_button = Button(
            text = "Update",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        update_button.size = (0, 50)
        update_button.bind(on_press = self._update_restaurant) # type: ignore
        delete_button = Button(
            text = "Delete",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        delete_button.size = (0, 50)
        delete_button.bind(on_press = self._delete_restaurant) # type: ignore

        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(update_button)
        buttons_layout.add_widget(delete_button)

        return buttons_layout


    def _create_restaurant_list(self):
        restaurant_list_layout = GridLayout(
            cols = 1,
            padding = 20
        )
        self.restaurant_table = self.create_table()
        self.restaurant_table.bind(on_check_press = self._checked)
        self.restaurant_table.bind(on_row_press = self._on_row_press)
        restaurant_list_layout.add_widget(self.restaurant_table)

        return restaurant_list_layout
    
    def create_table(self):
        table_row_data = []
        
        table_data = self.restaurant_database_manager.get_restaurant_list()
        # Without Database
        # for restaurant in self.restaurant_list:
        #     table_row_data.append((
        #         restaurant.restaurant_name,
        #         restaurant.restaurant_address
        #     ))

        # With Database
        for restaurant in table_data:
            table_row_data.append((
                restaurant.restaurant_name,
                restaurant.restaurant_address
            ))

        self.restaurant_table = MDDataTable(
            pos_hint = { "center_x": 0.5, "center_y": 0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("Name", dp(50)),
                ("Address", dp(50))
            ],
            row_data = table_row_data
        )
        return self.restaurant_table
    
    def _checked(self, instance_table, current_row):
        selected_restaurant = Restaurant(
            current_row[0],
            current_row[1],
            [],
            []
        )

        self.restaurant_name_input.text = str(selected_restaurant.restaurant_name)
        self.restaurant_address_input.text = str(selected_restaurant.restaurant_address)

    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))
    
    def _show_error_popup_message(self, title, content):
        popup = Popup(
            title = title,
            content = Label(
                text = content
            ),
            size_hint = (None, None),
            size = (400, 200)
        )
        popup.open()

    def _is_data_valid(self, restaurant_data):
        return (
            restaurant_data[0] != ""
            and restaurant_data[1] != ""
        )

    def _clear_input_text_fields(self):
        self.restaurant_name_input.text = ""
        self.restaurant_address_input.text = ""
        self.selected_row = -1

    def _add_restaurant(self, instance):
        name = self.restaurant_name_input.text
        address = self.restaurant_address_input.text

        restaurant_data = [name, address]

        if self._is_data_valid(restaurant_data):
            # With Database
            self.restaurant_database_manager.add_new_restaurant(self.restaurant_table, restaurant_data)
            
            # Without Database
            # self.restaurant_manager_controller.add_restaurant(self.restaurant_list, restaurant_data)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Provide mandatory data to add new Restaurant")

    def _update_restaurant(self, instance):
        if self.selected_row != -1:
            name = self.restaurant_name_input.text
            address = self.restaurant_address_input.text

            restaurant_data = [name, address]

            if self._is_data_valid(restaurant_data):
                restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]

                del self.restaurant_table.row_data[self.selected_row]
                # With Database
                self.restaurant_database_manager.update_restaurant(self.restaurant_list_database, restaurant_data, restaurant_to_remove)
                # Without Database
                # self.restaurant_manager_controller.update_restaurant(self.restaurant_list, restaurant_data, restaurant_to_remove)
                
                self.restaurant_table.row_data.append([name, address])

                self._clear_input_text_fields()
            else:
                self._show_error_popup_message("Invalid Data", "Provide mandatory data to update Restaurant")
        else:
            self._show_error_popup_message("Invalid Data", "Select a row to update")

    def _delete_restaurant(self, instance):
        if self.selected_row != -1:
            restaurant_to_delete = self.restaurant_table.row_data[self.selected_row]

            # With Database
            self.restaurant_database_manager.delete_restaurant(self.restaurant_table, restaurant_to_delete)
            
            # Without Database
            # self.restaurant_manager_controller.delete_restaurant(self.restaurant_list, restaurant_to_delete[0])

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Select any row to delete")

class MenuManager:
    selected_row = -1
    restaurant_list = DataProvider().restaurants_list
    menu_list = restaurant_list[0].menu_list
    menu_controller = MenuManagerController()

    restaurant_database_manager = RestaurantDatabaseManager("restaurant_point", "postgres", "Eliseo2001!", "localhost", 5432)

    restaurant_list = restaurant_database_manager.get_restaurant_list()
    selected_restaurant = restaurant_list[0].restaurant_name
    selected_restaurant_menu = restaurant_database_manager.get_menu_list(selected_restaurant)

    def create_content_panel(self):
        layout = GridLayout(
            cols = 2,
            spacing = 20
        )
        layout.size_hint_x = Window.width * 0.7
        layout.add_widget(self._create_management_panel())
        layout.add_widget(self._create_restaurant_list())
        return layout
    
    def _create_management_panel(self):
        management_panel_layout = GridLayout(
            cols = 1, 
            spacing = 20
        )
        management_panel_layout.add_widget(self._create_menu_list_input_data_panel())

        return management_panel_layout
    
    def _create_menu_list_input_data_panel(self):
        restaurant_manager_input_data_panel_layout = GridLayout(
            cols = 1,
            spacing=20,
            padding=20,
        )

        self.menu_input_name = MDTextField(
            hint_text = "Menu Name",
            mode = "rectangle",
            icon_left = "transcribe",
            helper_text = "Name for the menu"
        )

        restaurant_manager_input_data_panel_layout.add_widget(self.menu_input_name)
        restaurant_manager_input_data_panel_layout.add_widget(self._create_button_component())

        return restaurant_manager_input_data_panel_layout

    def _create_button_component(self):
        buttons_layout = GridLayout(
            rows = 1,
            spacing = 10,
            padding = 20
        )
        add_button = Button(
            text = "Add",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        add_button.size = (0, 50)
        add_button.bind(on_press = self._add_menu) # type: ignore

        update_button = Button(
            text = "Update",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        update_button.size = (0, 50)
        update_button.bind(on_press = self._update_menu) # type: ignore
        
        delete_button = Button(
            text = "Delete",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        delete_button.size = (0, 50)
        delete_button.bind(on_press = self._delete_menu) # type: ignore

        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(update_button)
        buttons_layout.add_widget(delete_button)

        return buttons_layout
    
    def _show_error_popup_message(self, title, content):
        popup = Popup(
            title = title,
            content = Label(
                text = content
            ),
            size_hint = (None, None),
            size = (400, 200)
        )
        popup.open()

    def _is_data_valid(self, menu_data):
        return (
            menu_data[0] != ""
        )
    
    def _clear_input_text_fields(self):
        self.selected_row = -1
        self.menu_input_name.text = ""

    def _create_restaurant_list(self):
        restaurant_and_menu_list = GridLayout(
            cols = 1,
            padding = 20,
            spacing = 20
        )


        restaurant_and_menu_list.add_widget(self._create_restaurant_menu_select_component())
        restaurant_and_menu_list.add_widget(self._create_menu_list_component())

        return restaurant_and_menu_list
    
    def _create_restaurant_menu_select_component(self):
        if self.selected_restaurant:

            self.button = MDRectangleFlatIconButton(
                text = self.selected_restaurant,
                icon = "menu",
                size_hint = (1,0)
            )
        self.button.bind(on_release = self.show_dropdown_menu) # type: ignore
        return self.button
    
    def show_dropdown_menu(self, button):
        menu_items = []
        
        drop_down_data = self.restaurant_database_manager.get_restaurant_list()
        
        if drop_down_data: 
            for restaurnat in drop_down_data:
                menu_items.append({
                    "viewclass": "OneLineListItem",
                    "text": restaurnat.restaurant_name,
                    "on_release": lambda r = restaurnat: self.update_menu_list(r)
                })
             
        self.dropdown_menu = MDDropdownMenu(
            caller = button,
            position = "bottom",
            items = menu_items,
            max_height = dp(150),
            width_mult = 5
        )
        
        self.dropdown_menu.open()

    def update_menu_list(self, restaurant):
        self.button.text = restaurant.restaurant_name
        self.selected_restaurant = restaurant.restaurant_name
        self.selected_restaurant_menu = self.restaurant_database_manager.get_menu_list(self.selected_restaurant)


        menu_list = []
        if self.selected_restaurant_menu:
            for menu in self.selected_restaurant_menu:
                menu_list.append((menu.menu_name, ""))
        
        self.menu_list_table.row_data = menu_list

        self.dropdown_menu.dismiss()

    def _create_menu_list_component(self):
        menu_list_layout = GridLayout(
            cols = 1,
            padding = 20
        )

        self.menu_table = self.create_table()
        self.menu_table.bind(on_check_press = self._checked)
        self.menu_table.bind(on_row_press = self._on_row_press)
        menu_list_layout.add_widget(self.menu_table)
        
        return menu_list_layout
    
    def create_table(self):
        table_row_data = []

        table_data = self.restaurant_database_manager.get_menu_list(self.selected_restaurant)
        # With Database
        if table_data:
            for menu in table_data:
                table_row_data.append((menu.menu_name, ""))
        
        self.menu_list_table = MDDataTable(
            pos_hint = {"center_x": 0.5, "center_y": 0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("Menu Name", dp(40)),
                ("", dp(40))
            ],
            row_data = table_row_data
        )

        return self.menu_list_table
    
    def _checked(self, instance_table, current_row):
        selected_menu = MenuList(
            current_row[0],
            []
        )

        self.menu_input_name.text = str(selected_menu.menu_name)

    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))
   
    def _add_menu(self, instance):  
        menu_name = self.menu_input_name.text
        menu_data = [menu_name, ""]

        if self._is_data_valid(menu_data):
            # Without Database
            # self.menu_controller.add_menu(self.menu_list , menu_data)

            # With Database
            self.restaurant_database_manager.add_menu(self.selected_restaurant, self.menu_list_table, menu_data)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Provide mandatory data to add new menu")

    def _update_menu(self, instance):
        if self.selected_row != -1:
            menu_name = self.menu_input_name.text

            menu_data = [menu_name,]

            if self._is_data_valid(menu_data):
                menu_to_remove = self.menu_list_table.row_data[self.selected_row]

                del self.menu_list_table.row_data[self.selected_row]
                # Without Database
                # self.menu_controller.update_menu(self.menu_list, menu_to_remove)

                # With Database
                self.restaurant_database_manager.update_menu(self.selected_restaurant, self.menu_list_table, menu_name, menu_to_remove)
                
                self._clear_input_text_fields()
            else:
                self._show_error_popup_message("Invalid Data", "Provide mandatory data to update menu")
        else:
            self._show_error_popup_message("Invalid Data", "Select a row to update")

    def _delete_menu(self, instance):
        if self.selected_row != -1:
            menu_to_remove = self.menu_list_table.row_data[self.selected_row]

            # del self.menu_list_table.row_data[self.selected_row]
            # Without Database
            # self.menu_controller.delete_menu(self.menu_list, menu_to_remove)

            # With Database
            self.restaurant_database_manager.delete_menu(self.selected_restaurant, self.menu_list_table, menu_to_remove)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Select any row to delete")

class MenuItemManager:
    selected_row = -1
    restaurant_list = DataProvider().restaurants_list
    menu_item_list_controller = MenuItemManagerController()
    menu_list = restaurant_list[0].menu_list
    selected_menu = menu_list[0]
    item_list = menu_list[0].menu_item_list
    selected_menu_item = None

    restaurant_database_manager = RestaurantDatabaseManager("restaurant_point", "postgres", "Eliseo2001!", "localhost", 5432)

    restaurant_list = restaurant_database_manager.get_restaurant_list()
    selected_restaurant = restaurant_list[0].restaurant_name

    selected_menu_list = restaurant_database_manager.get_menu_list(selected_restaurant)
    if selected_menu_list:
        selected_menu = selected_menu_list[0].menu_name 

    def create_content_panel(self):
        layout = GridLayout(
            cols = 2,
            spacing = 20
        )
        layout.size_hint_x = Window.width * 0.7
        layout.add_widget(self._create_management_panel())
        layout.add_widget(self._create_menu_item_list_panel())
        return layout
    
    def _create_management_panel(self):
        management_panel_layout = GridLayout(
            cols = 1, 
            spacing = 20
        )
        management_panel_layout.add_widget(self._create_menu_list_input_data_panel())

        return management_panel_layout
    
    def _create_menu_list_input_data_panel(self):
        restaurant_manager_input_data_panel_layout = GridLayout(
            cols = 1,
            spacing=20,
            padding=20,
        )

        self.menu_input_id = MDTextField(
            hint_text = "Menu item id",
            mode = "rectangle",
            # icon_left = "transcribe",
            helper_text = "Id of the menu"
        )

        self.menu_input_name = MDTextField(
            hint_text = "Menu item name",
            mode = "rectangle",
            # icon_left =  
            helper_text = "Name of the menu"
        )

        self.menu_input_price = MDTextField(
            hint_text = "Menu item price",
            mode = "rectangle",
            # icon_left =  
            helper_text = "Price of the menu"
        )



        restaurant_manager_input_data_panel_layout.add_widget(self.menu_input_id)
        restaurant_manager_input_data_panel_layout.add_widget(self.menu_input_name)
        restaurant_manager_input_data_panel_layout.add_widget(self.menu_input_price)
        restaurant_manager_input_data_panel_layout.add_widget(self.create_menu_type_checkbox())
        restaurant_manager_input_data_panel_layout.add_widget(self._create_button_component())

        return restaurant_manager_input_data_panel_layout

    def create_menu_type_checkbox(self):
        self.menu_type_panel = GridLayout(
            cols = 2,
            spacing = 20,
            size_hint = (None, None)
        )

        self.menu_types = ["Meal", "Drink"]
        self.checkboxes = []

        for food_type in self.menu_types:
            checkbox = CheckBox(
                group = "food_type",
                active = False,
                color = (0,0,0,1)
            )
            label = Label(
                text = food_type,
                color = (0,0,0,1)
            )
            self.menu_type_panel.add_widget(checkbox)
            self.menu_type_panel.add_widget(label)
            self.checkboxes.append(checkbox)

        return self.menu_type_panel

    def _get_selected_food_type(self):
        for index, child in enumerate(self.menu_type_panel.children):
            if isinstance(child, CheckBox) and child.active:
                label_index = index - 1
                if label_index < len(self.menu_type_panel.children):
                    label = self.menu_type_panel.children[label_index]
                    priority_text = label.text.lower()
                    return MenuType[priority_text.upper()]
        return None

    def _create_button_component(self):
        buttons_layout = GridLayout(
            rows = 1,
            spacing = 10,
            padding = 20
        )
        add_button = Button(
            text = "Add",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        add_button.size = (0, 50)
        add_button.bind(on_press = self._add_menu_item) # type: ignore

        update_button = Button(
            text = "Update",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        update_button.size = (0, 50)
        update_button.bind(on_press = self._update_menu_item) # type: ignore
        
        delete_button = Button(
            text = "Delete",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        delete_button.size = (0, 50)
        delete_button.bind(on_press = self._delete_menu_item) # type: ignore

        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(update_button)
        buttons_layout.add_widget(delete_button)

        return buttons_layout
    
    def _is_data_valid(self, new_data):
        return (
            new_data[0] != ""
            and new_data[1] != ""
            and new_data[2] != ""
            and new_data[3] != None
        )
    
    def _show_error_popup_message(self, title, content):
        popup = Popup(
            title = title,
            content = Label(
                text = content
            ),
            size_hint = (None, None),
            size = (400, 200)
        )

        popup.open()

    def _clear_input_text_fields(self):
        self.selected_row = -1
        self.menu_input_id.text = ""
        self.menu_input_name.text = ""
        self.menu_input_price.text = ""
        
        for child in self.menu_type_panel.children:
            if isinstance(child, CheckBox):
                child.active = False
            if isinstance(child, Label):
                child.color = (0,0,0,1)
    
    def _create_menu_item_list_panel(self):
        menu_item_list_panel = GridLayout(
            cols = 1,
            padding = 20,
            spacing = 20
        )

        menu_item_list_panel.add_widget(self._create_restaurant_menu_select_component())
        menu_item_list_panel.add_widget(self._create_menu_select_component())
        menu_item_list_panel.add_widget(self._create_menu_item_list_component())

        self.menu_items_table.bind(on_check_press = self._checked)
        self.menu_items_table.bind(on_row_press = self._on_row_press)
        return menu_item_list_panel
    
    def _create_restaurant_menu_select_component(self):
        self.restaurant_select_button = MDRectangleFlatIconButton(
            text = self.selected_restaurant,
            icon = "menu",
            size_hint = (1, None)
        )
        self.restaurant_select_button.bind(on_release = self.show_dropdown_menu) # type: ignore
        return self.restaurant_select_button
    
    def show_dropdown_menu(self, button):
        menu_items = []

        restaurant_list_updated = self.restaurant_database_manager.get_restaurant_list()

        for restaurnat in restaurant_list_updated:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": restaurnat.restaurant_name,
                "on_release": lambda r = restaurnat: self.update_menu_list(r)
            })

        self.dropdown_menu = MDDropdownMenu(
            caller = button,
            position = "bottom",
            items = menu_items,
            max_height = dp(150),
            width_mult = 5
        )
        
        self.dropdown_menu.open()

    def update_menu_list(self, restaurant):
        self.restaurant_select_button.text = restaurant.restaurant_name
        self.selected_restaurant = restaurant.restaurant_name

        self.selected_menu_list = self.restaurant_database_manager.get_menu_list(restaurant.restaurant_name)
        
        menu_list = []
        if self.selected_menu_list:
            for menu in self.selected_menu_list:
                menu_list.append((menu.menu_name,))
            
        self.menu_list = self.selected_restaurant

        self.dropdown_menu.dismiss()

    def _create_menu_select_component(self):
        if self.selected_menu:
            self.menu_select_button = MDRectangleFlatIconButton(
                text = self.selected_menu,
                icon = "menu",
                size_hint = (1, None)
            )

        self.menu_select_button.bind(on_release = self.show_dropdown_menu_list) 

        return self.menu_select_button

    def show_dropdown_menu_list(self, button):
        menu_list_items = []

        menu_list_updated = self.restaurant_database_manager.get_menu_list(self.selected_restaurant)

        if menu_list_updated:
            for menu in menu_list_updated:
                menu_list_items.append({
                    "viewclass": "OneLineListItem",
                    "text": menu.menu_name,
                    "on_release": lambda m = menu: self.update_menu_list_items(m)
                })
        
        self.dropdown_menu_items = MDDropdownMenu(
            caller = button,
            position = "bottom",
            items = menu_list_items,
            max_height = dp(300),
            width_mult = 5
        )

        self.dropdown_menu_items.open()

    def update_menu_list_items(self, menu):
        self.menu_select_button.text = menu.menu_name
        self.selected_menu = menu.menu_name

        item_list = self.restaurant_database_manager.get_menu_items_list(self.selected_restaurant, menu.menu_name)

        menu_items_list = []
        if item_list:
            for item in item_list:
                menu_items_list.append((item.menu_item_id, item.menu_item_name, item.menu_item_price, item.menu_item_type))
        else:
            print("Item list not full")

        self.menu_items_table.row_data = menu_items_list

        self.dropdown_menu_items.dismiss()

    def _create_menu_item_list_component(self):
        table_row_data = []
        item_list = self.restaurant_database_manager.get_menu_items_list(self.selected_restaurant, self.selected_menu)
        if item_list:
            for item in item_list:
                table_row_data.append((item.menu_item_id, item.menu_item_name, item.menu_item_price, item.menu_item_type))

        self.menu_items_table = MDDataTable(
            pos_hint = {"center_x": 0.5, "center_y": 0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("ID", dp(30)),
                ("Name", dp(30)),
                ("Price", dp(30)),
                ("Menu Type", dp(30))
            ],
            row_data = table_row_data
        )

        return self.menu_items_table
    
    def _checked(self, instance_table, current_row):
        selected_menu_item = MenuItemList(
            current_row[0],
            current_row[1],
            current_row[2],
            current_row[3]
        )

        self.menu_input_id.text = str(selected_menu_item.menu_item_id)
        self.menu_input_name.text = str(selected_menu_item.menu_item_name)
        self.menu_input_price .text = str(selected_menu_item.menu_item_price)
        
        if selected_menu_item.menu_item_type.upper() == MenuType.MEAL.name:
            self.menu_type_panel.children[3].active = True
        elif selected_menu_item.menu_item_type.upper() == MenuType.DRINK.name:
            self.menu_type_panel.children[1].active = True
            
    def _on_row_press(self, instance_table, current_row):
        self.selected_row = int(current_row.index / len(instance_table.column_data))

    def _add_menu_item(self, instance):
        menu_item_id = self.menu_input_id.text
        menu_item_name = self.menu_input_name.text
        menu_item_price = self.menu_input_price.text
        menu_item_type = self._get_selected_food_type()

        new_menu_item = [menu_item_id, menu_item_name, menu_item_price, menu_item_type]
        if self._is_data_valid(new_menu_item):
            menu_type = menu_item_type.value # type: ignore
            # Without Database
            # self.menu_item_list_controller.add_menu_item(self.item_list, new_menu_item)
            # self.menu_items_table.row_data.append([menu_item_id, menu_item_name, menu_item_price, menu_item_type.name]) # type: ignore
        
            # With Database

            self.restaurant_database_manager.add_menu_item(self.selected_restaurant, self.selected_menu, self.menu_items_table, new_menu_item, menu_type)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Provie mandatory data to add new menu item")

    def _update_menu_item(self, instance):
        if self.selected_row != -1:
            menu_item_id = self.menu_input_id.text
            menu_item_name = self.menu_input_name.text
            menu_item_price = self.menu_input_price.text
            menu_item_type = self._get_selected_food_type()

            item_data = [menu_item_id, menu_item_name, menu_item_price, menu_item_type.value]  # type: ignore
            if self._is_data_valid(item_data):
                item_to_remove = self.menu_items_table.row_data[self.selected_row]
                # Without Database
                # del self.menu_items_table.row_data[self.selected_menu]
                # self.menu_item_list_controller.update_menu_item(self.item_list, item_to_remove)

                # self.menu_items_table.row_data.append([menu_item_id, menu_item_name, menu_item_price, menu_item_type.name]) # type: ignore

                # With Database
                self.restaurant_database_manager.update_menu_item(self.selected_restaurant, self.selected_menu, self.menu_items_table, item_data, item_to_remove)

                self._clear_input_text_fields()
            else:
                self._show_error_popup_message("Invalid Data", "Provide mandatory data to update menu item")              
        else:
            self._show_error_popup_message("Invalid Data", "Select a row to update")              

    def _delete_menu_item(self, instance):
        if self.selected_row != -1:
            item_to_remove = self.menu_items_table.row_data[self.selected_row]
            
            # Without Database
            # del self.menu_items_table.row_data[self.selected_row]
            # self.menu_item_list_controller.delete_menu_item(self.item_list, item_to_remove)

            # With Database
            self.restaurant_database_manager.delete_menu_item(self.selected_restaurant, self.selected_menu, self.menu_items_table, item_to_remove)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Select any row to delete")

class TableManager:
    selected_row = -1
    restaurant_list = DataProvider().restaurants_list
    table_list = restaurant_list[0].table_list
    table_list_controller = TableListController()

    restaurant_database_manager = RestaurantDatabaseManager("restaurant_point", "postgres", "Eliseo2001!", "localhost", 5432)

    restaurant_list_with_database = restaurant_database_manager.get_restaurant_list()
    selected_restaurant = restaurant_list_with_database[0].restaurant_name

    def create_content_panel(self):
        layout = GridLayout(
            cols = 2,
            spacing = 20
        )
        layout.size_hint_x = Window.width * 0.7
        layout.add_widget(self._create_management_panel())
        layout.add_widget(self._create_table_list())
        return layout
    
    def _create_management_panel(self):
        management_panel_layout = GridLayout(
            cols = 1, 
            spacing = 20
        )
        management_panel_layout.add_widget(self._create_table_input_data_panel())

        return management_panel_layout
    
    def _create_table_input_data_panel(self):
        restaurant_manager_input_data_panel_layout = GridLayout(
            cols = 1,
            spacing=20,
            padding=20,
        )

        self.table_input_id = MDTextField(
            hint_text = "Table id",
            mode = "rectangle",
            icon_left = "transcribe",
            helper_text = "Table number (id)"
        )

        self.table_input_seat = MDTextField(
            hint_text = "Seats",
            mode = "rectangle",
            icon_left = "transcribe",
            helper_text = "Seats number"
        )

        restaurant_manager_input_data_panel_layout.add_widget(self.table_input_id)
        restaurant_manager_input_data_panel_layout.add_widget(self.table_input_seat)
        restaurant_manager_input_data_panel_layout.add_widget(self._create_button_component())

        return restaurant_manager_input_data_panel_layout

    def _create_button_component(self):
        buttons_layout = GridLayout(
            rows = 1,
            spacing = 10,
            padding = 20
        )
        add_button = Button(
            text = "Add",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        add_button.size = (0, 50)
        add_button.bind(on_press = self._add_table) # type: ignore

        update_button = Button(
            text = "Update",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        update_button.size = (0, 50)
        update_button.bind(on_press = self._update_table) # type: ignore
        
        delete_button = Button(
            text = "Delete",
            background_color = (0,1,1,1),
            font_size = 18,
            size_hint = (0.3, None)
        )
        delete_button.size = (0, 50)
        delete_button.bind(on_press = self._delete_table) # type: ignore

        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(update_button)
        buttons_layout.add_widget(delete_button)

        return buttons_layout
    
    def _is_data_valid(self, data):
        return (
            data[0] != ""
            and data[1] != ""
        ) 
    
    def _clear_input_text_fields(self):
        self.selected_row = -1
        self.table_input_id.text = ""
        self.table_input_seat.text = ""

    def _show_error_popup_message(self, title, content):
        popup = Popup(
            title = title,
            content = Label(
                text = content
            ),
            size_hint = (None, None),
            size = (400, 200)
        )

        popup.open()

    def _create_table_list(self):
        restaurant_and_table_list = GridLayout(
            cols = 1,
            padding = 20,
            spacing = 20
        )

        restaurant_and_table_list.add_widget(self._create_restaurant_select_component())
        restaurant_and_table_list.add_widget(self._create_menu_list_component())

        self.table_data.bind(on_check_press = self._checked)
        self.table_data.bind(on_row_press = self._on_row_press)
        return restaurant_and_table_list
    
    def _create_restaurant_select_component(self):
        self.button = MDRectangleFlatIconButton(
            text = self.selected_restaurant,
            icon = "menu",
            size_hint = (1,0)
        )
        self.button.bind(on_release = self.show_dropdown_menu) # type: ignore
        return self.button
    
    def show_dropdown_menu(self, button):
        menu_items = []

        restaurant_list_updated = self.restaurant_database_manager.get_restaurant_list()

        for restaurnat in restaurant_list_updated:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": restaurnat.restaurant_name,
                "on_release": lambda r = restaurnat: self.update_menu_list(r)
            })


        self.dropdown_menu = MDDropdownMenu(
            caller = button,
            position = "bottom",
            items = menu_items,
            max_height = dp(150),
            width_mult = 5
        )
        
        self.dropdown_menu.open()
 
    def update_menu_list(self, restaurant):
        self.button.text = restaurant.restaurant_name
        self.selected_restaurant = restaurant.restaurant_name

        self.selected_table_list = self.restaurant_database_manager.get_table_list(restaurant.restaurant_name)

        table_list = []
        if self.selected_table_list:
            for table in self.selected_table_list:
                table_list.append((table.table_id, table.seats))
        
        self.table_data.row_data = table_list
        # self.table_list = self.selected_restaurant

        self.dropdown_menu.dismiss()

    def _create_menu_list_component(self):
        table_row_data = []

        self.selected_table_list = self.restaurant_database_manager.get_table_list(self.selected_restaurant)

        if self.selected_table_list:
            for table in self.selected_table_list:
                table_row_data.append((table.table_id, table.seats))

            
        self.table_data = MDDataTable(
            pos_hint = {"center_x": 0.5, "center_y": 0.5},
            check = True,
            use_pagination = True,
            rows_num = 10,
            column_data = [
                ("ID", dp(35)),
                ("Seats", dp(35))
            ],
            row_data = table_row_data
        )

        return self.table_data
    
    def _checked(self, instance_table, current_row):
        selected_row = TableList(
            current_row[0],
            current_row[1]
        )
        self.table_input_id.text = selected_row.table_id
        self.table_input_seat.text = selected_row.seats

    def _on_row_press(self, instance_table, current_row):
        self.selected_row = int(current_row.index / len(instance_table.column_data))

    def _add_table(self, instance):
        table_id = self.table_input_id.text
        table_seat = self.table_input_seat.text

        new_table = [table_id, table_seat]

        if self._is_data_valid(new_table):
            # Without Database
            # self.table_list_controller.add_table(self.table_list, new_table)
            # self.table_data.row_data.append([table_id, table_seat])

            # With Database
            self.restaurant_database_manager.add_table(self.selected_restaurant, self.table_data, new_table)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Provide mandatory data to add new table")

    def _update_table(self, instance):
        if self.selected_row != -1:
            table_id = self.table_input_id.text
            table_seat = self.table_input_seat.text
            
            new_table = [table_id, table_seat]
            
            if self._is_data_valid(new_table):
                table_to_remove = self.table_data.row_data[self.selected_row]

                # del self.table_data.row_data[self.selected_row]
                # self.table_list_controller.update_table(self.table_list, new_table)

                # self.table_data.row_data.append([table_id, table_seat])

                self.restaurant_database_manager.update_table(self.selected_restaurant, self.table_data, new_table, table_to_remove)

                self._clear_input_text_fields()
            else:
                self._show_error_popup_message("Invalid Data", "Provide mandatory data to update table")
        else:
            self._show_error_popup_message("Invalid Data", "Select a row to update")

    def _delete_table(self, instance):
        if self.selected_row != -1:
            table_to_delete = self.table_data.row_data[self.selected_row]
            # Without Database
            # del self.table_data.row_data[self.selected_row]
            # self.table_list_controller.delete_table(self.table_list, table_to_delete)

            # With Database
            self.restaurant_database_manager.delete_table(self.selected_restaurant, self.table_data, table_to_delete)

            self._clear_input_text_fields()
        else:
            self._show_error_popup_message("Invalid Data", "Select a row to delete")
