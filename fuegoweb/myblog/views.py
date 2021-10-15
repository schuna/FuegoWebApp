from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from myblog.serializers import PostsSerializer
from myblog.models import Posts


class PostViewSet(ModelViewSet):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all().order_by("-updated_time")
    pagenation_class = PageNumberPagination
