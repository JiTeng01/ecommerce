from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def success_response(response_data=None):
    response = dict(status=HTTP_200_OK)
    if response_data:
        response.update(response_data)
    return response


def error_response(response_data=None):
    response = dict(status=HTTP_400_BAD_REQUEST)
    if response_data:
        response.update(response_data)
    return response

