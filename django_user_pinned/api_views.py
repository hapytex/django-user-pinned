from django_user_pinned.views import PinnedViewMixin
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.response import Response


class PinAPIView(PinnedViewMixin):

    @action(methods=['get', 'post', 'delete'], detail=True, url_path='pin', url_name='pin', serializer_class=Serializer)
    def check_pin(self, request, *args, **kwargs):
        instance = self.get_object()
        method = request.method.casefold()
        if method == 'get':
            pin = instance.pinned
        elif method == 'post':
            instance.pin(self.request.user)
            pin = True
        else:
            instance.unpin(self.request.user)
            pin = False
        return Response({'pinned': pin})