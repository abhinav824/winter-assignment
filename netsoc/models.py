from django.db import models

from django.contrib.auth.models import User
#inbuilt user model in django


class post(models.Model):
#model for posts
    post_text=models.TextField(max_length=200)
    post_date=models.DateTimeField('date_published')
    post_user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.post_text

class comment(models.Model):
#model for comment
    comment_text=models.CharField(max_length=100)
    comment_user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment_post=models.ForeignKey(post,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

class user_profile(models.Model):
    '''User profile for every user'''

    def user_directory_path(instance,filename):
        return "user_{0}/{1}".format(instance.user.id,filename)


    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name="profile_user")
    following=models.ManyToManyField(User,related_name='follower_user')
    picture=models.ImageField(upload_to=user_directory_path,blank=True)
    description=models.CharField(max_length=200,blank=True)
    date_of_birth=models.DateField()
    gen_choice=(('M',"Male"),('F',"Female"),('O',"Other"))
    gender=models.CharField(max_length=1,choices=gen_choice,default=None)
    subscribers=models.ManyToManyField(User,related_name='subscribed')


    def __str__(self):
        return self.user.username
