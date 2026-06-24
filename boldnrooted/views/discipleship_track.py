from rest_framework import generics
from ..models import DiscipleshipTrack
from ..serializers import *
from ..common import *
from rest_framework import status




class DiscipleshipTrackListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = DiscipleshipTrack.objects.filter(
        is_active=True
    )

    serializer_class = DiscipleshipTrackSerializer
    pagination_class = StandardPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return ApiResponse.success(
            data=response.data,
            meta={
                "count": self.paginator.page.paginator.count
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        track = serializer.save()

        return ApiResponse.success(
            data=DiscipleshipTrackSerializer(track).data,
            message="Discipleship track created successfully",
            status=status.HTTP_201_CREATED
        )
    
class DiscipleshipTrackRetrieveUpdateAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = DiscipleshipTrack.objects.filter(
        is_active=True
    )

    serializer_class = DiscipleshipTrackSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        track = self.get_object()

        return ApiResponse.success(
            data=DiscipleshipTrackSerializer(track).data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)

        track = serializer.save()

        return ApiResponse.success(
            data=DiscipleshipTrackSerializer(track).data,
            message="Discipleship track updated successfully"
        )

    def destroy(self, request, *args, **kwargs):
        track = self.get_object()

        track.is_active = False
        track.save(update_fields=["is_active"])

        return ApiResponse.success(
            message="Discipleship track deleted successfully"
        )
    
class DiscipleshipModuleListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = DiscipleshipModule.objects.filter(
        is_active=True
    )

    serializer_class = DiscipleshipModuleSerializer

class DiscipleshipModuleRetrieveUpdateAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = DiscipleshipModule.objects.filter(
        is_active=True
    )

    serializer_class = DiscipleshipModuleSerializer

    lookup_field = "id"