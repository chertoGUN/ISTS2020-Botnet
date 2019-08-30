"""
A sample python client which implements the bot for testing
"""

import os
import requests
import subprocess


def main():
    server = "http://127.0.0.1:5000"
    ip = "10.80.100.26"
    team = "5"

    print("Getting commands: ", end="")
    url = "{}/{}/{}/linux".format(server, team, ip)

    # Get the commands from the server
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Fail")
        quit(1)
    print("Success")

    commands = resp.content
    # Run the commands
    print("Running the process: ", end="")
    try:
        proc = subprocess.Popen(
            "/bin/sh", stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(commands)
        proc.terminate()
    except Exception as E:
        print("Fail:", E)
        quit(1)

    print("Success")
    # Send the results back to the same URL but as a POST
    print("Validating Results: ", end="")
    resp = requests.post(url, stdout.decode("utf-8"))
    if resp.status_code != 200:
        print("Fail:", resp.content.decode("utf-8"))
        quit(1)
    print("Success")


if __name__ == "__main__":
    main()
