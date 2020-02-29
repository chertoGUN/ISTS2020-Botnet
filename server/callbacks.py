"""
Routes for the application to receive callbacks

TODO: Implement these functions
"""

from flask import request, render_template, jsonify
from . import app

@app.route("/status")
def status():
    return jsonify({"status": "Botnet is running"})

@app.route('/')
def scores():
    state = app.config["state"]
    return render_template("index.html", state=state.state)


@app.route("/callback", methods=["GET", 'PUT'])
def get_commands():
    """Expects a JSON object of the following format:
    {
        "team": "10",
        "ip": "8.8.8.8",
        "user": "root"
    }

    Returns:
    {
        "id": 2818355651907523309,
        "command": "echo cvikkoyquvlrvnkpkntbultvxkmwnp",
        "type": "linux",
        "team": "10",
        "ip": "8.8.8.8",
    }

    If there is an error, return the following JSON
    {
        "error": "random error message"
    }
    """
    state = app.config["state"]
    data = request.get_json(force=True)
    try:
        team = data.get("team", False)
        if not team:
            raise ValueError("'team' not specified")
        # TODO: Do we want to get the IP from the request instead of trusting blue team?
        ip = data.get("ip", False)
        if not ip:
            raise ValueError("'ip' not specified")
        
        # Validate that they arent faking the ips
        if ip not in request.access_route:  
            raise ValueError("specified ip does not match incoming request ip '{}'".format(request.remote_addr))

        user = data.get("user", False)
        if not user:
            raise ValueError("'user' not specified")

        return jsonify(state.getCommands(team, ip, user))

    except ValueError as E:
        return jsonify({"error": str(E)}), 400

@app.route("/callback", methods=["POST"])
def return_results():
    """Expects a JSON object of the following format:
    {
        "id": "0000-0000-0000-0000",
        "results": "results of the command",
    }

    Returns:
    {
        "id": "0000-0000-0000-0000",
        "msg": "successful check in",
        "ip": "8.8.8.8",
        "time": 120000.00
    }

    If there is an error, return the following JSON
    {
        "error": "random error message"
    }
    """
    
    state = app.config["state"]
    data = request.get_json(force=True)
    try:
        com_id = data.get("id", False)
        if not com_id:
            raise ValueError("'id' not specified")
        results = data.get("results", False)
        if results is False:
            raise ValueError("'results' not specified")
        results = str(results)
        return jsonify(state.checkResults(com_id, results))

    except ValueError as E:
        print(E)
        return jsonify({"error": str(E)}), 400
