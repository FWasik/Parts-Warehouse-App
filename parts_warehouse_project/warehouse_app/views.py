from rest_framework import viewsets, generics
from .serializers import PartSerializer, CategorySerializer
from .models import Part, Category
from .exceptions import CustomException
from django_filters.rest_framework import DjangoFilterBackend


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PartSearchView(generics.ListAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "serial_number",
        "name",
        "description",
        "category",
        "quantity",
        "price",
    ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        parts_assigned = Part.objects.filter(category=category.name)

        if parts_assigned:
            raise CustomException('Cannot delete category that is assigned to parts', 400)

        return super().destroy(request, args, kwargs)



