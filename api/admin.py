from django.contrib import admin

from .models import Bucket, AssetCategory, AssetType, Sex, User, Asset

# Register your models here.


class BucketAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['name']
        }),
        ('Code', {
            'fields': ['code']
        })
    ]


admin.site.register(Bucket, BucketAdmin)
admin.site.register(AssetCategory)
admin.site.register(AssetType)
admin.site.register(User)
admin.site.register(Asset)
