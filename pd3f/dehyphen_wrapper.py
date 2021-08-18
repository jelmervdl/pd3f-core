"""Interaction with `dehyphen`, cache results
"""


from dehyphen import FlairScorer


def get_scorer(lang):
    # simplify Flair's naming of models
    if lang.endswith("-fast"):
        scorer = FlairScorer(lang=lang[:-5], fast=True)
    else:
        scorer = FlairScorer(lang=lang)
    return scorer


def dehyphen_paragraph(scorer, lines):
    return scorer.dehyphen_paragraph(lines)


def is_split_paragraph(scorer, p1, p2):
    return scorer.is_split_paragraph(p1, p2)


def newline_or_not(scorer, l1, l2):
    """Decide whether to add a newline or not.
    """
    # Flair does not work with only one char, thus this special case
    if len(l1) == 1 and len(l1[0]) == 1:
        return True
    if len(l2) == 1 and len(l2[0]) == 1:
        return False
    
    texts = [l1, l2, l1 + " " + l2]
    scores = scorer.score(texts)
    best_score_idx = scores.index(min(scores))
    return best_score_idx != 2


def single_score(scorer, text):
    # Flair does not work with only one char, thus this special case
    if len(text) == 1:
        return float("inf")
    return scorer.score([text])[0]
