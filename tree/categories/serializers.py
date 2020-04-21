from rest_framework import serializers

from tree.categories.models import Category
from tree.categories.services import CategoryData


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryRelationsSerializer(serializers.ModelSerializer):
    children = CategorySerializer(many=True)
    siblings = serializers.SerializerMethodField()
    parents = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'children', 'siblings', 'parents']

    def get_siblings(self, obj):
        siblings = CategoryData().get_siblings(obj)
        return CategorySerializer(siblings, many=True).data

    def get_parents(self, obj):
        parents = CategoryData().get_parents(obj)
        return CategorySerializer(parents, many=True).data
