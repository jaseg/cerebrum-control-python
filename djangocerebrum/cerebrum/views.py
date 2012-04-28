from djangorestframework.response import Response
from djangorestframework import status,views
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from jsonrpc import JsonRpc, publicmethod
from django.http import HttpResponse
from djangocerebrum.cerebrum import panel_driver
from djangocerebrum.cerebrum.panel_driver import LAMP_COUNT, METER_COUNT
import logging

log = logging.getLogger()
#log.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log.debug("Loading views")

#Home page

def home(request):
    return HttpResponse("Hail Eris!")

#REST driver interface

class PanelDriverRestView(views.View):
    def get(self, request):
        return {"lamps": [reverse('panel-lamp', kwargs={'num': num}) for num in range(LAMP_COUNT)], "meters": [reverse('panel-meter', kwargs={'num': num}) for num in range(METER_COUNT)]}

class PanelLampRestView(views.View):
    def get(self, request, num):
        if int(num) > LAMP_COUNT:
            return Response(status.HTTP_404_NOT_FOUND)
        return {"val": panel_driver.PanelDriver.driver.get_lamp(num)}

    def post(self, request, num):
        if int(num) > LAMP_COUNT:
            return Response(status.HTTP_404_NOT_FOUND)
        return {"val": panel_driver.PanelDriver.driver.set_lamp(num, request.POST['val'])}

class PanelMeterRestView(views.View):
    def get(self, request, num):
        if int(num) > METER_COUNT:
            return Response(status.HTTP_404_NOT_FOUND)
        return {"val": panel_driver.PanelDriver.driver.get_meter(num)}

    def post(self, request, num):
        if int(num) > METER_COUNT:
            return Response(status.HTTP_404_NOT_FOUND)
        return {"val": panel_driver.PanelDriver.driver.set_meter(num, request.POST['val'])}

#JSON-RPC driver interface

class PanelDriverRpcWrapper(object):
    def url():
        return reverse("panel-rpc")

    def __init__(self, driver):
        panel_driver.PanelDriver.driver = driver

    @publicmethod
    def get_lamp(self, num):
        return self.get_lamp(num)

    @publicmethod
    def set_lamp(self, num, val):
        return self.set_lamp(num, val)

    @publicmethod
    def get_meter(self, num):
        return self.get_meter(num)

    @publicmethod
    def set_meter(self, num, val):
        return self.set_meter(num, val)

    @classmethod
    def getInterface(cls, driver):
       return JsonRpc(PanelDriverRpcWrapper(driver)).handle_request.im_func
