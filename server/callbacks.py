"""
Routes for the application to receive callbacks

TODO: Implement these functions
"""

from flask import request, render_template
from . import app


@app.route("/<team>/<ip>/linux", methods=["GET", "POST"])
def callbackLinux(team, ip):
    state = app.config["state"]
    try:
        if request.method == "POST":
            results = request.data.decode("utf-8")
            state.checkResults(team, ip, results)
            return "Success"
        else:
            command = state.getCommands(team, ip)
            return "{}".format(command)
    except Exception as E:
        return str(E), 400


@app.route("/<team>/<ip>/windows")
def callbackWindows(team, ip):
    # TODO: replicate the windows callback after updating the linux callback
    pass
