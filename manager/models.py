# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TblCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100, db_collation='utf8_unicode_ci')
    cat_image = models.TextField(db_collation='utf8_unicode_ci')
    cat_type = models.IntegerField()
    cat_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_category'


class TblComment(models.Model):
    cmt_id = models.AutoField(primary_key=True)
    vid = models.ForeignKey('TblVideo', models.DO_NOTHING)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    cmt_time = models.DateTimeField()
    cmt_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'tbl_comment'


class TblFav(models.Model):
    vid = models.OneToOneField('TblVideo', models.DO_NOTHING, primary_key=True)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    is_fav = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_fav'
        unique_together = (('vid', 'uid'),)


class TblRating(models.Model):
    vid = models.OneToOneField('TblVideo', models.DO_NOTHING, primary_key=True)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    rate_score = models.IntegerField()
    rate_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_rating'
        unique_together = (('vid', 'uid'),)


class TblReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='uid')
    vid = models.ForeignKey('TblVideo', models.DO_NOTHING)
    report_content = models.TextField()
    report_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_report'


class TblUsers(models.Model):
    uid = models.CharField(primary_key=True, max_length=100, db_collation='utf8_unicode_ci')

    class Meta:
        managed = False
        db_table = 'tbl_users'


class TblVideo(models.Model):
    vid_id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(TblCategory, models.DO_NOTHING)
    vid_title = models.CharField(max_length=500, db_collation='utf8_unicode_ci')
    vid_url = models.TextField(db_collation='utf8_unicode_ci')
    vid_thumbnail = models.TextField(db_collation='utf8_unicode_ci')
    vid_description = models.TextField(db_collation='utf8_unicode_ci')
    vid_view = models.IntegerField()
    vid_duration = models.IntegerField()
    vid_time = models.DateTimeField()
    vid_avg_rate = models.FloatField()
    vid_status = models.IntegerField()
    vid_type = models.IntegerField()
    vid_is_premium = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_video'
