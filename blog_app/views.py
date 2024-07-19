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
        serializer = CategorySerializer(queryset, many=True, context={'request': request})
        if queryset.extra():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": 'No Category found'}, status=status.HTTP_404_NOT_FOUND)
