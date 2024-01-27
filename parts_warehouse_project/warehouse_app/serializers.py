from rest_framework import serializers
from .models import Part, Category


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        location = attrs.get('location')

        if (not quantity and location) or (quantity and not location):
            raise serializers.ValidationError({'message': 'Quantity and location must be given at the same time if one of them occurs'})

        if sum(location.values()) != quantity:
            raise serializers.ValidationError({'message': 'Sum of parts in locations does not equal quantity'})

        return super().validate(attrs)

    def validate_location(self, value):
        allowed_keys = {'room', 'bookcase', 'shelf', 'cuvee', 'column', 'row'}

        invalid_keys = set(value.keys()) - allowed_keys
        if invalid_keys:
            raise serializers.ValidationError('Missing correct location')

        invalid_values = [key for key, value in value.items() if not isinstance(value, int)]
        if invalid_values:
            raise serializers.ValidationError('Values must be integers')

        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'