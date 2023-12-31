from http import HTTPStatus

from rest_framework import exceptions
from rest_framework.views import Response, exception_handler


def custom_exception_handler(exception: Exception, context: dict):
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exception, context)

    # Only alter the response when it's a validation error
    if not isinstance(exception, exceptions.ValidationError):
        # TODO: rewrite this block to return all kinds of messages in project default
        # if response is not None:
        #     r = {
        #         'success': False,
        #         'statusCode': response.status_code,
        #         'message': ''
        #     }
        #     response.data = r

        return response

    # It's a validation error, there should be a Serializer
    view = context.get("view")
    serializer = view.get_serializer_class()()

    errors_list = []
    for key, details in response.data.items():

        if key in serializer.fields:
            label = serializer.fields[key].label
            help_text = serializer.fields[key].help_text

            for message in details:
                errors_list.append("{}: {}".format(label, message))

        elif key == "non_field_errors":
            for message in details:
                errors_list.append(message)

        else:
            for message in details:
                errors_list.append("{}: {}".format(key, message))

    # Using the description's of the HTTPStatus class as error message.
    http_code_to_message = {v.value: v.description for v in HTTPStatus}

    error_payload = {
        "statusCode": 0,
        "type": "ValidationError",
        "message": "",
        "errors": [],
    }

    #  error = error_payload["error"]
    status_code = response.status_code

    error_payload["statusCode"] = status_code
    error_payload["message"] = http_code_to_message[status_code]
    error_payload["errors"] = errors_list

    # Overwrite default exception_handler response data
    response.data = error_payload

    return response
