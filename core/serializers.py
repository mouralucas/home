import warnings

from rest_framework import serializers

import core.models


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        self.campos_bla = None

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TipoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = core.models.Tipo
        fields = '__all__'


class IdiomaSerializer(DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = core.models.Language
        fields = '__all__'


class MunicipioSerializer(DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = core.models.Municipio
        fields = '__all__'


class CepSerializer(DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = core.models.Cep
        fields = '__all__'


class CategoriaSerializer(DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = core.models.Category
        fields = '__all__'


class StatusSerializer(DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = core.models.Status
        fields = '__all__'


class PaisSerializer(DynamicFieldsModelSerializer):
    warnings.warn('All serializers deprecated!!', DeprecationWarning, stacklevel=2)

    class Meta:
        model = core.models.Country
        fields = '__all__'
