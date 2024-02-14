from .serializers import PartSerializer, CategorySerializer
from .models import Part, Category
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets, generics
from rest_framework import status
import itertools
import json


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    lookup_field = "serial_number"


class PartSearchView(generics.ListAPIView):
    serializer_class = PartSerializer

    def get_queryset(self):
        queryset = Part.objects.all()
        params = self.request.query_params

        filters = {
            "serial_number": params.get("serial_number"),
            "name": params.get("name"),
            "description": params.get("description"),
            "category": params.get("category"),
            "quantity": params.get("quantity"),
            "price": params.get("price"),
            "location": params.get("location"),
        }

        for field, value in filters.items():
            if value:
                if field == "location":
                    value = json.loads(value)

                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "name"

    def update(self, request, *args, **kwargs):
        name = request.data.get("name")

        category = self.get_object()
        category_name = category.name
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if name:
            children = Category.objects(parent_name=category_name).filter()
            parts = Part.objects(category=category_name).filter()

            for child, part in itertools.zip_longest(children, parts, fillvalue=None):
                if child:
                    child.parent_name = name
                    child.save()
                if part:
                    part.category = name
                    part.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        children_to_delete = []

        if not category.can_be_deleted(children_to_delete):
            return Response(
                {
                    "messages": "Cannot delete category - it or one of its children has a assigned parts"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        for child in children_to_delete:
            child.delete()

        return super().destroy(request, args, kwargs)
