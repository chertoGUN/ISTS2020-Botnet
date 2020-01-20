"""
Author: Micah Martin (knif3)
The state object keeps track of the scores and hosts that are allowed in the botnet
"""

import os
import time
import hashlib
import binascii

from .command import generateCommand

DEFAULT_TOKEN = os.environ.get("ADMIN_TOKEN", "adminadmin")

# Hosts for testing, can be anything
TESTING_HOSTS = {
    "192.168.177.195": "linux"
}


class State(object):
    """
    starttime: When the stores for this round started
    teams: a dictionary mapping teams to the hosts that have called back in the past X minutes
    hosts: a set of hosts that is allowed to be in the botnet
    """

    def __init__(self, db=None):
        self.starttime = time.time()
        self.scores = {}
        self.valid_teams = []
        self._hosts = TESTING_HOSTS
        self.commands = {}

        # If we dont have an admin token, create one
        if not os.path.exists(".admin_token"):
            with open(".admin_token", "w") as fil:
                self.ADMIN_TOKEN = hash_token(DEFAULT_TOKEN)
                fil.write(self.ADMIN_TOKEN)
        else:
            # Load the admin token
            with open(".admin_token") as fil:
                self.ADMIN_TOKEN = fil.read().strip()

    def reset(self):
        """Reset all the variables in the state object and return the scores for the round"""
        retval = self.state
        retval["round_end"] = time.time()
        self.scores = {}
        self.starttime = time.time()
        return retval

    def getHosts(self):
        """Get the valid hosts"""
        return self._hosts
    
    def setHosts(self, hosts):
        """Set the valid hosts here
        TODO: Maybe validate that the hosts are legit or something?
        """
        self._hosts = hosts

    def getCommands(self, team, ip, user):
        """
        Get commands for a host to run. Returns the following JSON
        {
            "id": 2818355651907523309,
            "command": "echo cvikkoyquvlrvnkpkntbultvxkmwnp",
            "type": "linux",
        }
        """
        if ip not in self._hosts:
            raise ValueError("unknown IP address: {}".format(ip))
        team = str(team)
        if self.valid_teams and team not in self.valid_teams:
            raise ValueError("unknown team: {}".format(team))

        # Generate a command for the bot to run
        host_type = self._hosts[ip]
        com = generateCommand(host_type, team, ip, user)
        # Store the command for later
        self.commands[com.id] = com
        return com.json()

    def checkResults(self, com_id, results):
        """When a bot calls back with results, see if they are right
        """
        print(self.commands)
        command = self.commands.get(com_id, None)
        if not command:
            raise ValueError("No command for id {}".format(command))

        # This function will ValueError if the reults are wrong
        command.check(results)

        # If we get here, no errors have been raised the results were valid
        if command.team not in self.scores:
            self.scores[command.team] = {}
        
        timestamp = time.time()
        # Mark this host as valid
        self.scores[command.team][command.ip] = timestamp

        return {
            "id":com_id,
            "msg": "successful check in",
            "ip": command.ip,
            "time": timestamp
        }


    def isadmin(self, token):
        """Check if the given token is an administrator"""
        return hash_token(token.strip()) == self.ADMIN_TOKEN

    @property
    def state_admin(self):
        """The state for the admins which shows the compromised boxes"""
        retval = {
            "round_start": self.starttime,
            "scores": self.scores.copy(),
            "host_count": len(self._hosts),
        }
        return retval

    @property
    def state(self):
        """Non admin state which just shows how many hosts a team has"""
        retval = {
            "round_start": self.starttime,
            "host_count": len(self._hosts),
            "scores": {},
        }
        for team, hosts in self.scores.items():
            retval["scores"][team] = len(hosts)
        return retval


def hash_token(d):
    """Hash an admin token"""
    pwdhash = hashlib.pbkdf2_hmac("sha512", d.encode("utf-8"), b"SALTY", 100000)
    return binascii.hexlify(pwdhash).decode("ascii")
