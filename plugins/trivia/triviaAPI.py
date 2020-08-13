import requests
import json
import urllib.parse as parse
from utils.logger import log

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

topic_list = [x.lower() for x in list(topics.keys())]

difficulties = ["easy", "aedium", "hard"]

class Question():
    def __init__(self, question):
        self.type = question["type"]
        self.category = parse.unquote_plus(question["category"])
        self.difficulty = question["difficulty"].title()
        self.question = parse.unquote_plus(question["question"])
        self.answer = parse.unquote_plus(question["correct_answer"])
        self.wrong_answers = [parse.unquote_plus(x) for x in question["incorrect_answers"]]

class Quiz():
    def __init__(self, topic, num_questions, difficulty):
        self.topic = topic
        if self.topic is not None:
            self.topic = self.topic.lower()
        self.num_questions = num_questions
        self.difficulty = difficulty
        if self.difficulty is not None:
            self.difficulty = self.difficulty.lower()
        self.questions = []
        self.get_questions()

    def get_questions(self):
        self.questions.clear()
        url = f"https://opentdb.com/api.php?amount={self.num_questions}&encode=url3986"
        if self.topic is not None:
            url += f"&category={topics[self.topic.title()]}"
        if self.difficulty is not None:
            url += f"&difficulty={self.difficulty}"

        r = requests.get(url)
        if r.status_code != 200:
            log.error(f"Couldn't reach Trivia API: {r.status_code}")
            return
            
        data = json.loads(r.text)
        if data["response_code"] != 0:
            log.error(f"Trivia API returned following response code: {data['response_code']}")
            return

        for question in data["results"]:
            self.questions.append(Question(question))
