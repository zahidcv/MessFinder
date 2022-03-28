# Generated by Django 4.0.2 on 2022-03-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_customuser_is_student_alter_room_floor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomimages',
            name='room',
        ),
        migrations.AddField(
            model_name='mess',
            name='image1',
            field=models.ImageField(null=True, upload_to='Room_Gallery'),
        ),
        migrations.AddField(
            model_name='mess',
            name='image2',
            field=models.ImageField(null=True, upload_to='Room_Gallery'),
        ),
        migrations.AddField(
            model_name='mess',
            name='image3',
            field=models.ImageField(null=True, upload_to='Room_Gallery'),
        ),
        migrations.AddField(
            model_name='room',
            name='image1',
            field=models.ImageField(null=True, upload_to='Room_Gallery'),
        ),
        migrations.AddField(
            model_name='room',
            name='image2',
            field=models.ImageField(null=True, upload_to='Room_Gallery'),
        ),
        migrations.AddField(
            model_name='room',
            name='image3',
            field=models.ImageField(null=True, upload_to='Room_Gallery'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile/'),
        ),
        migrations.DeleteModel(
            name='MessImages',
        ),
        migrations.DeleteModel(
            name='RoomImages',
        ),
    ]