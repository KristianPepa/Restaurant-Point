from login_controller import LoginController

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


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
                # ADD Two Sided Layout Here
                popup = Popup(
                    title = "Login Successful",
                    content = Label(
                        text = f"Welcome '{user.username}'"
                    ),
                    size_hint = (None, None),
                    size = (400, 200)
                )
                popup.open()
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

