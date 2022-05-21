from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.TblFav)
admin.site.register(models.TblComment)
admin.site.register(models.TblCategory)
admin.site.register(models.TblRating)
admin.site.register(models.TblReport)
admin.site.register(models.TblUsers)
admin.site.register(models.TblVideo)
