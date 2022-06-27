# Generated by Django 3.2.4 on 2022-06-21 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drevo', '0016_author_subscribers'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryExpert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.ManyToManyField(related_name='category_list', to='drevo.Category', verbose_name='Список категорий')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expert', to=settings.AUTH_USER_MODEL, verbose_name='Эксперт')),
            ],
            options={
                'verbose_name': 'Эксперта',
                'verbose_name_plural': 'Эксперты',
            },
        ),
    ]