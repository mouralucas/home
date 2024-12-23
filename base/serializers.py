from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import empty


# Default serializers for the system
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
            custom_error_dict = self.customize_errors(exc)
            raise serializers.ValidationError(custom_error_dict)

    def run_validation(self, data=empty):
        """
        We override the default `run_validation`, because the validation
        performed by validators and the `.validate()` method should
        be coerced into an error dictionary with a 'non_fields_error' key.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        try:
            self.run_validators(value)
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except (ValidationError, DjangoValidationError) as exc:
            custom_error_dict = self.customize_errors(exc)
            raise serializers.ValidationError(custom_error_dict)

        return value

    def customize_errors(self, exc):
        custom_error_dict = {
            'success': False,
            'statusCode': exc.status_code,
            'errors': {},
        }

        if isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                # Extract the string value using str() for each error message
                error_string = str(value[0])
                custom_error_dict['errors'][key] = error_string
        else:
            custom_error_dict['errors'] = {
                'non_field_errors': exc.detail
            }

        return custom_error_dict
