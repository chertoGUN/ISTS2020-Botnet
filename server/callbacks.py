"""
Routes for the application to receive callbacks

TODO: Implement these functions
"""

from flask import Request, render_template
from . import app

@app.route("/<team>/<ip>/linux")
def callbackLinux(team, ip):
    pass

@app.route("/<team>/<ip>/windows")
def callbackWindows(team, ip):
    pass
