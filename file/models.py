from django.db import models

import core.models


class File(core.models.Log):
    file = models.FileField()
    thumbnail = models.FileField(null=True)  # TODO: definir default dos thumb
    name = models.CharField(max_length=250)
    extension = models.CharField(max_length=50)
    size = models.IntegerField(null=True)

    main_category = models.ForeignKey('core.Category', on_delete=models.DO_NOTHING, null=True)

    owner = models.ForeignKey('user.Account', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_owner')
    is_directory = models.BooleanField(default=False)

    class Meta:
        db_table = 'public"."files'
