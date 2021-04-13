from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from django.db.models import signals
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging


logger = logging.getLogger(__name__)


class Seller(models.Model):
    """ Продавец """
    seller_name = models.CharField(max_length=50, help_text="Введите наименование организации",
                                   verbose_name="Наименование организации")
    mode = models.CharField(max_length=50, help_text="Введите форму организации",
                            verbose_name="Форма организации")  # ИП, Самозанятый и тд
    inn = models.CharField(max_length=12, help_text="Введите ИНН организации",
                           verbose_name="ИНН организации")  # функция проверки ИНН
    boss_name = models.CharField(max_length=50, help_text="Введите ФИО руководителя", verbose_name="ФИО руководителя")
    okpo = models.CharField(max_length=8, help_text="Введите ОКПО организации", verbose_name="ОКПО организации")
    ogrnip = models.CharField(max_length=13, help_text="Введите ОГРНИП организации", verbose_name="ОГРНИП организации")
    email = models.EmailField(max_length=50, help_text="Введите e-mail организации", verbose_name="e-mail организации")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.seller_name


class Tag(models.Model):
    """ Тэг """
    tag_name = models.CharField(max_length=20, help_text="Введите наименование тега", verbose_name="Наименование тега")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    """ Категория """
    category_name = models.CharField(max_length=50, help_text="Введите наименование категории",
                                     verbose_name="Наименование категории")
    slug = models.SlugField(verbose_name="Слаг")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.category_name


class Good(models.Model):
    """ Товар """
    good_name = models.CharField(max_length=30, help_text="Введите наименование товара",
                                 verbose_name="Наименование товара")
    description = models.CharField(max_length=255, help_text="Введите описание товара", verbose_name="Описание")
    picture = models.ImageField(upload_to="images/", verbose_name="Картинка")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")  # 999 999.99
    discount = models.IntegerField(verbose_name="Скидка %")  # от 0 до 100
    brand = models.CharField(max_length=30, help_text="Введите бренд товара",
                             verbose_name="Бренд")  # в будущем отдельная таблица
    color = models.CharField(max_length=15, help_text="Введите цвет товара",
                             verbose_name="Цвет")  # в будущем отдельная таблица
    composition = models.CharField(max_length=50, help_text="Введите состав товара", verbose_name="Состав")
    good_shifr = models.CharField(max_length=12, help_text="Введите артикул товара", verbose_name="Артикул")
    slug = models.SlugField(verbose_name="Слаг")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, help_text="Добавьте теги для товара")
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True)  # должно привязываться автоматически
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ["good_name"]
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.good_name

    def get_absolute_url(self):
        return reverse('good-detail', args=[str(self.id)])


class Profile(models.Model):
    """Профиль"""
    user = models.OneToOneField(auto_created=True, on_delete=models.CASCADE, parent_link=True,
                                primary_key=True, serialize=False, to='auth.user')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    picture = models.ImageField(upload_to="users/", verbose_name='Аватар', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Subscriber(models.Model):
    """Подписчики"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    # @receiver(post_save, sender=Good)
    # def go_subscrib(sender, instance, created, self, **kwargs):
    #     if created:
    #         title = instance.good_name.encode('utf-8')
    #         for subscrib_user in Subscriber.objects.all():
    #             user = User.objects.get(id=subscrib_user.user_id)
    #             logger.info("Отправка email")
    #             logger.warning("Пользователь: %s" % user)
    #             to_email = user.email
    #             logger.warning("Почта %s " % to_email)
    #             subject = 'Новый товар на сайте'
    #             html_content = '<p><i>Здравствуйте</i></p>'
    #             html_content += 'Новый товар: <a href="http://127.0.0.1:8000/main/goods/%s">%s</a>' % (instance.id, title)
    #             html_content += '<p><i>Всего доброго.</i></p>'
    #             from_email = 'admin@marketplace.ru'
    #             email = EmailMessage(subject, html_content, from_email, [to_email])
    #             email.content_subtype = "html"
    #             email.send()
    #             logger.warning("Email отправлен")
