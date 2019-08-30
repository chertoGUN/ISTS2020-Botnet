"""
Author: Micah Martin (knif3)
The state object keeps track of the scores and hosts that are allowed in the botnet
"""

import os
import time
import hashlib
import binascii

from .command import Command

DEFAULT_TOKEN = "WHITETEAMSAYSHI"

# Hosts for testing, can be anything
TESTING_HOSTS = [
    "10.80.100.1",
    "10.80.100.6",
    "10.80.100.11",
    "10.80.100.16",
    "10.80.100.21",
    "10.80.100.26",
    "10.80.100.31",
    "10.80.100.36",
    "10.80.100.41",
    "10.80.100.46",
    "10.80.100.51",
    "10.80.100.56",
    "10.80.100.61",
    "10.80.100.66",
    "10.80.100.71",
    "10.80.100.76",
    "10.80.100.81",
    "10.80.100.86",
    "10.80.100.91",
    "10.80.100.96",
]


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
        self.hosts = set(TESTING_HOSTS)
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

    def getCommands(self, team, ip):
        """
        Get commands for a host to run
        """
        if ip not in self.hosts:
            raise ValueError("Invalid IP address")
        team = str(team)
        if self.valid_teams and team not in self.valid_teams:
            raise ValueError("Invalid team")

        # Generate a command for the bot to run
        com = Command(team + ip)
        print(com)
        self.commands[team + ip] = com
        return com

    def checkResults(self, team, ip, results):
        if team + ip not in self.commands:
            raise ValueError("No command for id {}".format(command))

        self.commands[team + ip].check(results)
        # If an error has occured, it should be caught in the checkin function
        # If we get here, no errors have been raised the results were valid
        if team not in self.scores:
            self.scores[team] = {}
        self.scores[team][ip] = time.time()
        return True

    def isadmin(self, token):
        return hash_token(token.strip()) == self.ADMIN_TOKEN

    @property
    def state_admin(self):
        """The state for the admins which shows the compromised boxes"""
        retval = {
            "round_start": self.starttime,
            "scores": self.scores.copy(),
            "host_count": len(self.hosts),
        }
        return retval

    @property
    def state(self):
        """Non admin state which just shows how many hosts a team has"""
        retval = {
            "round_start": self.starttime,
            "host_count": len(self.hosts),
            "scores": {},
        }
        for team, hosts in self.scores.items():
            retval["scores"][team] = len(hosts)
        return retval


def hash_token(d):
    """Hash an admin token"""
    pwdhash = hashlib.pbkdf2_hmac("sha512", d.encode("utf-8"), b"SALTY", 100000)
    return binascii.hexlify(pwdhash).decode("ascii")
