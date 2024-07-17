from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from enums import UserFeatures, UserRole
from login_controller import LoginController
from utils import AuthorizationService, UserFeatureLabelResolver

class TwoSidedPanel(MDApp):
    def build(self):
        Window.size = (900, 500)
        screen_manager = ScreenManager()
        screen = Screen()
        screen.add_widget(self._create_split_layout_panel())
        screen_manager.add_widget(screen)

        return screen_manager
    
    def _create_split_layout_panel(self):
        layout = GridLayout(
            cols = 2
        )
        layout.add_widget(self._create_navigation_panel())
        # layout.add_widget(self._create_content_panel())
        return layout 

    def _create_navigation_panel(self):
        navigation_panel = GridLayout(
            cols = 1,
            spacing = 20
        )
        navigation_panel.width = Window.width * 0.2
        navigation_panel.height = Window.height * 1

        button_list = self._create_navigation_button_component()
        navigation_panel.add_widget(button_list)
        return navigation_panel
    def _create_navigation_button_component(self):
        self.button_list = []
        user_role = LoginController.get_logged_in_user().user_role # type: ignore
        authorization = AuthorizationService()
        self.user_Features = authorization.get_user_feature_by_user_role(user_role)

        for feature in self.user_Features: # type: ignore
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
    
TwoSidedPanel().run()