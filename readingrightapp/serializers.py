from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('userId','id','title','body')

class PostjsonSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=500)
    class Meta:
        fields = ('userId','id','title','body')