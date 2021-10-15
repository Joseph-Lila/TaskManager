from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""
    """
    my_collection - this is a collection of checked list elements
    """
    my_collection = []

    def __draw_shadow__(self, origin, end, context=None):
        pass

    def on_active(self, *args):
        if self.active:
            self.my_collection.append(self.parent.parent)
        else:
            self.my_collection.remove(self.parent.parent)
