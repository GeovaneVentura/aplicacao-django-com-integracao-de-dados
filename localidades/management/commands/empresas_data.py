import csv
import itertools
from django.core.management.base import BaseCommand
from django.db import transaction
from localidades.models import Empresa

'''
definir o tamanho do lote. Em máquinas mais potentes,
valor pode ser aumentado para melhor desempenho
'''
BATCH_SIZE = 25000

class Command(BaseCommand):
    help = 'Importa dados de empresas de um arquivo CSV da Receita Federal.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV das empresas.')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Iniciando importação do arquivo: {file_path}'))

        data_generator = self._csv_reader_generator(file_path)

        # mapeamento dos índices do csv
        COLUMN_MAPPING = {
            'cnpj_basico': 0, 'razao_social': 1, 'natureza_juridica': 2,
            'qualificacao_responsavel': 3, 'capital_social': 4,
            'porte_empresa': 5, 'ente_federativo_responsavel': 6,
        }

        batch_num = 1
        while True:
            # pega um lote do gerador usando itertools.islice
            self.stdout.write(self.style.NOTICE(f'\nProcessando lote {batch_num}...'))
            batch = list(itertools.islice(data_generator, BATCH_SIZE))

            # se o lote estiver vazio, sai do loop
            if not batch:
                break

            cnpjs_no_lote = [row[COLUMN_MAPPING['cnpj_basico']] for row in batch]

            # para este lote, verifica quais CNPJs já existem no banco
            cnpjs_existentes = set(Empresa.objects.filter(
                cnpj_basico__in=cnpjs_no_lote
            ).values_list('cnpj_basico', flat=True))

            objetos_para_criar = []
            objetos_para_atualizar = []

            for row in batch:
                cnpj = row[COLUMN_MAPPING['cnpj_basico']]
                capital_social_str = row[COLUMN_MAPPING['capital_social']].replace(',', '.')

                empresa = Empresa(
                    cnpj_basico=cnpj,
                    razao_social=row[COLUMN_MAPPING['razao_social']],
                    natureza_juridica=row[COLUMN_MAPPING['natureza_juridica']],
                    qualificacao_responsavel=int(row[COLUMN_MAPPING['qualificacao_responsavel']]),
                    capital_social=float(capital_social_str),
                    porte_empresa=row[COLUMN_MAPPING['porte_empresa']] or None,
                    ente_federativo_responsavel=row[COLUMN_MAPPING['ente_federativo_responsavel']] or None,
                )

                if cnpj in cnpjs_existentes:
                    objetos_para_atualizar.append(empresa)
                else:
                    objetos_para_criar.append(empresa)

            # executa as operações de banco de dados para o lote atual
            try:
                with transaction.atomic():
                    if objetos_para_criar:
                        Empresa.objects.bulk_create(objetos_para_criar, batch_size=1000)
                        self.stdout.write(
                            self.style.SUCCESS(f'  - Criados: {len(objetos_para_criar)} novos registros.'))

                    if objetos_para_atualizar:
                        campos_para_atualizar = [
                            'razao_social', 'natureza_juridica', 'qualificacao_responsavel',
                            'capital_social', 'porte_empresa', 'ente_federativo_responsavel'
                        ]
                        Empresa.objects.bulk_update(objetos_para_atualizar, campos_para_atualizar, batch_size=1000)
                        self.stdout.write(
                            self.style.SUCCESS(f'  - Atualizados: {len(objetos_para_atualizar)} registros existentes.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ocorreu um erro no lote {batch_num}: {e}'))
                # Decide se quer parar ou continuar
                break

            batch_num += 1

        self.stdout.write(self.style.SUCCESS('\nImportação concluída com sucesso!'))

    def _csv_reader_generator(self, file_path):
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    yield row
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro fatal ao ler o arquivo: {e}"))
            exit()