from functools import wraps
import warnings

class RequestMap():
    def __init__(self):
        self.request_map = {}

    def register_request(self, route, *args, name=None, **kw):
        def _register_request(func):
            # Added compatibility layer such that when the function is directly called, it works as if it wasn't registered.
            @wraps(func)
            def __register_request(*fargs, **fkw):
                return func(*fargs, **fkw)

            if route in self.request_map and self.request_map[route]['func'] != func:
                warnings.warn(
                    f'WARNING: Handler {self.request_map[route]["func"].__name__} is already mapped to route {route}. It is now being overwritten by {func.__name__}.')
            # The decorator has been called, so register the request.
            self.request_map[route] = {
                'args': args,
                'kw': kw,
                'func': func,
                'name': name if name != None else func.__name__
            }
            return __register_request
        return _register_request

    def handle_flask(self, app):
        '_channel = flask'
        for route in self.request_map:
            try:
                app.add_url_rule(
                    route, self.request_map[route]['name'], self.request_map[route]['func'], *self.request_map[route]['args'], **self.request_map[route]['kw'])
            except Exception as e:
                raise RuntimeError(
                    'Can not handle flask due to flask exception.')

        # return app.route(route, *args, **kw)
