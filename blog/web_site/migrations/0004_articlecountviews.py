# Generated by Django 5.0.1 on 2024-01-15 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCountViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=150)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_site.article')),
            ],
        ),
    ]
