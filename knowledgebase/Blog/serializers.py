from csv import excel
from dataclasses import field
from pyexpat import model
from rest_framework import serializers 
from .models import Category, Post,  Comment, User
from django.contrib.auth.hashers import make_password

class PostSerializer(serializers.ModelSerializer):
    comment = serializers.StringRelatedField(many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.name

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = Post
        exclude = []
        extra_field = ['comment']


class CategorySerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model= Category
        fields = '__all__'
        extra_field = ['post']


class CommentSerializer(serializers.ModelSerializer):
    comment_made_by = serializers.SerializerMethodField()
    post_name = serializers.SerializerMethodField()

    def get_comment_made_by(self, obj):
        return obj.commented_by.username

    def get_post_name(self, obj):
        print(obj.post.title)
        return obj.post.title

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        exclude = ['user_permissions','groups','is_superuser','is_staff','last_login','is_active','date_joined']
        extra_kwargs= {
             'password':{'write_only': True}
        }

    def create(self, validated_data):
        password = make_password(password=validated_data['password'])
        validated_data['password'] = password
        user = User.objects.create_user(**validated_data)
        return user

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','password','username', 'first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True}, 
            
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], email=validated_data['email'], password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
        return user


# Change password serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance