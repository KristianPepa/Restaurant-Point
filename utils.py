from enums import UserRole, UserFeatures
from admin_view import RestaurantManager, MenuManager, MenuItemManager, TableManager

class AuthorizationService:
    def get_user_feature_by_user_role(self, user_role):
        if user_role == UserRole.ADMIN:
            return [
                UserFeatures.RESTAURANT_MANAGER, 
                UserFeatures.MENU_MANAGER,
                UserFeatures.MENU_ITEM_MANAGER,
                UserFeatures.TABLE_MANAGER,
                UserFeatures.SIGN_OUT
            ]
        elif user_role == UserRole.EMPLOYEE:
            return [
                # UserFeatures.RESTAURANT_MANAGER, 
                UserFeatures.MENU_MANAGER,
                UserFeatures.MENU_ITEM_MANAGER,
                UserFeatures.TABLE_MANAGER,
                UserFeatures.SIGN_OUT
            ]
        elif user_role == UserRole.INTERN:
            return [
                # UserFeatures.RESTAURANT_MANAGER, 
                # UserFeatures.MENU_MANAGER,
                UserFeatures.MENU_ITEM_MANAGER,
                UserFeatures.TABLE_MANAGER,
                UserFeatures.SIGN_OUT
            ]
        elif user_role is None:
            raise RuntimeError("The provided user role " + user_role + " is not supported")
        
class UserFeatureLabelResolver:
    user_feature_label = None

    @staticmethod
    def get_user_feature_label(user_feature):
        return UserFeatureLabelResolver.__get_user_feature_label_dict().get(user_feature)
    
    @staticmethod
    def __get_user_feature_label_dict():
        if UserFeatureLabelResolver.user_feature_label is None:
            UserFeatureLabelResolver.user_feature_label = {
                    UserFeatures.RESTAURANT_MANAGER: "Restaurant Manager",
                    UserFeatures.MENU_MANAGER: "Menu Manager",
                    UserFeatures.MENU_ITEM_MANAGER: "Menu Item Manager",
                    UserFeatures.TABLE_MANAGER: "Table Manager",
                    UserFeatures.SIGN_OUT: "Sign Out"
            }
        return UserFeatureLabelResolver.user_feature_label
    
class UserFeatureContentPanelResolver:
    user_feature_content_panel_map = None

    @staticmethod
    def get_user_feature_panel(user_feature):
        return UserFeatureContentPanelResolver.get_user_feature_panel_map().get(user_feature)
    
    @staticmethod
    def get_user_feature_panel_map():
        if UserFeatureContentPanelResolver.user_feature_content_panel_map is None:
            UserFeatureContentPanelResolver.user_feature_content_panel_map = {
                "Restaurant Manager": RestaurantManager(),
                "Menu Manager": MenuManager(),
                "Menu Item Manager": MenuItemManager(),
                "Table Manager": TableManager()
            }
        return UserFeatureContentPanelResolver.user_feature_content_panel_map