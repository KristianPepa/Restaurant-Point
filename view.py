from login_controller import LoginController
from utils import AuthorizationService, UserFeatureLabelResolver, UserFeatureContentPanelResolver

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import sys



class TwoSidedPanel(MDApp):
    def build(self):
        Window.size = (900, 500)
        screen = Screen()
        screen.add_widget(self._create_split_into_two_rows())

        return screen
    
    def _create_split_into_two_rows(self):
        rows_layout = GridLayout(
            rows = 2,
            spacing = 20
        )
        rows_layout.add_widget(self._create_split_layout_top_bar())
        rows_layout.add_widget(self._create_split_layout_panel())
        return rows_layout

    def _create_split_layout_top_bar(self):
        columns_layout = GridLayout(
            cols = 2,
            spacing = 20
        )
        columns_layout.size_hint_y = Window.height * 0.1
        columns_layout.add_widget(self.restaurant_point_label())
        columns_layout.add_widget(self.restaurant_category_label())
        return columns_layout

    def restaurant_point_label(self):
        restaurant_label = Button(
            text = "Restaurant Point",
            background_color = (0,1,1,1),
            color = (1,1,1,1),
            font_size = 18,
        )
        restaurant_label.size_hint_x = Window.width * 0.3
        return restaurant_label
    
    def restaurant_category_label(self):
        self._restaurant_category_label = Button(
            text = "",
            background_color = (0,1,1,1),
            color = (1,1,1,1),
            font_size = 14,
        )
        self._restaurant_category_label.size_hint_x = Window.width * 0.7 
        return self._restaurant_category_label

    def _create_split_layout_panel(self):
        self.columns_layout = GridLayout(
            cols = 2,
            spacing = 20
        )
        self.columns_layout.size_hint_y = Window.height * 0.9
        self.columns_layout.add_widget(self._create_navigation_panel())
        self.columns_layout.add_widget(self._create_content_panel())
        return self.columns_layout 

    def _create_navigation_panel(self):
        navigation_panel = GridLayout(
            cols = 1,
            spacing = 20
        )
        navigation_panel.size_hint_x = Window.width * 0.3

        button_list = self._create_navigation_button_component()

        for button in button_list:
            if button.text != "Sign Out":
                button.bind(on_press = self._change_content_panel_label)
            else:
                button.bind(on_press = self._sign_out)

            navigation_panel.add_widget(button)

        return navigation_panel

    def _create_navigation_button_component(self):
        self.button_list = []
        user_role = LoginController.get_logged_in_user().user_role # type: ignore
        authorization = AuthorizationService()
        self.user_features = authorization.get_user_feature_by_user_role(user_role)

        for feature in self.user_features: # type: ignore
            button = Button(
                text = UserFeatureLabelResolver.get_user_feature_label(feature),
                background_color = (0,1,1,1),
                color = (1,1,1,1),
                font_size = 18,
                size_hint = (1, None)
            )
            button.size = (300, 60)
            self.button_list.append(button)
        return self.button_list
    
    def _create_content_panel(self):
        content_panel_layout = GridLayout(
            cols = 1,
            spacing = 10,
        )
        content_panel_layout.size_hint_x = Window.width * 0.7

        return content_panel_layout

    def _change_content_panel_label(self, instance):
        self._restaurant_category_label.text = f"{instance.text}"
        self.columns_layout.clear_widgets()
        self.columns_layout.add_widget(self._create_navigation_panel())
        user_feature_panel_creator = (
            UserFeatureContentPanelResolver.get_user_feature_panel(instance.text)
        )
        self.column_layout = (user_feature_panel_creator.create_content_panel()) # type: ignore
        self.columns_layout.add_widget(self.column_layout)

    
    def _sign_out(self, instance):
        sys.exit(0)

class LoginApp(MDApp):
    username = None
    password = None

    def build(self):
        Window.size = (500, 600)
        screen_manager = ScreenManager()
        screen = Screen()
        screen.add_widget(self._create_login_components())
        screen_manager.add_widget(screen)
        self.screen = screen
        self.screen_manager = screen_manager
        return screen_manager
    
    def _create_login_components(self):
        layout = GridLayout(
            cols = 1,
            padding = 150,
            spacing = 30
        )

        restaurant_point_label = MDLabel(
            text = "Welcome",
            theme_text_color = "Primary",
            font_style = "H6",
            font_size = "50sp",
            halign = "center",
            allow_selection = False
        )

        layout.add_widget(restaurant_point_label)

        self._create_username_component()
        layout.add_widget(self.username_input)

        self._create_password_component()
        layout.add_widget(self.password_input)

        self._create_login_button()
        layout.add_widget(self.login_button)

        return layout
    
    def _create_username_component(self):
        self.username_input = MDTextField(
            hint_text = "Username",
            required = True,
            helper_text =  "Username cant be empty",
            mode = "rectangle",
            icon_left = "account",
        )
    
    def _create_password_component(self):
        self.password_input = MDTextField(
            hint_text = "Password",
            required = True,
            mode = "rectangle",
            icon_right = "eye",
            password = True,
        )

    def _create_login_button(self):
        self.login_button = Button(
            text = "Login",        
        )
        self.login_button.size_hint = (None, None)
        self.login_button.size = (100, 50)
        self.login_button.bind( on_press = self.login_with_provided_credentials) # type: ignore
            
    def login_with_provided_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        
        if self.is_credentials_provided(username, password):
            LoginController.login_user(username, password)
            user = LoginController.get_logged_in_user()
            if user is None:
                popup = Popup(
                    title = "Login Failed",
                    content = Label(
                        text = "Invalid username or password"
                    ),
                    size_hint = (None, None),
                    size = (400, 200)
                )
                self.username_input.text = ""
                self.password_input.text = ""
                popup.open()
            else:
                two_sided_panel = TwoSidedPanel().build()
                self.screen_manager.remove_widget(self.screen)
                self.screen_manager.add_widget(two_sided_panel)
                
    def is_credentials_provided(self, username, password):
        if LoginController.is_string_none_or_blank(username):
            popup = Popup(
                title = "Credentials Missing",
                content = Label(
                    text = "Please provide your username"
                ),
                size_hint =  (None, None),
                size = (400, 200)
            )
            popup.open()
            return False
        
        elif LoginController.is_string_none_or_blank(password):
            popup = Popup(
                title = "Credentials Missing",
                content = Label(
                    text = "Please provide your password"
                ),
                size_hint =  (None, None),
                size = (400, 200)
            )
            popup.open()
            return False

        return True



LoginApp().run()

