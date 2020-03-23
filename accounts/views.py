from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from blog.models import Post
#@verified_email_required
@login_required
def profile(request, pk):
    user  = get_object_or_404(User, pk=pk)
    contents = Post.objects.filter(user=user)
    return render(request, 'registration/profile.html', {'user': user, 'contents': contents})

