from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.config import Config


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    """Custom list item."""
    icon = StringProperty("bat")
    my_collection = []
