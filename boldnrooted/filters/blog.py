import django_filters
from ..models import BlogPost


class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    is_published = django_filters.BooleanFilter()
    scripture_references__book = django_filters.CharFilter(
        field_name="scripture_references__book",
        lookup_expr="icontains"
    )

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "is_published",
            "scripture_references__book",
        ]