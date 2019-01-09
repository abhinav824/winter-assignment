from django.contrib import admin
from netsoc.models import User,post,comment,user_profile
# Register your models here.

class commentInline(admin.StackedInline):
    extra = 2
    model = comment

class user_profileInline(admin.StackedInline):
    model=user_profile

class postInline(admin.StackedInline):
    model=post
    extra =2


class postAdmin(admin.ModelAdmin):
    inlines=[commentInline]
    pass

class user_profileAdmin(admin.ModelAdmin):
    pass

class commentAdmin(admin.ModelAdmin):
    pass

class NewUserAdmin(admin.ModelAdmin):
    inlines = [user_profileInline,postInline]

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
admin.site.register(post,postAdmin)

admin.site.register(user_profile,user_profileAdmin)
admin.site.register(comment,commentAdmin)
