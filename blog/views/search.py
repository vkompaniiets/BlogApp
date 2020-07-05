from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import ListView

from blog.models import Post, Tag


class SearchListView(ListView):
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(published_at__lte=timezone.now()), Q(title__icontains=query) | Q(text__icontains=query)
        ).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(posts__published_at__isnull=False).values('pk', 'name').annotate(
            tags_count=Count('posts')).order_by('-tags_count')[:5]
        return context
