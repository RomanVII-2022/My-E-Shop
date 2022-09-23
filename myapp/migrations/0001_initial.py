# Generated by Django 4.1.1 on 2022-09-17 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField()),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=Hidden')),
                ('trending', models.BooleanField(default=False, help_text='0=default, 1=Trending')),
                ('meta_title', models.CharField(max_length=200)),
                ('meta_keywords', models.CharField(max_length=200)),
                ('meta_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]