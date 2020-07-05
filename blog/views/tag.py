from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, FormView, CreateView

from blog.forms import TagForm
from blog.models import Tag
from blog.permission import AdminPermissionMixin


class BaseView(AdminPermissionMixin, FormView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('tags')
    template_name = 'blog/tags.html'

    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.form_error = False

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['form'] = TagForm
        context['form_error'] = self.form_error
        return context


class TagView(BaseView, CreateView):
    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)
        if not form.is_valid():
            self.form_error = True
            return super(TagView, self).get(request, *args, **kwargs)
        return super(TagView, self).post(request, *args, **kwargs)


class UpdateTagView(UpdateView, BaseView):
    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)
        if not form.is_valid():
            self.form_error = True
            return super(UpdateTagView, self).get(request, *args, **kwargs)
        return super(UpdateTagView, self).post(request, *args, **kwargs)


class FilterByTagView(DetailView):
    template_name = 'blog/tag_specific.html'
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(FilterByTagView, self).get_context_data(**kwargs)
        context['posts'] = kwargs['object'].posts.filter(published_at__isnull=False).order_by('published_at')
        context['tags'] = kwargs['object']
        return context


class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('tags')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
