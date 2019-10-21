from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def home():
    mars_data = list(mongo.db.mars_data.find())
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars = scrape_mars.scrape()
    mars_data.update({}, mars, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
