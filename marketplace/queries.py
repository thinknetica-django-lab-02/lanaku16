from main.models import *
g1 = Good(
    good_name = "Markuss Леггинсы женские",
    description = "Леггинсы женские кожаные. Леггинсы черные из эко-кожи, выполнены из эластичного очень прочного высококачественного материала, что делает носку леггинсов очень комфортной. ",
    picture = "images/",
    price = "1140",
    discount = "0",
    brand = "Markuss",
    color = "черный",
    good_shifr= "19404686",
    slug = "Markuss19404686",
    category_id = 2,
    seller_id = 1)
g1.save()

g2 = Good.objects.create(
    good_name="Колонный вентилятор LED",
    description="Колонный вентилятор Увеличенный поток воздуха и большая площадь обдува Циркулярное движение воздуха LED дисплей с индикацией режимов работы и температуры воздуха в помещении",
    picture="images/",
    price="9889",
    discount="0",
    brand="BRAYER",
    color="белый",
    good_shifr="21660888",
    slug="BRAYER21660888",
    category_id=1,
    seller_id=2)

q1 = Good.objects.filter(category_id = 1)
print(q1)
