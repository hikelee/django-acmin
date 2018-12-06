import json

from django.conf import settings
from django.core.management.base import BaseCommand

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

        self.import_area()
