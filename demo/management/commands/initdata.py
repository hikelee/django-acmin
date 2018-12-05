import json

from django.conf import settings
from django.core.management.base import BaseCommand

from acmin.models import User, Group
from demo.models import Province, City, Area, Address, Author, Book, Member, Order


class Command(BaseCommand):
    """
        python manage.py initdata
    """

    @staticmethod
    def import_area():
        file = settings.BASE_DIR + "/demo/data/area.json"
        with open(file, "r", encoding="UTF-8") as f:
            data = json.load(f)
            Province.objects.bulk_create([Province(code=code, name=obj.get("name")) for code, obj in data.items()])
            provinces = {o.code: o for o in Province.objects.all()}
            City.objects.bulk_create([City(province=provinces[pc], code=cc, name=co["name"]) for pc, po in data.items() for cc, co in (po["child"] or {}).items()])
            cities = {o.code: o for o in City.objects.all()}
            Area.objects.bulk_create([Area(city=cities[cc], code=ac, name=name) for pc, po in data.items() for cc, co in (po["child"] or {}).items() for ac, name in (co["child"] or {}).items()])

    def handle(self, *args, **options):

        for model in [Province, City, Area, Address, Author, Book, Member, Order]:
            model.objects.all().delete()

        group = Group.objects.update_or_create(name="员工")[0]

        def create_user(name):
            user = User.objects.filter(username=name).first()
            if not user:
                user = User(group=group, username=name, title=name)
                user.set_password("123456")
                user.save()
            return user

        user1 = create_user("user1")
        user2 = create_user("user2")
        self.import_area()
        # author = Author.objects.create(address=address, name="令将")
        # book = Book.objects.create(author=author, name="陈天故事", price=12)
        # member1 = Member.objects.create(name="M1")
        # member2 = Member.objects.create(name="M2")
        # Order.objects.create(follower=user1, address=address, member=member1, book=book, amount=2)
        # Order.objects.create(follower=user2, address=address, member=member2, book=book, amount=2)
        # print("ok")
