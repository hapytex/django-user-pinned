class PinnedViewMixin:
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).with_pinned(self.request.user)