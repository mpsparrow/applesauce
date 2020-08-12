import requests
import json
from utils.logger import log

class Quiz():
    topics = {
        "General": 9,
        "Books": 10,
        "Movies": 11,
        "Music": 12,
        "Theatre": 13,
        "TV": 14,
        "Videogames": 15,
        "Boardgames": 16,
        "Science": 17,
        "Computers": 18,
        "Math": 19,
        "Mythology": 20,
        "Sports": 21,
        "Geography": 22,
        "History": 23,
        "Politics": 24,
        "Art": 25,
        "Celebrities": 26,
        "Animals": 27,
        "Vehicles": 28,
        "Comics": 29,
        "Technology": 30,
        "Anime": 31,
        "Cartoons": 32
    }

    difficulties = ["Easy", "Medium", "Hard"]

    def __init__(self, topic, num_questions, difficulty):
        self.topic = topic
        self.num_questions = num_questions
        self.difficutly = difficulty