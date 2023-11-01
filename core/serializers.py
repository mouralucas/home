from rest_framework import serializers


class CustomModelSerializer(serializers.ModelSerializer):
    """
    :Name: CustomSerializer
    :Created by: Lucas Penha de Moura - 09/03/2021
    :Edited by:

    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    If fields are None, all model fields are returned
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(CustomModelSerializer, self).__init__(*args, **kwargs)

        self.campos_bla = None

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CustomSerializer(serializers.Serializer):
    """
    :Name: CustomSerializer
    :Created by: Lucas Penha de Moura - 19/07/2023
    :Edited by:

    Create a customized version of the return json when validation fails
    """

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:

            custom_error_dict = {
                'success': False,
                'statusCode': exc.status_code,
                'errors': exc.detail,
            }

            for key, value in exc.detail.items():
                # Extract the string value using str() for each error message
                error_string = str(value[0])
                custom_error_dict['errors'][key] = error_string

            raise serializers.ValidationError(custom_error_dict)


class ReferenceGetSerializer(CustomSerializer):
    sMonth = serializers.IntegerField(required=False, min_value=1, max_value=12, default=1)
    sYear = serializers.IntegerField(required=False, default=2018)
    eMonth = serializers.IntegerField(required=False, min_value=1, max_value=12)
    eYear = serializers.IntegerField(required=False)
