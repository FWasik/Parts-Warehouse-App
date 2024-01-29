from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Part, Category


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"

    def validate(self, attrs):
        quantity = attrs.get("quantity")
        location = attrs.get("location")

        if (not quantity and location) or (quantity and not location):
            raise serializers.ValidationError(
                "Quantity and location must be given at the same time if one of them occurs"
            )

        if sum(location.values()) != quantity:
            raise serializers.ValidationError(
                "Sum of parts in locations does not equal quantity"
            )

        return super().validate(attrs)

    def validate_location(self, value):
        allowed_keys = {"room", "bookcase", "shelf", "cuvee", "column", "row"}
        errors = []

        invalid_keys = set(value.keys()) - allowed_keys
        if invalid_keys:
            errors.append(
                "Missing correct location (room, bookcase, shelf, cuvee, column, row)"
            )

        invalid_values = [
            key
            for key, value in value.items()
            if not isinstance(value, int) or value < 0
        ]
        if invalid_values:
            errors.append("Values must be positive integers")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate_serial_number(self, value):
        if Part.objects.filter(serial_number=value):
            raise serializers.ValidationError(
                "There is already a part with this serial number"
            )

        return value

    def validate_category(self, value):
        try:
            category = Category.objects.get(name=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("There is no given category")

        if not category.parent_name:
            raise serializers.ValidationError("Cannot assign to base category")

        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be lower than 0")

        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_parent_name(self, value):
        if not Category.objects.filter(name=value):
            raise serializers.ValidationError("There is no given category")

        return value
