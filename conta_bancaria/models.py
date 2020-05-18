from django.db import models


class contaBancaria(models.Model):
    banco = models.CharField(max_length=100)

    numero_agencia = models.CharField(max_length=100)

    digito_verificador_agencia = models.CharField(
        max_length=100, null=True, blank=True)

    numero_conta_bancaria = models.CharField(max_length=100)

    digito_verificador_conta_bancaria = models.CharField(max_length=100)

    def get_absolute_url(self):
        return '/conta-bancaria/' + str(self.pk)
