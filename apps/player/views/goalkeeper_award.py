# from rest_framework import generics, filters
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
# from ..serializers import *
# from ..filters import *
# from ...common import *


# class GoalkeeperAwardEventListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = GoalkeeperAwardEventSerializer
#     pagination_class = StandardPagination
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_class = GoalkeeperAwardEventFilter
#     ordering_fields = ["event_date"]

#     def get_permissions(self):
#         if self.request.method == "POST":
#             return [IsAuthenticated()]
#         return [AllowAny()]

#     def get_queryset(self):
#         return GoalkeeperAwardEvent.objects.all()


# class GoalkeeperAwardNominationListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = GoalkeeperAwardNominationSerializer
#     pagination_class = StandardPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = GoalkeeperAwardNominationFilter
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return GoalkeeperAwardNomination.objects.select_related(
#             "player", "category", "category__event"
#         )


# class GoalkeeperAwardWinnerCreateAPIView(generics.CreateAPIView):
#     serializer_class = GoalkeeperAwardWinnerSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(approved_by=self.request.user)
