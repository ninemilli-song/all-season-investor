from django.contrib import admin

from .models import Bucket, AssetCategory, AssetType, Sex, User, Asset, Investor, UserLoginActivity

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


class UserLoginActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bucket, BucketAdmin)
admin.site.register(AssetCategory)
admin.site.register(AssetType)
# admin.site.register(User)
admin.site.register(Investor)
admin.site.register(Asset)
admin.site.register(UserLoginActivity, UserLoginActivityAdmin)
