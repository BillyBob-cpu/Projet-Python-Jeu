import json
import os

def load_high_score():
    path = "data/scores.json"
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    except:
        return 0

def save_high_score(current_score):
    path = "data/scores.json"
    best_score = load_high_score()
    
    if current_score > best_score:
        data = {"high_score": current_score}
        with open(path, "w") as file:
            json.dump(data, file)