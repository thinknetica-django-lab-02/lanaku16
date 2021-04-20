from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from main.models import Good

client = Client()


class SimplePagesTestCase(TestCase):
    """Тестирование простых страниц"""
    def test_view_url_accessible_by_name(self):
        names = ['home', 'about', 'contacts', 'delivery', 'pay']
        for name in names:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


class GoodViewsTestCase(TestCase):
    """Тестирование детального просмотра и добавления/редактирования товара"""
    @classmethod
    def setUpTestData(cls):
        cls.obj_id = Good.objects.create(good_name="good test1",
                                         description="good test1",
                                         picture="images/17679636.jpg",
                                         price="9889",
                                         discount="0",
                                         brand="BRAYER",
                                         color="белый",
                                         good_shifr="21660888",
                                         slug="BRAYER21660888").pk
        cls.obj_id2 = Good.objects.create(good_name="good test2",
                                          description="good test2",
                                          picture="images/17679636.jpg",
                                          price="9889",
                                          discount="0",
                                          brand="BRAYER",
                                          color="белый",
                                          good_shifr="21660888",
                                          slug="BRAYER21660888").pk

    def test_view_url_accessible_by_name(self):
        good = Good.objects.get(id=self.obj_id)

        url = reverse('good-update', args=[good.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

        url = reverse('good-add')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

        url = reverse('good-detail', args=[good.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        url = reverse('goods')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class UserAccountTestCase(TestCase):
    """Тестирование аккаунта пользователя"""
    @classmethod
    def setUpTestData(cls):
        cls.obj_id = User.objects.create(username= 'testuser',
                                         email= 'foo@example.com',
                                         first_name= 'Test',
                                         last_name= 'User').pk

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'username': 'foo',
                'password': 'bar'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(id=self.obj_id)
        url = reverse('update-profile', args=[user.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
