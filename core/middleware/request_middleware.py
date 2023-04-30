class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request_dict_keys(['environ', 'path_info', 'path', 'META', 'method', 'content_type', 'content_params',
        # '_stream', '_read_started', 'resolver_match', 'COOKIES', 'session', 'user', '_messages'])
        response = self.get_response(request)
        return response
