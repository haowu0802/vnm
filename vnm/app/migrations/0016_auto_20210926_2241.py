# Generated by Django 3.2.4 on 2021-09-26 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20210926_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actorimagelocal',
            options={'ordering': ['filepath']},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['filepath']},
        ),
        migrations.AlterField(
            model_name='actorimage',
            name='actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.actor'),
        ),
        migrations.AlterField(
            model_name='actorimagelocal',
            name='story',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.story'),
        ),
        migrations.AlterField(
            model_name='story',
            name='actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.actor'),
        ),
    ]
