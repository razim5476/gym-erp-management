"""
Common API response helpers.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_response(
    *,
    success=True,
    message="",
    data=None,
    errors=None,
    status_code=status.HTTP_200_OK,
):
    """
    Return one response shape across the project.
    """

    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
            "errors": errors,
        },
        status=status_code,
    )


def success_response(message="", data=None, status_code=status.HTTP_200_OK):
    """
    Standard success response.
    """

    return api_response(
        success=True,
        message=message,
        data=data,
        errors=None,
        status_code=status_code,
    )


def error_response(
    message="Something went wrong.",
    errors=None,
    status_code=status.HTTP_400_BAD_REQUEST,
):
    """
    Standard error response.
    """

    return api_response(
        success=False,
        message=message,
        data=None,
        errors=errors,
        status_code=status_code,
    )


def custom_exception_handler(exc, context):
    """
    Wrap DRF errors in the project response format.
    """

    response = exception_handler(exc, context)

    if response is None:
        return None

    detail = response.data
    message = "Request failed."

    if isinstance(detail, dict) and "detail" in detail:
        message = str(detail["detail"])
    elif isinstance(detail, list) and detail:
        message = str(detail[0])

    response.data = {
        "success": False,
        "message": message,
        "data": None,
        "errors": detail,
    }
    return response
