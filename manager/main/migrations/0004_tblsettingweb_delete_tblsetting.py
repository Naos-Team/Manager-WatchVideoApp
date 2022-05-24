# Generated by Django 4.0.4 on 2022-05-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_tblsetting_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblSettingWeb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ads_key_banner', models.TextField()),
                ('ads_key_interstial', models.TextField()),
                ('ad_display_count', models.IntegerField()),
                ('ads_key_openads', models.TextField()),
                ('arr_trend', models.TextField()),
            ],
            options={
                'db_table': 'tbl_setting_web',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='TblSetting',
        ),
    ]
