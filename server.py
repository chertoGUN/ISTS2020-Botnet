from server import app


@app.route("/")
def index():
    pass

def main():
    app.config['db'] = "" # TODO Open the DB here and 
    app.run(debug=True)

if __name__ == "__main__":
    main()