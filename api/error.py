

class ApiError(Exception):

    def __init__(self, *args, url):
        super().__init__(*args, url)
        self.url = url


class ApiConnectionError(ApiError):

    pass
