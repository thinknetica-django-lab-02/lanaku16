from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    sql = """
    CREATE OR REPLACE VIEW good_view AS
      SELECT a.good_name, a.description, a.price, a.discount, a.brand, a.color, a.composition, a.good_shifr, a.picture,
        b.category_name, c.seller_name 
        FROM Good AS a  
        LEFT JOIN Category AS b ON a.category_id = b.id
        LEFT JOIN Seller AS c ON a.seller_id = c.id
        ORDER BY a.id
    """

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS good_view ;'),
        migrations.RunSQL(sql)
    ]