import warnings

import core.serializers
import finance.models


class ContaBancarioSerializer(core.serializers.DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = finance.models.BankAccount
        fields = '__all__'


class CartaoCreditoSerializer(core.serializers.DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = finance.models.CreditCard
        fields = '__all__'


class FaturaSerializer(core.serializers.DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = finance.models.CreditCardBill
        fields = '__all__'
