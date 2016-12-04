__author__ = 'lee'


class Credentials(object):
    ## ABC

    def authenticate_request(self, request):
        raise NotImplemented("Nope")


class NoOpCredentials(Credentials):
    """
    These credentials are not much use outside of catalog methods.
    """
