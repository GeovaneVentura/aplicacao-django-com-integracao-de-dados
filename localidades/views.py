from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Estado, Municipio, Distrito, Empresa
from .filters import EstadoFilter, MunicipioFilter, DistritoFilter, EmpresaFilter

class EstadoListView(ListView):
    model = Estado
    template_name = 'localidades/estado_list.html'
    context_object_name = 'estados'
    paginate_by = 10  # Quantidade de itens por página

    def get_queryset(self):
        # Pega o queryset original
        queryset = super().get_queryset()
        self.filter = EstadoFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class HomePageView(TemplateView):
    template_name = "home.html"

class MunicipioListView(ListView):
    model = Municipio
    template_name = 'localidades/municipio_list.html'
    context_object_name = 'municipios'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('estado')
        self.filter = MunicipioFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class DistritoListView(ListView):
    model = Distrito
    template_name = 'localidades/distrito_list.html'
    context_object_name = 'distritos'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('municipio__estado')
        self.filter = DistritoFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class EmpresaListView(ListView):
    model = Empresa
    template_name = 'localidades/empresa_list.html'
    context_object_name = 'empresas'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('cnpj_basico')
        self.filter = EmpresaFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context