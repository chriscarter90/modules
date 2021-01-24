# Token: e81b2022-d932-45ad-9752-1ebad52b5aa7
# Docs: http://lite.realtime.nationalrail.co.uk/openldbws/

from .nr_service import NRService
from zeep import Client


class NRClient:
    WSDL = 'https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'

    def __init__(self, token=None):
        self.client = Client(wsdl=self.WSDL)
        self.token = token

    def get_departure_board(self, stn, rows, to=None):
        deps = self.client.service.GetDepartureBoard(
            numRows=rows,
            crs=stn,
            filterCrs=to,
            filterType="to",
            timeOffset=None,
            timeWindow=None,
            _soapheaders={'AccessToken': self.token})

        return list(
            map(
                lambda obj: NRService(obj),
                deps['trainServices']['service'],
            ))
