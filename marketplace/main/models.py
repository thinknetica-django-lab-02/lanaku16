from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
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
    seller_name = models.CharField(max_length=50, unique=True, help_text="Введите наименование организации",
                                   verbose_name="Наименование организации")
    mode = models.CharField(max_length=50, help_text="Введите форму организации",
                            verbose_name="Форма организации")  # ИП, Самозанятый и тд
    inn = models.CharField(max_length=12, unique=True, help_text="Введите ИНН организации",
                           verbose_name="ИНН организации")  # функция проверки ИНН
    boss_name = models.CharField(max_length=50, help_text="Введите ФИО руководителя", verbose_name="ФИО руководителя")
    okpo = models.CharField(max_length=8, unique=True, help_text="Введите ОКПО организации", verbose_name="ОКПО организации")
    ogrnip = models.CharField(max_length=13, unique=True, help_text="Введите ОГРНИП организации", verbose_name="ОГРНИП организации")
    email = models.EmailField(max_length=50, unique=True, help_text="Введите e-mail организации", verbose_name="e-mail организации")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    user = models.ForeignKey(to='auth.user', blank=True, default=None, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ["id"]
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"

    def __str__(self) -> str:
        return self.seller_name

    def get_user_id(self):
        return self.user


class Tag(models.Model):
    """ Тэг """
    tag_name = models.CharField(max_length=20, unique=True, help_text="Введите наименование тега", verbose_name="Наименование тега")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return self.tag_name

    def get_all_tags(self):
        return self.objects.all()

    class Meta:
        ordering = ["id"]
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Category(models.Model):
    """ Категория """
    category_name = models.CharField(max_length=50, unique=True, help_text="Введите наименование категории",
                                     verbose_name="Наименование категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    favorite = models.BooleanField(verbose_name="Избранное", default=False)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self) -> str:
        return self.category_name

    def get_all_categories(self):
        return self.objects.all()

    def get_category_by_pk(self, pk):
        try:
            return self.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get_count_goods_in_category(self, pk):
        goods_set = Good.objects.filter(category=pk)
        i = 0
        for good in goods_set:
            i += 1
        return i

    class Meta:
        ordering = ["id"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Good(models.Model):
    """ Товар """
    good_name = models.CharField(max_length=30, help_text="Введите наименование товара", unique=True,
                                 verbose_name="Наименование товара")
    description = models.TextField(max_length=255, help_text="Введите описание товара", verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")  # 999 999.99
    discount = models.IntegerField(verbose_name="Скидка %")  # от 0 до 100
    brand = models.CharField(max_length=30, help_text="Введите бренд товара",
                             verbose_name="Бренд")  # в будущем отдельная таблица
    color = models.CharField(max_length=15, help_text="Введите цвет товара",
                             verbose_name="Цвет")  # в будущем отдельная таблица
    composition = models.CharField(max_length=50, help_text="Введите состав товара", verbose_name="Состав")
    good_shifr = models.CharField(max_length=12, unique=True, help_text="Введите артикул товара", verbose_name="Артикул")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    tag = ArrayField(models.CharField(max_length=40, blank=True, null=True), blank=True, null=True)
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True, verbose_name="Продавец")  # должно привязываться автоматически
    in_stock = models.PositiveIntegerField(verbose_name="Количество товара на складе")
    is_published = models.BooleanField(verbose_name="Опубликован", default=True)
    archive = models.BooleanField(verbose_name="В архиве", default=False)
    favorite = models.BooleanField(verbose_name="Избранное", default=False)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    picture = models.ImageField(upload_to="images/", verbose_name="Картинка")

    class Meta:
        ordering = ["id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.good_name

    def get_absolute_url(self) -> str:
        return reverse('good-detail', args=[str(self.id)])

    def get_in_stock(self):
        return self.in_stock

    def get_all_goods(self):
        return self.objects.all()

    def get_good_by_pk(self, pk):
        try:
            return self.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None


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


class SMSLog(models.Model):
    """Логи отправки смс"""
    body = models.IntegerField()
    from_number = models.CharField(max_length=30)
    to_number = models.CharField(max_length=30)
    status_response = models.CharField(max_length=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(auto_now_add=True)


class GoodView(models.Model):
    """ Представление для отображения инфомарции по товару """
    good_name = models.CharField(max_length=30, help_text="Введите наименование товара", unique=True,
                                 verbose_name="Наименование товара")
    description = models.TextField(max_length=255, help_text="Введите описание товара", verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")  # 999 999.99
    discount = models.IntegerField(verbose_name="Скидка %")  # от 0 до 100
    brand = models.CharField(max_length=30, help_text="Введите бренд товара",
                             verbose_name="Бренд")  # в будущем отдельная таблица
    color = models.CharField(max_length=15, help_text="Введите цвет товара",
                             verbose_name="Цвет")  # в будущем отдельная таблица
    composition = models.CharField(max_length=50, help_text="Введите состав товара", verbose_name="Состав")
    good_shifr = models.CharField(max_length=12, unique=True, help_text="Введите артикул товара", verbose_name="Артикул")
    picture = models.ImageField(upload_to="images/", verbose_name="Картинка")
    category_name = models.CharField(max_length=50, unique=True, help_text="Введите наименование категории",
                                     verbose_name="Наименование категории")
    seller_name = models.CharField(max_length=50, unique=True, help_text="Введите наименование организации",
                                   verbose_name="Наименование организации")

    class Meta:
        managed = False
        db_table = 'good_view'