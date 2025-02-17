from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.utils.translation import gettext as _


class PinnableAdminMixin:
    def get_queryset(self, request):
        # include number of pins and if the current user is a pin
        return super().get_queryset(request).with_pinned(request.user).with_pins()

    def get_list_display(self, request):
        return [*super().get_list_display(request), 'pin_star']

    def _get_base_actions(self):
        return [*super()._get_base_actions(), *filter(None, map(self.get_action, ('pin', 'unpin')))]

    @admin.action(description=_("Pin items"), permissions=['pin'])
    def pin(self, request, queryset):
        model_name = self.model._meta.model_name
        getattr(request.user, f'pinned_{model_name}s').add(*queryset)

    def has_pin_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('pin', opts)
        return request.user.has_perm(f'{opts.app_label}.{codename}')

    @admin.action(description=_("Unpin items"), permissions=['unpin'])
    def unpin(self, request, queryset):
        model_name = self.model._meta.model_name
        getattr(request.user, f'pinned_{model_name}s').remove(*queryset)

    def has_unpin_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('unpin', opts)
        return request.user.has_perm(f'{opts.app_label}.{codename}')