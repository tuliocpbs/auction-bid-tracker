class ErrorGetInfoBidApi(Exception):
    """Raise when is not possible get information from Bid RestAPI"""
    def __init__(self):
        Exception.__init__(self,"Error get information from Bid API")