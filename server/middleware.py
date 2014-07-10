import json

from django import http


RESPONSE_TYPES = {
    400: http.HttpResponseBadRequest,
    404: http.HttpResponseNotFound,
    500: http.HttpResponseServerError,
}
DEFAULT_RESPONSE_TYPE = http.HttpResponse


class JSONException(Exception):
    pass


class JSONExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, JSONException):
            return None

        message, code = exception.args
        data = {"error": message}

        response_type = RESPONSE_TYPES.get(code, DEFAULT_RESPONSE_TYPE)
        response = response_type(content_type="application/json")

        # Dumps the data straight into the response as IO
        json.dump(data, response)

        return response


class JSONRequestMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'body') or not request.body:
            return

        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            json_str = request.body.decode(encoding='UTF-8')
            setattr(
                request,
                request.method,
                {} if not json_str else json.loads(json_str)
            )
