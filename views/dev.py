from GlobalContext import API


@API.endpoint("endpoint-info", {
    'httpmethods': ['GET'],
    'httproute': '/dev/endpoint-info',
    'authlevel': 'public'
})
def endpointInfo(makeResponse, path=None, identifier=None):
    def JSONSafe(object):
        if isinstance(object, dict):
            current = {}
            for key, value in object.items():
                current[key] = JSONSafe(value)
            return current
        elif isinstance(object, list):
            current = []
            for value in object:
                current.append(JSONSafe(value))
            return current
        elif isinstance(object, str):
            return object
        elif isinstance(object, int):
            return object
        elif isinstance(object, float):
            return object
        elif isinstance(object, bool):
            return object
        elif object is None:
            return object
        else:
            return str(object)

    endpoints = {}
    if identifier:
        if identifier in API.endpointMap:
            endpoints[identifier] = API.endpointMap[identifier]
    if path:
        for identifier, endpoint in API.endpointMap.items():
            try:
                if endpoint['metadata']['httproute'] == path:
                    endpoints[identifier] = endpoint
            except Exception as e:
                return makeResponse(-1, f'Could not generate endpoint \
                    information for path {path}: {str(e)}')
    if not identifier and not path:
        endpoints = API.endpointMap
    if not endpoints:
        return makeResponse(-1, f'Could not find endpoint information for \
            path {path}. Please try again or use the identifier.')

    return makeResponse(0, endpoints=JSONSafe(endpoints))
