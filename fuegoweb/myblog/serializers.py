from rest_framework import serializers
from myblog.models import Posts


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["post_id", "description", "image_path", "updated_time", "user_id"]
