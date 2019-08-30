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
        results += "Team {}: {}/{}\n".format(team, count, total)

    print(results)
    return results


def main():
    app.config["state"] = State()  # TODO Open the DB here and
    app.run(debug=True)


if __name__ == "__main__":
    main()
