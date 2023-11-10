from rest_framework.templatetags.rest_framework import items

import library.models
from service.library.library import Library


class Reading(Library):
    def __init__(self, owner):
        super().__init__(owner=owner)

    def set_reading(self):
        pass

    def get_reading(self):
        readings = library.models.Reading.objects.filter(item_id=self.item_id)

    def __set_reading_number(self):
        # TODO: read the model filtering by item and owner and count to return number
        pass


