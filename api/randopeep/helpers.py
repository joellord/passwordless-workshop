import json
import random

with open("./randopeep/data/data.json") as f:
    data = json.load(f)


def get(section):
    return randomEl(data[section])


def randomEl(array):
    return array[random.randint(0, len(array) - 1)]