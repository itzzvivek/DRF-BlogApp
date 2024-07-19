from rest_framework.pagination import CursorPagination


class BlogListCreatePagination(CursorPagination):
    page_size = 2
    ordering = "post_date"
