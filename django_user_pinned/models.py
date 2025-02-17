from django.db import models
from django.conf import settings
from django.db.models.aggregates import Count
from django.db.models.expressions import Exists, OuterRef
from django.db.models.query_utils import Q
from django.contrib import admin
from django.utils.translation import gettext as _


STAR_CHARS = '☆★'


class PinnableQuerySet(models.QuerySet):
    def with_pinned(self, user, *users):
        model = self.model
        rel = model.pinned_by
        junction = rel.through
        rel_name = rel.rel.model._meta.model_name
        if users:
            rel_name = f'{rel_name}__in'
            user = (user, *users)
        return self.annotate(
            is_pinned=Exists(junction.objects.filter(
                Q((self.model._meta.model_name, OuterRef('pk')),
                Q((rel_name, user))
            )))
        )

    def with_pinned_sorted(self, user, *users):
        return self.get_pinned(user, *users).order_by('-is_pinned')

    def with_pins(self):
        return self.annotate(_pins=Count('pinned_by', distinct=True))

    def with_pins_sorted(self):
        return self.with_pins().order_by('-_pins')


class PinnableModel(models.Model):
    pinned_by = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='pinned_%(class)ss', blank=True, editable=False)
    objects = PinnableQuerySet.as_manager()

    @property
    def pins(self):
        pins = getattr(self, '_pins', None)
        if pins is None:
            self._pins = pins = self.pinned_by.count()
        return pins

    @property
    def pin_star_char(self):
        return STAR_CHARS[bool(getattr(self, 'is_pinned', False))]

    @property
    @admin.display(description='pins', ordering='_pins')
    def pin_star(self):
        return f'{self.pins} {self.pin_star_char}'

    def pin(self, user, *users):
        self.pinned_by.add(user, *users)

    def unpin(self, user, *users):
        self.pinned_by.remove(user, *users)

    class Meta:
        abstract = True
        permissions = [
            ('pin', _('a user can add an object to their selection')),
            ('unpin', _('a user can remove an object from their selection')),
        ]