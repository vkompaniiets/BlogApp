from django import forms

from .models import Post, Tag
from .fields import *


def new_tag(value):
    tag, created = Tag.objects.get_or_create(name=value)
    return tag


class PostForm(forms.ModelForm):
    tags = MultipleTypeaheadField(
        queryset=Tag.objects.all(),
        builder=new_tag,
        required=True
    )

    class Meta:
        model = Post
        fields = ('title', 'tags', 'text',)
        exclude = ['author']

    def clean(self):
        return super(PostForm, self).clean()

    def full_clean(self):
        return super(PostForm, self).full_clean()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if instance:
            initial['tags'] = instance.tags.all()
        else:
            initial['tags'] = Tag.objects.all()
        kwargs['initial'] = initial


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
