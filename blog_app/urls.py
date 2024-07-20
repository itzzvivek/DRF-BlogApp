from django.urls import path
from . import views

urlpatterns = [
    path("category_list/", views.CategoryListCreateView.as_view(), name="category_list"),
    path("category_detail/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),

    path("blog_list/", views.BlogListCreateView.as_view(), name="blog_list"),
    path("blog_detail/<int:pk>/", views.BlogDetailView.as_view(), name="blog_detail"),

    path("blog_comment_list/<int:blog_id>", views.BlogCommentListCreateView.as_view(), name="blog_comment_list"),
    path("blog_comment_details/blog/<int:blog_id>/comment/<int:comment_id>", views.BlogCommentDetailView.as_view(),
         name="blog_comment_details"),
]

