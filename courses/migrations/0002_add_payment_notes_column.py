
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE core_paymentinstallment ADD COLUMN payment_notes TEXT DEFAULT '';",
            reverse_sql="ALTER TABLE core_paymentinstallment DROP COLUMN payment_notes;"
        ),
    ]
