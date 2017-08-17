from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView , 
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
) 
 
from posts.models import Post
from .serializers import (
    PostListSerializer , 
    PostDetailSerializer,
    PostCreateUpdateSerializer,
)



class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer



class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abs'

class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abs'

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abs'


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()    
    serializer_class = PostListSerializer




