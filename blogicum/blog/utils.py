from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from .models import Post


class CreateUpdateView(
    SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView
):
    """
    Как у BaseUpdateView, так и у BaseCreateView общие практически родители,
    то просто наследуем их все. Дальше единственным отличием в их реализации -
    это значение атрибута self.object. Чтобы сделать CBV для создания и
    удаления,  мы должны переопределить метод get_object в случае если Update
    операция (тк мы работаем с существующим объектом модели), либо None
    если Create.
    """

    def get_object(self, queryset=None):
        """
        Если у нас определится ID объекта модели, то это Update метод
        и мы вернём ему результат, а иначе Create и возвращаем None.
        :param queryset: Запрос к ORM.
        :return: Запись по ID или None.
        """
        pk = self.kwargs.get("pk")
        if pk is not None:
            return get_object_or_404(Post, pk=pk)
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CreateUpdateView, self).post(request, *args, **kwargs)
