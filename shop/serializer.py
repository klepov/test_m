from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Item, User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("date_joined",
                  "dttm_deleted",
                  "sex",
                  "id",
                  'count_items_and_cost_by_user',
                  "username")

    count_items_and_cost_by_user = serializers.SerializerMethodField()

    def get_count_items_and_cost_by_user(self, instance):
        return {"total_sum": instance.total_sum,
                "bought_items_count": instance.bought_items_count}


class ItemsSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    bought_items_user = serializers.SerializerMethodField()

    def get_bought_items_user(self, instance: Item):
        return instance.user_set.filter(date_joined__lte=datetime(year=2019, month=5, day=1)).count()
