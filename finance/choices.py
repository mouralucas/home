from django.db import models

from django.utils.translation import gettext_lazy as _


class InterestRate(models.TextChoices):
    FIXED = ('FIXED', _('Pré-fixado'))
    FLOATING = ('FLOATING', _('Pós-fixado'))
    HYBRID = ('HYBRID', _('Hibrido'))
