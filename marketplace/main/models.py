from django.db import models
from django.urls import reverse


""" Продавец """
class Seller(models.Model):
    seller_name = models.CharField(max_length=50, help_text="Введите наименование организации", verbose_name="Наименование организации")
    mode = models.CharField(max_length=50, help_text="Введите форму организации", verbose_name="Форма организации") # ИП, Самозанятый и тд
    INN = models.CharField(max_length=12, help_text="Введите ИНН организации", verbose_name="ИНН организации") # функция проверки ИНН
    Boss_name = models.CharField(max_length=50, help_text="Введите ФИО руководителя", verbose_name="ФИО руководителя")
    OKPO = models.CharField(max_length=8, help_text="Введите ОКПО организации", verbose_name="ОКПО организации")
    OGRNIP = models.CharField(max_length=13, help_text="Введите ОГРНИП организации", verbose_name="ОГРНИП организации")
    email = models.EmailField(max_length=50, help_text="Введите e-mail организации", verbose_name="e-mail организации")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.seller_name

""" Тэг """
class Tag(models.Model):
    tag_name = models.CharField(max_length=20, help_text="Введите наименование тега", verbose_name="Наименование тега")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.tag_name

""" Категория """
class Category(models.Model):
    category_name = models.CharField(max_length=50, help_text="Введите наименование категории", verbose_name="Наименование категории")
    slug = models.SlugField(verbose_name="Слаг")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.category_name

""" Товар """
class Good(models.Model):
    good_name = models.CharField(max_length=30, help_text="Введите наименование товара", verbose_name="Наименование товара")
    description = models.CharField(max_length=255, help_text="Введите описание товара", verbose_name="Описание")
    picture = models.ImageField(upload_to="images/", verbose_name="Картинка")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")    # 999 999.99
    discount = models.IntegerField(verbose_name="Скидка %")     #от 0 до 100
    brand = models.CharField(max_length=30, help_text="Введите бренд товара", verbose_name="Бренд")     #в будущем отдельная таблица
    color = models.CharField(max_length=15, help_text="Введите цвет товара", verbose_name="Цвет")       #в будущем отдельная таблица
    good_shifr = models.CharField(max_length=12, help_text="Введите артикул товара", verbose_name="Артикул")
    slug = models.SlugField(verbose_name="Слаг")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, help_text="Добавьте теги для товара")
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True)   # должно привязываться автоматически
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ["good_name"]
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.good_name

    def get_absolute_url(self):
        pass
        #return reverse('good-detail', args=[str(self.good_name)])