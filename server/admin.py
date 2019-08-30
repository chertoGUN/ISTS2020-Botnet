"""
Admin routes for the application

TODO: Implement these functions
"""


from flask import request, render_template, jsonify, abort

from . import app


def checkadmin():
    """This is a decorator that makes sure the caller has an ADMIN_TOKEN"""
    token = request.headers.get("ADMIN_TOKEN", "")
    if not token or not app.config["state"].isadmin(token):
        abort(401, "Invalid ADMIN token")


@app.route("/admin/score")
def getScore():
    checkadmin()
    state = app.config["state"]
    return jsonify(state.state_admin)


@app.route("/admin/reset")
def resetScore():
    checkadmin()
    state = app.config["state"]
    return jsonify(state.reset())


@app.route("/admin/edit")
def editScore():
    # TODO
    pass


@app.route("/admin/gethosts")
def getHosts():
    # TODO
    pass


@app.route("/admin/sethosts")
def setHosts():
    # TODO
    pass
