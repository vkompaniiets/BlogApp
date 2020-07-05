from django.conf.urls import url

from .views import about, tag, contact, post, search

urlpatterns = [
    # landing
    url(r'^$', post.PostListView.as_view(), name='post_list'),
    url(r'^search/$', search.SearchListView.as_view(), name='search_results'),
    url(r'^contact/$', contact.ContactView.as_view(), name='contact'),
    url(r'^about/$', about.AboutView.as_view(), name='about'),

    # post
    url(r'^post/(?P<pk>[0-9]+)/$', post.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', post.PostCreateView.as_view(), name='post_new'),
    url(r'^post/drafts/$', post.PostDraftListView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', post.PostUpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', post.PostPublishView.as_view(), name='post_publish'),
    url(r'^post_remove/(?P<pk>[0-9]+)/$', post.PostDeleteView.as_view(), name='post_remove'),

    # tag
    url(r'^tags/$', tag.TagView.as_view(), name='tags'),
    url(r'^tags/(?P<pk>[0-9]+)/$', tag.FilterByTagView.as_view(), name='filter_by_tag'),
    url(r'^tags/(?P<pk>[0-9]+)/edit/$', tag.UpdateTagView.as_view(), name='edit_tag'),
    url(r'^tags/(?P<pk>[0-9]+)/remove/$', tag.TagDelete.as_view(), name='remove_tag'),
]
