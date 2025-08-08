import django_filters
from .models import Estado, Municipio, Distrito, Empresa


class EstadoFilter(django_filters.FilterSet):
    # Permite filtrar pelo nome
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do Estado')

    class Meta:
        model = Estado
        fields = ['sigla']  # Permite filtrar por sigla

class MunicipioFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do Município')
    class Meta:
        model = Municipio
        fields = ['estado'] # Permite filtrar por estado

class DistritoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do Distrito')
    class Meta:
        model = Distrito
        fields = ['municipio'] # Permite filtrar por municipio

class EmpresaFilter(django_filters.FilterSet):
    razao_social = django_filters.CharFilter(lookup_expr='icontains', label='Razão Social')
    cnpj_basico = django_filters.CharFilter(lookup_expr='exact', label='CNPJ (8 dígitos)')
    class Meta:
        model = Empresa
        fields = ['razao_social', 'cnpj_basico'] # Permite filtrar por razao social e cnpj
