from rest_framework.throttling import User

class BlogListCreateViewThrottle(UserRateThrottle):
    scope = "blog-list"

