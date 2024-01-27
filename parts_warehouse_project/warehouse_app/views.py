from rest_framework import viewsets
from .serializers import PartSerializer, CategorySerializer
from .models import Part, Category
from .exceptions import CustomException


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        parts_assigned = Part.objects.filter(category=category.name)

        if parts_assigned:
            raise CustomException('Cannot delete category that is assigned to parts', 400)

        return super().destroy(request, args, kwargs)



