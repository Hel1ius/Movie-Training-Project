from django.views.generic import CreateView, RedirectView

from .forms import ContactForm
from .models import Contact


class ContactView(RedirectView):
    model = Contact
    form_class = ContactForm
    pattern_name = 'home'