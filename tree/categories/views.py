from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tree.categories.exceptions import InvalidBodyException, CategoryServiceException
from tree.categories.models import Category
from tree.categories.serializers import CategoryRelationsSerializer
from tree.categories.services import CategoryService, CategoryData
from tree.categories.utils import parse_category_tree_request_body


class CategoriesView(APIView):
    def post(self, request):
        """
        Accepts a categories tree, validates it and saves to DB.
        """
        try:
            category_tree = parse_category_tree_request_body(request.body)
        except InvalidBodyException:
            return Response(data={'error': 'Invalid body'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = CategoryService(data=CategoryData())
            root_id = service.save_category_tree(category_tree)
        except CategoryServiceException as e:
            return Response(data=e.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'rootId': root_id}, status=status.HTTP_201_CREATED)


class CategoryView(RetrieveAPIView):
    """
    Retrieves info about a category and its relations with other categories.
    """
    serializer_class = CategoryRelationsSerializer
    queryset = Category.objects.all().prefetch_related('children')
