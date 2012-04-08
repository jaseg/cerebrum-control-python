#
# Copyright (c) 2009, Ben Wilber (benwilber@gmail.com)
# All rights reserved
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License. You should have
# received a copy of the GPL license along with this program; if you
# did not, you can find it at http://www.gnu.org/
#

class publicmethod(object):

    def __init__(self, method):
        self.method = method
        __public__  = True

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    def get_args(self):
        from inspect import getargspec
        return [ a for a in getargspec(self.method).args if a != "self" ]

class JsonRpc(object):

    def __init__(self, instance, allow_errors=True, report_methods=True):

        self.instance            = instance
        self.allow_errors        = allow_errors
        self.report_methods        = report_methods

        if not hasattr(self.instance, "url"):
            raise Exception("'url' not present in supplied instance")

    def get_public_methods(self):

        return [
            m for m in dir(self.instance) if \
            getattr(self.instance, m).__class__.__name__ == "publicmethod" and \
            getattr(self.instance, m).__public__ == True
        ]

    def generate_smd(self):

        smd = {
            "serviceType": "JSON-RPC",
            "serviceURL": self.instance.url(),
            "methods": []
        }

        if self.report_methods:
            smd["methods"] = [
                {"name": method, "parameters": getattr(self.instance, method).get_args()} \
                for method in self.get_public_methods()
            ]

        return simplejson.dumps(smd)
 
    def dispatch(self, method, params):

        if hasattr(self.instance, "dispatch") and \
            callable(self.instance.dispatch):
            return self.instance.dispatch(method, params)
        elif method in self.get_public_methods():
            return getattr(self.instance, method)(*params)
        else:
            return "no such method"

    def serialize(self, raw_post_data):

        raw_request        = simplejson.loads(raw_post_data)
        request_id        = raw_request.get("id", 0)
        request_method    = raw_request.get("method")
        request_params    = raw_request.get("params", [])

        response        = {"id": request_id}

        try:
            response["result"] = self.dispatch(request_method, request_params)
        except:
            if self.allow_errors:
                from sys import exc_type, exc_value
                response["error"] = "%s: %s" % (exc_type, exc_value)
            else:
                response["error"] = "error"

        return simplejson.dumps(response)

    def handle_request(self, request):

        if request.method == "POST" and \
            len(request.POST) > 0:
            return self.serialize(request.raw_post_data)
        else:
            return self.generate_smd()
