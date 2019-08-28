"""
Admin routes for the application

TODO: Implement these functions
"""


from flask import Request, render_template
from . import app

@app.route("/admin/score")
def getScore():
    pass


@app.route("/admin/reset")
def resetScore():
    pass


@app.route("/admin/edit")
def editScore():
    pass


@app.route("/admin/gethosts")
def getHosts():
    pass

@app.route("/admin/sethosts")
def setHosts():
    pass


