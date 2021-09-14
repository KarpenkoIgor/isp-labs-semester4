from django.shortcuts import render
from django.views.generic import DetailView
from .models import (
    Filter,
    Breaks,
    Ignition,
    Suspension,
    ExhaustSystem,
    FuelSystem
    )

def test_view(request):
    return render(request, 'base.html', {})

class CarpartDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'filter': Filter,
        'breaks': Breaks,
        'ignition': Ignition,
        'suspension': Suspension,
        'exhaust-system': ExhaustSystem,
        'fuel-system': FuelSystem,        
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'carpart'
    template_name = 'carpart_detail.html'
    slug_url_kwarg = 'slug'