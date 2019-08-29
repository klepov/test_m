from django.test import TestCase

# Create your tests here.
from django.utils.crypto import get_random_string

from shop.models import User, Item
from django.db.models import Count, Sum


class TestSettingModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='test')
        self.user.save()

    def test_lol(self):
        item = Item.objects.create(price=21)
        for _ in range(10):
            u = User.objects.create(username=get_random_string(), password='test')
            u.bought_items.add(item)

        for _ in range(10):
            u = User.objects.all()[1]
            i = Item.objects.create(price=100)
            u.bought_items.add(i)

        for _ in range(10):
            u = User.objects.first()
            i = Item.objects.create(price=100)
            u.bought_items.add(i)
        Sum

        s = User.objects.annotate(bought_items_count=Count('bought_items')).annotate(
            total_sum=Sum('bought_items__price'))

        for i in s:
            print(i.bought_items_count)
            print(i.total_sum)
