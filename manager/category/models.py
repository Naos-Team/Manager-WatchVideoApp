from django.db import models

# Create your models here.
class TblCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100, db_collation='utf8_unicode_ci')
    cat_image = models.TextField(db_collation='utf8_unicode_ci')
    cat_type = models.IntegerField()
    cat_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_category'
