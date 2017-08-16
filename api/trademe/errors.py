from api.error import ApiError


class TradeMeError(ApiError):

    def __init__(self, code, description, data=None, url=None):
        # Make the exception picklable by calling super.
        super().__init__(code, description, data, url=url)
        self.code = code
        self.description = description
        self.data = data


class ClassifiedExpiredError(TradeMeError):
    pass


def raise_for_error_key(api_response):
    if not isinstance(api_response, dict):
        # Not a dictionary, so no errors can be reported.
        return
    err_desc = {
        'ErrorDescription': api_response.get('ErrorDescription', None),
    }
    err_requ = api_response.get('Request', None)
    if 'Error' not in api_response and 'ErrorDescription' not in api_response:
        return
    elif 'Error' not in api_response:
        raise TradeMeError(
            code='Unknown',
            description=err_desc,
            url=err_requ
        )
    error_dict = api_response['Error']
    if 'DeveloperDescription' in error_dict:
        err_desc['DeveloperDescription'] = error_dict['DeveloperDescription']
    if 'UserDescription' in error_dict:
        err_desc['UserDescription'] = error_dict['UserDescription']
    err_code = error_dict['Code']
    err_data = error_dict.get('ErrorData', None)
    if err_code == 'ClassifiedExpired':
        raise ClassifiedExpiredError(err_code, err_desc, err_data, err_requ)
    else:
        raise TradeMeError(err_code, err_desc, err_data, request=err_requ)
