from django.urls import path
from .views import (
    HomePageView,
    EstadoListView,
    MunicipioListView,
    DistritoListView,
    EmpresaListView
)

app_name = 'localidades'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('estados/', EstadoListView.as_view(), name='estado_list'),
    path('municipios/', MunicipioListView.as_view(), name='municipio_list'),
    path('distritos/', DistritoListView.as_view(), name='distrito_list'),
    path('empresas/', EmpresaListView.as_view(), name='empresa_list'),
]