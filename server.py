import os

from server import app
from server.state import State

# Get the routes we created
from server.admin import *
from server.callbacks import *


@app.route("/")
def index():
    # TODO Make nice graphs here or in JS
    state = app.config["state"].state
    total = state["host_count"]
    results = ""

    for team, count in state["scores"].items():
        results += "Team {}: {}/{}\n<br>".format(team, count, total)

    print(results)
    return results


def main():
    app.config["state"] = State()  # TODO Open the DB here and

    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    try:
        port = os.environ.get("FLASK_PORT", "5000")
        port = int(port)
    except ValueError:
        port = 5000
    debug = os.environ.get("FLASK_DEBUG", "True")
    debug = debug.lower().strip() in ["true", "yes", "1", "t"]
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    main()
