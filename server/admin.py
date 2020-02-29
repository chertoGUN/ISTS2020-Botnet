"""
Admin routes for the application

TODO: Implement these functions
"""


from flask import request, render_template, jsonify, abort

from . import app


def checkadmin():
    """This is a decorator that makes sure the caller has an ADMIN_TOKEN"""
    try:
        token = request.get_json(force=True).get("auth-token", "")
        if token and app.config["state"].isadmin(token):
            return True
    except Exception as E:
        print(type(E), E)

    abort(401, "Invalid ADMIN token")


@app.route("/admin/getscore")
def getScore():
    state = app.config["state"]
    return jsonify(state.state_admin)


@app.route("/admin/reset", methods=["POST"])
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
    """Show all the hosts that are allowed to callback"""
    checkadmin()
    state = app.config["state"]
    return jsonify({"hosts": state.getHosts()})


@app.route("/admin/sethosts", methods=["POST"])
def setHosts():
    """Set the valid hosts for the application
    
    Example:
    POST /admin/sethosts

    {
        "auth-token": "asdas"
        "hosts": {
            "8.8.8.8": "linux",
            "8.8.4.4": "windows"
        }
    }
    """
    checkadmin()
    state = app.config["state"]
    # Get the new hosts
    hosts = request.get_json(force=True).get('hosts')
    if not hosts:
        return jsonify({"error": "Invalid 'hosts' fields set"}), 400
    
    state.setHosts(hosts)
    return jsonify({"hosts": state.getHosts()})
