from flask import Flask
app = Flask(__name__)


@app.route("/")
def main():
    return "H3ll0 :)"


if __name__ == "__main__":
  app.run()