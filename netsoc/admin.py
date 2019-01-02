from django.contrib import admin
from netsoc.models import User,post,comment,user_profile
# Register your models here.

admin.site.register(post)
admin.site.register(comment)
admin.site.register(user_profile)
