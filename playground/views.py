from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _


class TestView(TemplateView):
    template_name = 'playground/index.html'
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['mamad'] = _('mamad')
        return context