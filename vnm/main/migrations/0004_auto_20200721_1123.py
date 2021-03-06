# Generated by Django 2.2.6 on 2020-07-21 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200721_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='matcher',
        ),
        migrations.RemoveField(
            model_name='novel',
            name='actors',
        ),
        migrations.CreateModel(
            name='Matcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.CharField(blank=True, max_length=256, null=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Actor')),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Novel')),
            ],
        ),
    ]
