from rest_framework import routers
from myblog.views import PostViewSet

posts_router = routers.DefaultRouter()
posts_router.register("myblog", viewset=PostViewSet, basename="myblog")
