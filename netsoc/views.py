from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from . import forms
from django.urls import reverse
from . import models
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from .create_record import record_store
from .resize import get_resized_image
from PIL import Image
from django.core.mail import EmailMultiAlternatives
from . import user_record
from django.http import HttpResponse
# Create your views here.

class new_user(object):

    def create_user(request):
        '''View to display the registration form '''
        if request.method== 'POST':
            form=forms.UserForm(request.POST)
            if form.is_valid():
                user=User
                UP=models.user_profile
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                email=form.cleaned_data['email']
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                gender=form.cleaned_data['gender']
                dob=form.cleaned_data['dob']

                user=User.objects.create_user(username,email,password,first_name=first_name,last_name=last_name)
                UP=models.user_profile(user=user,date_of_birth=dob,gender=gender)
                UP.save()


                return redirect('netsoc:registered')
        else:
            form=forms.UserForm()
            return render(request,'netsoc/new_user.html',{'form':form})

    def user_created(request):
        '''To show the success message after registering a the user'''
        return render(request,'netsoc/user_created.html',{})

class news_feed(object):

    def home(request):
        '''View to display the home page'''
        if request.user.is_authenticated:
        #complete profile of a new user
            if not models.user_profile.objects.filter(user=request.user).exists():
                return redirect('netsoc:profile_completion')

        try:
            list=models.user_profile.objects.get(user=request.user).following.all()
            queryset=list | User.objects.filter(pk=request.user.pk)
            posts=models.post.objects.filter(post_user__in=queryset).order_by('-post_date')
            comments=models.comment.objects.filter(comment_post__in=posts)
            form=forms.CommentForm()

        except:
            return render(request,'netsoc/home.html',{})

        return render(request,'netsoc/home.html',{'post':posts,'comments':comments,'form':form})

    def new_post(request):
        '''view to display form for new post'''
        if request.method=='POST':
            form=forms.PostForm(request.POST)
            if form.is_valid():
                post=form.save(commit=False)
                post.post_text=form.cleaned_data['post_text']
                post.post_date=timezone.now()
                post.post_user=request.user
                post.save()

                recipient_list=[]
                for subscriber in post.post_user.profile_user.subscribers.all():
                    if subscriber.email:
                        recipient_list.append(subscriber.email)
                mail=EmailMultiAlternatives(
                subject="Post Update - NETSOC , {0} Posted Something".format(post.post_user.username),
                body="check this out on NETSOC , \n {0}".format(post.post_text),
                from_email="NETSOC <abhinavtiwari824@gmail.com>",
                to=recipient_list
                )
                mail.send()

                return redirect('netsoc:home')
        else:
            form=forms.PostForm()

            return render(request,'netsoc/new_post.html',{'form':form})

    def user_list(request):
        '''To display list of all users'''
        list=User.objects.all().exclude(username='admin')
        prof_list=models.user_profile.objects.all()

        return render(request,'netsoc/user_list.html',{'list':list,'profiles':prof_list})

class datahandle(object):
    '''views to perform certain tasks like adding a comment , deleteing a comment/post,editing a post ,etc'''
    def save_comment(request,id):

        if request.method=='POST':
            form=forms.CommentForm(request.POST)
            if form.is_valid():
                comment=form.save(commit=False)
                comment.comment_text=form.cleaned_data['comment_text']
                comment.comment_user=request.user
                comment.comment_post=models.post.objects.get(pk=id)
                comment.save()

                return redirect('netsoc:home')

    def delete_comment(request,id):

        if request.user == models.comment.objects.get(pk=id).comment_user:

            instance=models.comment.objects.get(pk=id)
            record_store(instance.id,"comment","delete")
            instance.delete()
            return redirect('netsoc:home')
        else:
            return HttpResponseForbidden('Access Denied')

    def delete_post(request,id):

        if request.user==models.post.objects.get(pk=id).post_user:
            instance=models.post.objects.get(pk=id)
            record_store(instance.id,"post","delete")
            for comments in models.comment.objects.filter(comment_post_id=id):
                record_store(comments.id,"comment","delete")

            instance.delete()
            return redirect('netsoc:home')
        else:
            return HttpResponseForbidden('access Denied')

    def edit_post(request,id):

        if request.user==models.post.objects.get(pk=id).post_user:

            post=models.post.objects.get(pk=id)

            if request.method=='POST':

                form=forms.PostForm(request.POST, instance=post)

                if form.is_valid():
                    record_store(post.id,"post","edit")
                    post=form.save(commit=False)
                    post_user=request.user
                    post_date=timezone.now()
                    post.save()
                    return redirect('netsoc:home')

            else:

                form=forms.PostForm(instance=post)

            return render(request,'netsoc/new_post.html',{'form':form})
        else:
            return HttpResponseForbidden('access Denied')

    def followreq(request,id):

        user_req=models.user_profile.objects.get(user=request.user)
        user_foll=User.objects.get(pk=id)
        user_foll_prof=models.user_profile.objects.get(user=user_foll)
        user_req.following.add(user_foll)

        return redirect('netsoc:profile',id)

    def unfollow(request,id):

        user_req_prof=models.user_profile.objects.get(user=request.user)
        user_foll=User.objects.get(pk=id)
        user_foll_prof=models.user_profile.objects.get(user=user_foll)

        user_req_prof.following.remove(user_foll)
        return redirect('netsoc:profile',id)

    def subsreq(request,id):
        if request.user.is_authenticated and request.user.id!=id:

            user=User.objects.get(pk=id)
            user_prof=models.user_profile.objects.get(user=user)
            user_req=request.user
            user_prof.subscribers.add(user_req)

            return redirect('netsoc:profile',id)
        else:

            HttpResponseForbidden('Access Denied , invalid request')

    def unsubsreq(request,id):
        if request.user.is_authenticated and request.user.id!=id:

            user=User.objects.get(pk=id)
            user_prof=models.user_profile.objects.get(user=user)
            user_req=request.user
            user_prof.subscribers.remove(user_req)

            return redirect('netsoc:profile',id)
        else:

            HttpResponseForbidden('Access Denied , invalid request')


    def edit_profile(request,id):

        if request.user == models.user_profile.objects.get(pk=id).user:

            user_prof=models.user_profile.objects.get(pk=id)
            if request.method=="POST":

                form=forms.ProfileForm(request.POST)
                if form.is_valid():

                    request.user.username=form.cleaned_data['username']

                    request.user.email=form.cleaned_data['email']
                    request.user.first_name=form.cleaned_data['first_name']
                    request.user.last_name=form.cleaned_data['last_name']
                    user_prof.gender=form.cleaned_data['gender']
                    user_prof.dob=form.cleaned_data['dob']
                    request.user.save()
                    user_prof.save()

                    return redirect('netsoc:profile',id)

            else:
                prof=models.user_profile.objects.get(user=request.user)
                data={'username':request.user.username,

                      'email':request.user.email,
                      'first_name':request.user.first_name,
                      'last_name':request.user.last_name,
                      'gender':prof.gender,
                      'dob':prof.date_of_birth,}

                form=forms.ProfileForm(initial=data)

                return render(request,'netsoc/edit_profile.html',{'user':request.user,'prof':prof,'form':form})

        else:

            return HttpResponseForbidden('Access Denied')

    def changepassword(request,id):

        if request.user==User.objects.get(pk=id):

            if request.method=='POST':

                form=forms.PasswordChangeForm(request.user,request.POST)

                if form.is_valid():

                    user=form.save()
                    update_session_auth_hash(request,user)
                    messages.success(request,('Your Password was Succesfully Updated !!'))
                    return redirect('netsoc:profile',id)
                else:

                    messages.error(request,('Correct the error below'))
                    return render(request,'netsoc/change_password.html',{'form':form})
            else:

                form=forms.PasswordChangeForm(request.user)
                return render(request,'netsoc/change_password.html',{'form':form})

        else:

            return HttpResponseForbidden('Access Denied')

    def user_record(request):

        if request.user.is_staff or request.user.is_superuser:
            user_record.create()

            return HttpResponse('Exported Succesfully')

        else:

            return HttpResponseForbidden('Only staff members and admins are allowed to access this page')

    def profile_completion(request):

        if request.user.is_authenticated:

            if request.method=="POST":
                form=forms.profile_completion_form(request.POST)

                if form.is_valid():

                    DOB=form.cleaned_data['DOB']
                    gender=form.cleaned_data['gender']
                    profile=models.user_profile(user=request.user,date_of_birth=DOB,gender=gender)
                    profile.save()
                    return redirect('netsoc:home')

            else:

                form=forms.profile_completion_form()
                return render(request,'netsoc/profile_completion.html',{'form':form})
        else:

            return HttpResponseForbidden('Access Denied')

class profile(object):

    def profile_page(request,id):
        '''view to display the profile page of a user'''
        user=User.objects.get(pk=id)
        prof=models.user_profile.objects.get(user=user)
        qu=user.follower_user.all()
        followers =User.objects.filter(profile_user__in=qu)

        posts=user.post_set.all().order_by('-post_date')
        comments=models.comment.objects.all()
        form=forms.CommentForm()

        return render(request,'netsoc/profile_page.html',{'user':user,'prof':prof,'posts':posts,'comments':comments,'form':form,'followers':followers})

    def following(request,id):
        '''To display the list of the users which are followed by the given user'''
        user=User.objects.get(pk=id)
        user_prof=models.user_profile.objects.get(user=user)
        following=user_prof.following.all()

        return render(request,'netsoc/following.html',{'user':user,'following':following})

    def followers(request,id):
        '''to display the list of users who are following the given user'''
        user=User.objects.get(pk=id)
        user_prof=models.user_profile.objects.get(user=user)
        qu=user.follower_user.all()
        followers =User.objects.filter(profile_user__in=qu)


        return render(request,'netsoc/followers.html',{'user':user,'followers':followers})

    def describe(request,id):
        '''user description form'''
        if request.user==User.objects.get(pk=id):

            if request.method=="POST":

                form=forms.DescriptionForm(request.POST)

                if form.is_valid():

                    user_prof=models.user_profile.objects.get(user=request.user)
                    user_prof.description=form.cleaned_data['description']
                    user_prof.save()
                    return redirect('netsoc:profile',id)

            else:
                user_prof=models.user_profile.objects.get(user=request.user)
                form=forms.DescriptionForm(initial={'description':user_prof.description})

                return render(request,'netsoc/description.html',{'form':form,'profile':user_prof})
        else:

            return HttpResponseForbidden('Access Denied')

    def UploadImage(request,id):

        if request.user==User.objects.get(pk=id):

            if request.method=='POST':
                form=forms.ImageForm(request.POST,request.FILES)

                if form.is_valid():
                    user_prof=models.user_profile.objects.get(user=request.user)
                    file=request.FILES['image']
                    user_prof.picture=file
                    user_prof.save()

                    image=get_resized_image(user_prof.picture)
                    image.save(user_prof.picture.path)
                    return redirect('netsoc:profile',id)

                else:

                    messages.error(request,('Please correct the error'))
                    return render(request,'netsoc/UploadImage.html',{'form':form})

            else:

                form=forms.ImageForm()
                messages.error(request,('Please correct the error'))
                return render(request,'netsoc/UploadImage.html',{'form':form})
        else:

            HttpResponseForbidden("Access Denied")

    def get_follower_set(user):
        qu=user.follower_user.all()
        followers =User.objects.filter(profile_user__in=qu)
        return followers
