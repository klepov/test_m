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
                  "count_items_and_cost_by_user",
                  "username")

    count_items_and_cost_by_user = serializers.SerializerMethodField()

    def get_count_items_and_cost_by_user(self, instance):
        pre_item = instance.count_items_and_cost().get()
        return {"total_sum": pre_item.total_sum,
                "bought_items_count": pre_item.bought_items_count}


class ItemsSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    bought_items_user = serializers.SerializerMethodField()

    def get_bought_items_user(self, instance: Item):
        return User.objects.filter(bought_items=instance).filter(
            date_joined__lte=datetime(year=2019, month=5, day=1)).count()
