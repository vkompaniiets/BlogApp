from django.views.generic import TemplateView


class ContactView(TemplateView):
    template_name = 'blog/contact.html'
