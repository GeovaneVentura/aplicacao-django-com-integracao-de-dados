import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from localidades.models import Estado, Municipio, Distrito

# url da api do ibge
URL_ESTADOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"


class Command(BaseCommand):
    help = 'Importa dados de Estados, Municípios e Distritos da API do IBGE.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando importação de dados do IBGE...'))

        # importar estados
        self.stdout.write('Importação de Estados...')
        response_estados = requests.get(URL_ESTADOS)
        estados_data = response_estados.json()

        estados_para_criar = []
        for estado_info in estados_data:
            estados_para_criar.append(
                Estado(id=estado_info['id'], sigla=estado_info['sigla'], nome=estado_info['nome'])
            )

        # inserção unica
        Estado.objects.bulk_create(estados_para_criar, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'{len(estados_para_criar)} Estados importados.'))

        # importar municípios
        self.stdout.write('Importação de Municípios...')
        municipios_para_criar = []
        estados = Estado.objects.all()
        for estado in estados:
            url_municipios = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado.id}/municipios"
            response_municipios = requests.get(url_municipios)
            municipios_data = response_municipios.json()

            for municipio_info in municipios_data:
                municipios_para_criar.append(
                    Municipio(id=municipio_info['id'], nome=municipio_info['nome'], estado=estado)
                )

        Municipio.objects.bulk_create(municipios_para_criar, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'{len(municipios_para_criar)} Municípios importados.'))

        # importar distritos
        self.stdout.write('Importação de Distritos...')
        distritos_para_criar = []
        municipios = Municipio.objects.all()
        url_distritos = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"
        response_distritos = requests.get(url_distritos)
        distritos_data = response_distritos.json()

        municipio_map = {municipio.id: municipio for municipio in municipios}

        for distrito_info in distritos_data:
            municipio_id = distrito_info['municipio']['id']
            municipio_obj = municipio_map.get(municipio_id)
            if municipio_obj:
                distritos_para_criar.append(
                    Distrito(id=distrito_info['id'], nome=distrito_info['nome'], municipio=municipio_obj)
                )

        Distrito.objects.bulk_create(distritos_para_criar, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'{len(distritos_para_criar)} Distritos importados.'))

        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))