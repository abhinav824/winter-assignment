from netsoc.models import User,user_profile
for u in User.objects.all():
    for y in User.objects.all():
        up=user_profile.objects.get(user=u)
        yp=user_profile.objects.get(user=y)
        if y in up.following.all():
            yp.followers.add(u)
