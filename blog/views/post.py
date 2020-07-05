from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, RedirectView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post, Tag
from blog.permission import AdminPermissionMixin


class PostListView(ListView):
    queryset = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(posts__published_at__isnull=False).values('pk', 'name').annotate(
            tags_count=Count('posts')).order_by('-tags_count')[:5]
        return context


class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    model = Tag

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post


class TagMixin(object):
    def save_tags(self, post_getlist_tags):
        """
        return objects list of tags.
        allow to create if the tag is doesn't exist.
        this function bassed on slug field.

        :param `post_getlist_tags` is request.POST.getlist('fake_tags', [])
        """
        cleaned_tags = []
        for name in post_getlist_tags:
            if Tag.objects.filter(name=name).exists():
                tag = Tag.objects.filter(name=name).first()
                cleaned_tags.append(tag)
            else:
                if bool(name.strip()):
                    tag = Tag.objects.create(name=name)
                    tag.save()
                    cleaned_tags.append(tag)
        return cleaned_tags


class PostCreateView(AdminPermissionMixin, CreateView, TagMixin):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_draft_list')
    template_name_suffix = '_edit'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        saved_tags = self.save_tags(self.request.POST.getlist('tags', []))
        post.tags.add(*saved_tags)
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(AdminPermissionMixin, UpdateView, TagMixin):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name_suffix = '_edit'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        saved_tags = self.save_tags(self.request.POST.getlist('tags', []))
        post.tags.add(*saved_tags)
        return super(PostUpdateView, self).form_valid(form)


class PostDraftListView(AdminPermissionMixin, TemplateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_draft_list')
    template_name = 'blog/post_draft_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostDraftListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(published_at__isnull=True).order_by('created_at')
        return context


class PostPublishView(AdminPermissionMixin, RedirectView):
    url = reverse_lazy('post_list')

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.publish()
        return super(PostPublishView, self).get(request, *args, **kwargs)


class PostDeleteView(AdminPermissionMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
