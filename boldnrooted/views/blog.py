from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import BlogPost
from ..serializers import BlogPostSerializer
from ..filters import BlogFilter
from ..common import *


class BlogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = BlogFilter

    search_fields = [
        "title",
        "content",
        "scripture_references__book",
        "tags__name",
    ]

    ordering_fields = [
        "created_at",
        "published_at",
        "title",
    ]

    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return BlogPost.objects.filter(
            is_active=True,
            is_published=True
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return ApiResponse.success(
            data=response.data,
            meta={
                "count": self.paginator.page.paginator.count
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        blog = serializer.save()

        return ApiResponse.success(
            data=BlogPostSerializer(blog).data,
            message="Blog post created successfully",
            status=status.HTTP_201_CREATED
        )


class BlogRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return BlogPost.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()
        return ApiResponse.success(BlogPostSerializer(blog).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        blog = serializer.save()


        return ApiResponse.success(
            BlogPostSerializer(blog).data,
            message="Blog post updated successfully"
        )
    
    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()

        blog.delete()

        return ApiResponse.success(
            message="Blog post deleted successfully",
            status=status.HTTP_200_OK
        )