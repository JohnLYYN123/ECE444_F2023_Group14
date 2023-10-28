from flask import Flask

# create and initialize a new Flask app
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/main_page")
def main_page():
    return "Main Page"


if __name__ == "__main__":
    app.run()
