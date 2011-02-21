# -*- encoding: utf-8 -*-
from string import join
#TODO
#from PIL import Image as PImage
from os.path import join as pjoin

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from settings import MEDIA_URL
from models import *


# class ProfileForm(ModelForm):
#     class Meta:
#         model = UserProfile
#         exclude = ["posts", "user"]

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

@login_required
def forum_view(request):
    """Listing of threads in a forum."""
    threads = Thread.objects.all().order_by("-created")
    threads = mk_paginator(request, threads, 20)
    return render_to_response("forum.html", add_csrf(request, threads=threads))

@login_required
def thread_view(request, pk):
    """Listing of posts in a thread."""
    posts = ForumPost.objects.filter(thread=pk).order_by("created")
    posts = mk_paginator(request, posts, 15)
    t = Thread.objects.get(pk=pk)
    return render_to_response("thread.html", add_csrf(request, posts=posts, pk=pk, title=t.title,
                                                      media_url=MEDIA_URL))

# @login_required
# def profile(request, pk):
#     """Edit user profile."""
#     profile = UserProfile.objects.get(user=pk)
#     img = None

#     if request.method == "POST":
#         pf = ProfileForm(request.POST, request.FILES, instance=profile)
#         if pf.is_valid():
#             pf.save()
#             # resize and save image under same filename
#             # imfn = pjoin(MEDIA_ROOT, profile.avatar.name)
#             # TODO
#             # im = PImage.open(imfn)
#             # im.thumbnail((160,160), PImage.ANTIALIAS)
#             # im.save(imfn, "JPEG")
#     else:
#         pf = ProfileForm(instance=profile)

#     if profile.avatar:
#         img = "/media/" + profile.avatar.name
#     return render_to_response("profile.html", add_csrf(request, pf=pf, img=img))

@login_required
def post(request, ptype, pk):
    """Display a post form."""
    if ptype == "new_thread":
        action = reverse(new_thread)
        title = u"Начало новой темы"
        subject = ''
    elif ptype == "reply":
        action = reverse(reply, args=[pk])
        title = u"Ответ"
        subject = "Re: " + Thread.objects.get(pk=pk).title

    return render_to_response("forum_post.html", add_csrf(request, subject=subject, action=action,
                                                          title=title))

def increment_post_counter(request):
    None
    # profile = request.user.userprofile_set.all()[0]
    # profile.posts += 1
    # profile.save()

@login_required
def new_thread(request):
    """Start a new thread."""
    p = request.POST
    if p["subject"] and p["body"]:
        thread = Thread.objects.create(title=p["subject"], creator=request.user)
        ForumPost.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse(forum_view))

@login_required
def reply(request, pk):
    """Reply to a thread."""
    p = request.POST
    if p["body"]:
        thread = Thread.objects.get(pk=pk)
        post = ForumPost.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse(thread_view, args=[pk]) + "?page=last")


def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d
