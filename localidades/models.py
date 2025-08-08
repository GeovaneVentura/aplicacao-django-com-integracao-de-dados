from django.db import models

class Estado(models.Model):
    # ID do ibge será o utilizado
    id = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    # um municipio pertence a um estado.
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='municipios')

    def __str__(self):
        return f'{self.nome} ({self.estado.sigla})'

class Distrito(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    # um distrito pertence a um municipio.
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='distritos')

    def __str__(self):
        return f'{self.nome} / {self.municipio}'


class Empresa(models.Model):
    cnpj_basico = models.CharField(max_length=8, primary_key=True)
    razao_social = models.CharField(max_length=255, db_index=True)
    natureza_juridica = models.CharField(max_length=4)
    qualificacao_responsavel = models.IntegerField()
    capital_social = models.DecimalField(max_digits=16, decimal_places=2)
    porte_empresa = models.CharField(max_length=2, blank=True, null=True)
    ente_federativo_responsavel = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f'{self.cnpj_basico} - {self.razao_social}'