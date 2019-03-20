from .helpers import get, randomEl

templates = [
    "Is {name} {verb} {noun}?",
    "Is {name} {verb} {noun} {modifier}?",
    "{name} {verb} {noun}, you won't guess what happened next!",
    "{name} {verb} {noun} and you won't believe what happened next!"
]


def headline(star = False):
    if not star:
        star = get("clickbait/star")

    mode = randomEl(templates)

    noun = get("clickbait/noun")
    verb = get("clickbait/verb")
    modifier = get("clickbait/modifier")

    out = mode.format(name=star, verb=verb, noun=noun, modifier=modifier)

    return out

