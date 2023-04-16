# Generated by Django 3.2.18 on 2023-04-16 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FashionProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=200, verbose_name='gender')),
                ('masterCategory', models.CharField(max_length=200, verbose_name='masterCategory')),
                ('subCategory', models.CharField(max_length=200, verbose_name='subCategory')),
                ('articleType', models.CharField(max_length=200, verbose_name='articleType')),
                ('baseColour', models.CharField(max_length=200, verbose_name='baseColour')),
                ('season', models.CharField(max_length=200, verbose_name='season')),
                ('year', models.CharField(max_length=200, verbose_name='year')),
                ('usage', models.CharField(max_length=200, verbose_name='usage')),
                ('productDisplayName', models.CharField(max_length=200, verbose_name='productDisplayName')),
                ('imagePath', models.CharField(max_length=200, verbose_name='imagePath')),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('masterCategory', models.CharField(blank=True, max_length=200, null=True)),
                ('subCategory', models.CharField(blank=True, max_length=200, null=True)),
                ('articleType', models.CharField(blank=True, max_length=200, null=True)),
                ('baseColour', models.CharField(blank=True, max_length=200, null=True)),
                ('season', models.CharField(blank=True, max_length=200, null=True)),
                ('year', models.CharField(blank=True, max_length=200, null=True)),
                ('usage', models.CharField(blank=True, max_length=200, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_preference', to='style.account')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=500, null=True)),
                ('masterCategory', models.CharField(max_length=200, null=True)),
                ('related_product_masterCategory', models.CharField(max_length=200, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='style.fashionproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='style.account')),
            ],
        ),
        migrations.CreateModel(
            name='LikeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('masterCategory', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('superliked', models.BooleanField(default=False)),
                ('likes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='style.likes')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='style.fashionproduct')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='preferences',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_preferences', to='style.userpreference'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
