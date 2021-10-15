from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarIconListItem


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    """Custom list item."""
    icon = StringProperty("bat")
    my_collection = []
