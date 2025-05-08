"""
URL configuration for miniblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions, viewsets
from blog.permissions import IsAuthorOrReadOnly  # Import the missing permission class

class PostViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    # ...

class CommentViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    # ...

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('api-auth/', TemplateView.as_view(template_name='api_auth.html')),
    path('create-post/', TemplateView.as_view(template_name='create_post.html')),
    path('my-posts/', TemplateView.as_view(template_name='my_posts.html')),
    path('add-comment/', TemplateView.as_view(template_name='add_comment.html')),
    path('my-comments/', TemplateView.as_view(template_name='my_comments.html')),
]
