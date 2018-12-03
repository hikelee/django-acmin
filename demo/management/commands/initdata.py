from django.core.management.base import BaseCommand

from acmin.models import User, Group
from demo.models import Province, City, Area, Address, Author, Book, Member, Order


class Command(BaseCommand):
    """
        python manage.py initdata
    """

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

        province = Province.objects.create(name="广东省")
        city = City.objects.create(province=province, name="深圳市")
        area = Area.objects.create(city=city, name="南山区")
        address = Address.objects.create(area=area, detail="科技园")
        author = Author.objects.create(address=address, name="令将")
        book = Book.objects.create(author=author, name="陈天故事", price=12)
        member1 = Member.objects.create(name="M1")
        member2 = Member.objects.create(name="M2")
        Order.objects.create(follower=user1, address=address, member=member1, book=book, amount=2)
        Order.objects.create(follower=user2, address=address, member=member2, book=book, amount=2)
        print("ok")
