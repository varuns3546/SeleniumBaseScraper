from pymongo import MongoClient
import os

def save_data():
    client = MongoClient("mongodb+srv://varunseenivasan82786:82786Vs2002!@cluster0.vdxciru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["web_scraper"]
    collection = db["scraped_data"]


    collection.insert_one({"HELLO": "world"})



save_data()