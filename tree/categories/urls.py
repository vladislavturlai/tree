from django.urls import path

from tree.categories.views import CategoriesView, CategoryView

app_name = 'categories'
urlpatterns = [
    path('', CategoriesView.as_view(), name='categories'),
    path('<int:pk>/', CategoryView.as_view(), name='category'),
]
