from django.core.management.base import BaseCommand, CommandError
from main.models import Good, Category, Seller, Tag

import factory
from factory.faker import faker
from faker import Faker


fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        tag = 'test tag'
        new_tag = Tag.objects.create(tag_name=tag).pk

        cat = 'test cat'
        new_cat = Category.objects.create(category_name=cat,
                                          slug=cat).pk

        new_seller = Seller.objects.create(seller_name='test seller',
                                           mode='test',
                                           inn=str(factory.Faker._get_faker().random_int()),
                                           boss_name=factory.Faker('last_name'),
                                           okpo=str(factory.Faker._get_faker().random_int()),
                                           ogrnip=str(factory.Faker._get_faker().random_int()),
                                           email='test@test.ru',
                                           user_id=None
                                           ).pk

        new_good = Good.objects.create(good_name='test',
                                       description='test',
                                       picture='images/test.img',
                                       price=factory.Faker._get_faker().random_int(),
                                       discount=0,
                                       brand='test brand',
                                       color='test',
                                       composition='test',
                                       good_shifr=str(factory.Faker._get_faker().random_int()),
                                       category_id=new_cat,
                                       seller_id=new_seller,
                                       in_stock=0
                                       ).pk

        through_objs = [
            Good.tag.through(
                good_id=new_good,
                tag_id=new_tag,
            ),]

        Good.tag.through.objects.bulk_create(through_objs)




