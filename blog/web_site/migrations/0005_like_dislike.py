# Generated by Django 4.2.8 on 2024-01-22 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_site', '0004_articlecountviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='web_site.article')),
                ('comment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='web_site.comment')),
                ('user', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='web_site.article')),
                ('comment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='web_site.comment')),
                ('user', models.ManyToManyField(related_name='dislikes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]