from django.http import Http404
from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly
from .pagination import PostPagination

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status , generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
 

# ----------------- USERS ----------------------
class UserList(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    '''
    List all users, or create a new user
    '''
    def get(self, request):
        users = User.objects.all() 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
      
class UserDetail(APIView):
    '''
    Retrieve, update and delete a user instance
    '''
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)  
        except User.DoesNotExist:
            return Response({'Error':'user not found'}, status=status. HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.is_admin:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():  
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        return Response({'error':'Only admins can perform this task!'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        if request.user.is_admin:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'DETAIL': 'DELETED'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Only admins can perform this task!'}, status=status.HTTP_403_FORBIDDEN)


# ------------------ CATEGORIES -------------------
class CategoryList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [ SearchFilter]
    search_fields = ['name']
    
class CategoryDetail(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    '''
    Retrieve, update and delete a category instance
    '''
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)  
        except Category.DoesNotExist:
            return Response({'error':'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)  


    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({'DETAIL': 'DELETED'}, status=status.HTTP_204_NO_CONTENT)
    

# ---------------- POSTS ----------------------
class PostList(generics.ListAPIView):
    '''
    List all posts or create a new post instance
    '''
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all() 
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category_id']
    search_fields = ['title', 'category__name', 'intro']

class PostDetail(APIView):
    '''
    Retrieve, update and delete a post instance
    '''
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)  
        except Post.DoesNotExist:
            return Response({'Error':'Post not found'}, status=status. HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    '''
    Only owners of post should be able update and delete it (But admin can delete)
    '''
    def put(self, request, pk): 
        aut = Post.objects.get(pk=pk).author
        if request.user == aut:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():  
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        return Response({'error':'you do not have permission to perform this action'})
    
    def delete(self, request, pk):
        aut = Post.objects.get(pk=pk).author
        if request.user == aut or request.user.is_admin:
            post = Post.objects.get(pk=pk)
            if post.delete():
                return Response( status=status.HTTP_204_NO_CONTENT)
            return Response({'DETAIL': 'DELETED'}, status=status.HTTP_204_NO_CONTENT)  
        return Response({'error':'you do not have the permission to perform this action'})

        
#------------------ COMMENTS -------------------- 
class CommentList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter ]
    filterset_fields = ['post_id' ]
    search_fields = ['post__title', 'comment']

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Only owners of comment and admins should be able to update or delete it
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 




























