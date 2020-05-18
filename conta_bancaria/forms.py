from django import forms
import requests
import json
from bank_account_validator.core import Bank, BrazilianBank
from bank_account_validator.exceptions import (
    BankNotImplemented, InvalidBranch, InvalidAccount,
    InvalidBranchAndAccountCombination, InvalidBranchlength,
    InvalidAccountlength, MissingBranchDigit, MissingAccountDigit,
    UnexpectedBranchDigit, UnexpectedAccountDigit
)
from .models import contaBancaria


class cadastroBanco(forms.ModelForm):
    banco = forms.CharField(required=True)
    numero_agencia = forms.CharField(required=True)

    digito_verificador_agencia = forms.CharField(required=False)

    numero_conta_bancaria = forms.CharField(required=True)

    digito_verificador_conta_bancaria = forms.CharField(required=False)

    error_messages = {
        'invalid_branch': (
            "Agência '%(agencia_e_digito)s' é inválida."
        ),
        'invalid_account': (
            "Conta bancária '%(conta_e_digito)s' é inválida."
        ),
        'invalid_branch_and_account_combination': (
            "Combinação (agência='%(agencia)s', conta='%(conta_e_digito)s') não é válida."
        ),
        'invalid_branch_length': (
            "%(banco)s: a agência deve ter %(agencia_length)s caracteres."
        ),
        'invalid_account_length': (
            "%(banco)s: a conta deve ter %(conta_length)s caracteres."
        ),
        'missing_branch_digit': (
            "%(banco)s: agências devem ter um dígito, de tamanho %(digito_agencia_length)s."
        ),
        'unexpected_branch_digit': (
            "%(banco)s: agências devem ter %(digito_agencia_length)s dígitos."
        ),
        'missing_account_digit': (
            "%(banco)s: contas devem ter um dígito, de tamanho %(digito_conta_length)s."
        ),
        'unexpected_account_digit': (
            "%(banco)s: contas devem ter %(digito_conta_length)s dígitos."
        )
    }

    class Meta:
        model = contaBancaria
        fields = ['banco', 'numero_agencia', 'digito_verificador_agencia', 'numero_conta_bancaria',
                  'digito_verificador_conta_bancaria']  # list of fields you want from model

    def clean(self):
        cleaned_data = super().clean()

        banco = str(cleaned_data.get("banco"))
        numero_agencia = str(cleaned_data.get("numero_agencia"))
        digito_verificador_agencia = str(cleaned_data.get(
            "digito_verificador_agencia"))
        numero_conta_bancaria = str(cleaned_data.get("numero_conta_bancaria"))
        digito_verificador_conta_bancaria = str(cleaned_data.get(
            "digito_verificador_conta_bancaria"))

        BANKS = requests.get(
            'https://gist.githubusercontent.com/antoniopresto/d73888dab087ae35a7cf41a61d8a3cbc/raw/43c94b305367afa82734f6fb4480f55e77e08a6e/banco_codigo.json').json()

        label_banco = None

        for bank in BANKS:
            if bank['value'] == banco:
                label_banco = bank['label']

        try:
            bank_class = BrazilianBank.get(banco)
            bank_class(branch=numero_agencia, branch_digit=digito_verificador_agencia,
                       account=numero_conta_bancaria, account_digit=digito_verificador_conta_bancaria).execute()

        except InvalidBranch:
            raise forms.ValidationError(
                self.error_messages['invalid_branch'],
                code='invalid_branch',
                params={'agencia_e_digito': numero_agencia +
                        '-'+digito_verificador_agencia}
            )

        except InvalidAccount:
            raise forms.ValidationError(
                self.error_messages['invalid_account'],
                code='invalid_account',
                params={'conta_e_digito': numero_conta_bancaria +
                        '-'+digito_verificador_conta_bancaria}
            )

        except InvalidBranchAndAccountCombination:
            raise forms.ValidationError(
                self.error_messages['invalid_branch_and_account_combination'],
                code='invalid_branch_and_account_combination',
                params={'agencia': numero_agencia,
                        'conta_e_digito': numero_conta_bancaria +
                        '-'+digito_verificador_conta_bancaria}
            )

        except InvalidBranchlength:
            raise forms.ValidationError(
                self.error_messages['invalid_branch_length'],
                code='invalid_branch_length',
                params={'banco': label_banco,
                        'agencia_length': bank_class.branch_length}
            )

        except InvalidAccountlength:
            raise forms.ValidationError(
                self.error_messages['invalid_account_length'],
                code='invalid_account_length',
                params={'banco': label_banco,
                        'conta_length': bank_class.account_length}
            )

        except MissingBranchDigit:
            raise forms.ValidationError(
                self.error_messages['missing_branch_digit'],
                code='missing_branch_digit',
                params={'banco': label_banco,
                        'digito_agencia_length': bank_class.branch_digit_length}
            )

        except UnexpectedBranchDigit:
            raise forms.ValidationError(
                self.error_messages['unexpected_branch_digit'],
                code='unexpected_branch_digit',
                params={'banco': label_banco,
                        'digito_agencia_length': bank_class.branch_digit_length}
            )

        except MissingAccountDigit:
            raise forms.ValidationError(
                self.error_messages['missing_account_digit'],
                code='missing_account_digit',
                params={'banco': label_banco,
                        'digito_conta_length': bank_class.account_digit_length}
            )

        except UnexpectedAccountDigit:
            raise forms.ValidationError(
                self.error_messages['unexpected_account_digit'],
                code='unexpected_account_digit',
                params={'banco': label_banco,
                        'digito_conta_length': bank_class.account_digit_length}
            )
