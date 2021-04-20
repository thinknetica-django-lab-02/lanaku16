from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from main.models import Good

import pytest

client = Client()


@pytest.mark.django_db
@pytest.mark.parametrize('name',
                         ['home', 'about', 'contacts', 'delivery', 'pay'])
def test_simplepagesview_by_name(name):
    """Тестирование простых страниц"""
    url = reverse(name)
    response = client.get(url)
    assert (response.status_code, 200)


@pytest.mark.django_db
@pytest.mark.parametrize('name, code, need_args',
                         [('good-update', 320, True),
                          ('good-add', 302, False),
                          ('good-detail', 200, True),
                          ('goods', 200, False)])
def test_goodviews_by_name(name, code, need_args):
    """Тестирование детального просмотра и добавления/редактирования товара"""
    obj_id = Good.objects.create(good_name="good test1",
                                     description="good test1",
                                     picture="images/17679636.jpg",
                                     price="9889",
                                     discount="0",
                                     brand="BRAYER",
                                     color="белый",
                                     good_shifr="21660888",
                                     slug="BRAYER21660888").pk
    obj_id2 = Good.objects.create(good_name="good test2",
                                      description="good test2",
                                      picture="images/17679636.jpg",
                                      price="9889",
                                      discount="0",
                                      brand="BRAYER",
                                      color="белый",
                                      good_shifr="21660888",
                                      slug="BRAYER21660888").pk
    good = Good.objects.get(id=obj_id)

    if need_args == True:
        url = reverse(name, args=[good.id])
    else:
        url = reverse(name)

    resp = client.get(url)
    assert(resp.status_code, code)


@pytest.mark.django_db
@pytest.mark.parametrize('name, code, need_args',
                         [('login', 200, False),
                          ('register', 200, False),
                          ('logout', 200, False),
                          ('update-profile', 302, True)])
def test_useraccountviews_by_name(name, code, need_args):
    """Тестирование аккаунта пользователя"""
    obj_id = User.objects.create(username='testuser',
                                 email='foo@example.com',
                                 first_name='Test',
                                 last_name='User').pk

    user = User.objects.get(id=obj_id)

    if need_args == True:
        url = reverse(name, args=[user.id])
    else:
        url = reverse(name)

    resp = client.get(url)
    assert(resp.status_code, code)