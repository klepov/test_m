from rest_framework.exceptions import APIException
from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Item, User
from shop.serializer import ItemsSerializer, UsersSerializer


class ItemsViewSet(ReadOnlyModelViewSet):
    serializer_class = ItemsSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        query_params = self.request.query_params

        sex = query_params.get('sex')
        price = query_params.get('price')

        if sex is not None and price is not None:
            qs = qs.filter(user__sex=sex, price=price)
        else:
            if sex:
                qs = qs.filter(user__sex=sex)
            if price:
                qs = qs.filter(price=price)

        return qs


class UsersViewSet(ReadOnlyModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        ids = self.request.GET.getlist('ids')
        if ids:
            try:
                return User.objects.filter(id__in=list(map(int, self.request.GET.get('ids').split(','))))
            except:
                raise APIException()
        return super().get_queryset()
