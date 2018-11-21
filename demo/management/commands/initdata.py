import time

import django.apps
import requests
from django.core.management.base import BaseCommand
from demo.models import Province, City, Area, Address, Author, Book, Member, User,Order
# python manage.py initdata


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in [Province, City, Area, Address, Author, Book, Member, User,Order]:
            model.objects.all().delete()
        province = Province.objects.create(name="广东省")
        city = City.objects.create(province=province, name="深圳市")
        area = Area.objects.create(city=city, name="南山区")
        address = Address.objects.create(area=area, detail="科技园")
        author = Author.objects.create(address=address, name="令将")
        book = Book.objects.create(author=author, name="陈天故事", price=12)
        member = Member.objects.create(name="M1")
        user = User.objects.create_superuser(
            'admin', 'emailname@demon.com', '123456')
        user.title = "admin"
        user.save()
        Order.objects.create(follower=user, address=address,member=member, book=book, amount=2)
        print("ok")
