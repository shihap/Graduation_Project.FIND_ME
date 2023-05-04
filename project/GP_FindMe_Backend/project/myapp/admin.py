from django.contrib import admin
from .models import user , relatives , images_dataset , post , notfications
# Register your models here.

admin.site.register(user)
admin.site.register(relatives)
admin.site.register(images_dataset)
admin.site.register(post)
admin.site.register(notfications)