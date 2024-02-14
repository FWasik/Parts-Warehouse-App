from rest_framework.serializers import ValidationError
from .models import Part, Category
from rest_framework_mongoengine import serializers


class PartSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Part
        fields = "__all__"

    def validate(self, attrs):
        quantity = attrs.get("quantity")
        location = attrs.get("location")

        if (not quantity and location) or (quantity and not location):
            raise ValidationError(
                {
                    "messages": "Quantity and location must be given at the same time if one of them occurs"
                }
            )

        if quantity and location and sum(location.values()) != quantity:
            raise ValidationError(
                {"messages": "Sum of parts in locations does not equal quantity"}
            )

        return super().validate(attrs)

    def validate_category(self, value):
        category = Category.objects(name=value).first()

        if not category:
            raise ValidationError("There is no given category")

        if not category.parent_name:
            raise ValidationError("Cannot assign to base category")

        return value

    def validate_location(self, value):
        allowed_keys = {"room", "bookcase", "shelf", "cuvee", "column", "row"}
        errors = []

        if set(value.keys()) - allowed_keys:
            errors.append(
                "Missing correct location (room, bookcase, shelf, cuvee, column, row)"
            )

        for key, val in value.items():
            if not isinstance(val, int) or val < 0:
                errors.append("Values must be greater than or equal to 0")

                break

        if errors:
            raise ValidationError(errors)

        return value


class CategorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_parent_name(self, value):
        if value:
            parent_category = Category.objects(name=value).first()

            if not parent_category:
                raise ValidationError("There is no given parent category")

        return value

    def update(self, instance, validated_data):
        if "parent_name" in validated_data:
            parent_name = validated_data.get("parent_name")

            if parent_name:
                parent_category = Category.objects(name=parent_name).first()

                if parent_category == instance:
                    raise ValidationError({"messages": "Category cannot be its own parent"})

                if not instance.parent_name and instance.is_child(parent_category):
                    raise ValidationError(
                        {
                            "messages": "Base category cannot be assigned to one of its children"
                        }
                    )

            elif instance.parent_name and Part.objects(category=instance.name).count() > 0:
                raise ValidationError(
                    {
                        "messages": "Cannot change category to a base category if there are parts assigned to that category"
                    }
                )

        return super().update(instance, validated_data)
