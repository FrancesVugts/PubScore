import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'PubScore'
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/overview")
def overview():
    return render_template("overview.html",
                           competitors=mongo.db.competitors.find())


@app.route('/deleteteam/<competitor_id>')
def deleteteam(competitor_id):
    mongo.db.competitors.remove({'_id': ObjectId(competitor_id)})
    return redirect(url_for('overview'))


@app.route("/updatecompetition")
def updatecompetition():
    return render_template("updatecompetition.html",
                           competitors=mongo.db.competitors.find())


@app.route("/addteam")
def addteam():
    return render_template("addteam.html")


@app.route('/insertteam', methods=['POST'])
def insertteam():
    competitors = mongo.db.competitors
    competitors.insert_one(request.form.to_dict())
    return redirect(url_for('overview'))


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
