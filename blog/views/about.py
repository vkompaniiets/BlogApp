from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'blog/about.html'
