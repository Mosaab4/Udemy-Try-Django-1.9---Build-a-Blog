from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from comments.models import Comment

from posts.api.permissions import IsOwnerOrReadOnly

from posts.api.pagination import (
    PostLimitOffsetPagination,
    PostPageNumberPagination
)

from .serializers import CommentSerializer, CommentDetailSerializer


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'


class CommentListAPTView(ListAPIView):
    serializer_class =CommentSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['content','user__first_name']
    pagination_class = PostPageNumberPagination


    def get_queryset(self, *args,**kwargs):
        queryset_list = Comment.objects.all()
        
        query = self.request.GET.get("q")

        if query :
            queryset_list = queryset_list.filter(
                Q(content__iscontains = query)|
                Q(user__first_name__iscontains = query)|
                Q(user__last_name__iscontains = query)
            ).distinct()

        return queryset_list






















