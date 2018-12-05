import json

from django.conf import settings
from django.core.management.base import BaseCommand

from acmin.models import User, Group
from demo.models import Province, City, Area, Address, Author, Book, Member, Order


class Command(BaseCommand):
    """
        python manage.py initdata
    """

    def import_area(self):
        file = settings.BASE_DIR + "/demo/data/area.json"
        with open(file, "r", encoding="UTF-8") as f:
            for province_code, province_obj in json.load(f).items():
                province = Province.objects.create(code=province_code, name=province_obj.get("name"))
                cities = province_obj["child"]
                if cities:
                    for city_code, city_obj in cities.items():
                        city = City.objects.create(province=province, code=city_code, name=city_obj["name"])
                        areaes = city_obj["child"]
                        if areaes:
                            area_array = []
                            for area_code, area_name in areaes.items():
                                area_array.append(Area(city=city, code=area_code, name=area_name))
                                Area.objects.bulk_create(area_array)

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
