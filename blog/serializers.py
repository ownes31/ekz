from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'created_at', 'author']
        read_only_fields = ['id', 'created_at', 'author', 'post']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Комментарий не может быть пустым.")
        return value

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'comments']
        read_only_fields = ['id', 'created_at', 'author', 'comments']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Заголовок не может быть пустым.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст поста не может быть пустым.")
        return value