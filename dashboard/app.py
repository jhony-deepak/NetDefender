from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    alerts = []
    with open("alerts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            alerts.append(row)
    return render_template("index.html", alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5050)