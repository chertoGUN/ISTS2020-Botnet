"""
Basic client that can be used to get information from the server

Author: Micah Martin
"""

import sys
import os
import requests

class BotnetAdminError(Exception):
    pass

class BotnetAdmin(object):
    def __init__(self, server, token=None):
        self.server = server.rstrip('/') + "/admin/"
        
        # Get the admin token, first check the value, then check environment
        if token:
            self.token = token
        else:
            token = os.environ.get("ADMIN_TOKEN", None)
            if not token:
                raise BotnetAdminError("Admin Token is not specified. Use ADMIN_TOKEN environment to pass it in")
            else:
                self.token = token

    def _send(self, method, data):
        """Handle the sending of data to the server"""
        endpoint = sys._getframe(1).f_code.co_name  # Calling function name is the endpoint
        if "auth-token" not in data:
            data['auth-token'] = self.token # add the auth token
        
        if method.lower() == 'post':
            resp = requests.post(self.server+endpoint, json=data)
        else:
            resp = requests.get(self.server+endpoint, json=data)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if "error" in data:
                    raise BotnetAdminError(data['error'])
                return data
            except ValueError:
                BotnetAdminError("Server did not send back valid json")
        elif resp.status_code == 400:
            try:
                data = resp.json()
                if "error" in data:
                    raise BotnetAdminError(data['error'])
                return data
            except ValueError:
                pass
            BotnetAdminError("An invalid request was sent to the server")
        elif resp.status_code in (403, 401):
            BotnetAdminError("You are not authorized to call this API function")
        raise BotnetAdminError("Invald response code: {}".format(resp.status_code))
    
    def getscore(self):
        """Get the current scores for the teams"""
        return self._send("get", {})

    def reset(self):
        """Reset all the current scores for the teams"""
        return self._send("post", {})

    def gethosts(self):
        """Get all the hosts that are allowed to call back"""
        return self._send("get", {})