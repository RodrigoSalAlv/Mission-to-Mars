#The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
#The second line says we'll use PyMongo to interact with our Mongo database
#The third line says that to use the scraping code, we will convert from Jupyter notebook to Python

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)


# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach 
# Mongo through our localhost server, using port 27017, using a database named "mars_app".
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, 
    # which we will create when we convert our Jupyter scraping code to Python Script
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


#This route will be the "button" of the web application, the one that will scrape updated data when we tell it to from the homepage of our web app
#The first line, @app.route(“/scrape”) defines the route that Flask will be using
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   #e created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all(). 
   # In this line, we're referencing the scrape_all function in the scraping.py 
   mars_data = scraping.scrape_all()
   #we need to update the database using .update_one()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)


if __name__ == "__main__":
   app.run()