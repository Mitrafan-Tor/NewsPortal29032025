from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter
from .models import Post, Category
from django.forms import DateTimeInput

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class SearchPost(FilterSet):
   created_at = DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
   )

   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'title': ['icontains'],
           # количество товаров должно быть больше или равно
           'author__user__username': ['icontains'],
       }

   categories = ModelMultipleChoiceFilter(
       field_name='categories',  # имя поля в модели Post
       queryset=Category.objects.all(),
       label='Категории',
   )

   # class Category_fl:
   #      model = Category
   #      fields = {
   #         # поиск по названию
   #         'name': ['icontains'],
   #      }