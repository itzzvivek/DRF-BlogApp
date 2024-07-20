from django.db.migrations import serializer
from django.shortcuts import get_object_or_404
from .models import Blog, BlogComment, Category
from .serializers import BlogSerializer, BlogCommentSerializer, CategorySerializer
from rest_framework.response import responses, Response
from rest_framework import status, viewsets
from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import BlogListCreatePagination


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = CategorySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": 'No Category found'}, status=status.HTTP_404_NOT_FOUND)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_data = BlogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__category_name', 'is_published']
    search_fields = ['^blog_title', 'blog_description', 'category__category_name']

    pagination_class = BlogListCreatePagination

    def create(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.filter(is_public=True)
    serializer_class = BlogSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogCommentListCreateView(generics.ListCreateAPIView):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id')
        return BlogComment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        if BlogComment.objects.filter(blog=blog, author=self.request.user).exists():
            raise serializers.ValidationError({'Message': 'You have already added comment on this blog'})
        serializer.save(author=self.request.user, blog=blog)


class BlogCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(BlogComment, id=comment_id)

        blog_id= self.kwargs.get('blog_id')
        if comment.blog.id != blog_id:
            raise serializers.ValidationError({'Message': 'This comment is not related to the requested blog'}, status=status.HTTP_401_UNAUTHORIZED)
        return comment

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise serializers.ValidationError({"Message": "You are not authorized to perform this action"}, status=status.HTTP_404_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.author != request.user:
            raise serializers.ValidationError({"Message": "You are not authorized to perform this action"}, stauts=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)