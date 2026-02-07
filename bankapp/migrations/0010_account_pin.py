from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0009_alter_account_id_alter_creditcarddeposit_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='pin',
            field=models.CharField(default='2027', max_length=10),
        ),
    ]
