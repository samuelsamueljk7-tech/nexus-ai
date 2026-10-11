from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():

    return render_template(
        "index.html"
    )


print()
print("==============================")
print("       SPARK IS ONLINE")
print("==============================")
print()
print("Open:")
print("http://127.0.0.1:5000")
print()


app.run(
    host="127.0.0.1",
    port=5000,
    debug=False
)