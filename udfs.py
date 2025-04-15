import re

from duckdb.typing import *
import editdistance
import jaro
import jellyfish


def edit_distance(a: str, b: str) -> int:
    # levenshtein distance
    s = editdistance.eval(a, b)
    return s


def soundex(s: str) -> str:
    return jellyfish.soundex(s)


def jaro_winkler(a: str, b: str) -> float:
    # jaro-winkler distance
    s = jaro.jaro_winkler_metric(a, b)
    return s


def get_trigrams_from_word(word: str) -> set[str]:
    s = "  " + word + " "
    return {s[i : i + 3] for i in range(len(s) - 2)}


def trigram(a: str, s: str) -> float:
    # Each word is considered to have two spaces prefixed and one space suffixed
    # Replace non-alphanumeric characters with spaces
    # The evaluation score is #trigrams_shared / #total_trigrams
    s_filtered = re.sub("[^0-9a-zA-Z]+", " ", s)
    a_filtered = re.sub("[^0-9a-zA-Z]+", " ", a)
    s_words = s_filtered.split()
    a_words = a_filtered.split()

    s_trigrams: set[str] = set()
    a_trigrams: set[str] = set()

    for word in s_words:
        s_trigrams.update(get_trigrams_from_word(word))
    for word in a_words:
        a_trigrams.update(get_trigrams_from_word(word))

    return len(s_trigrams.intersection(a_trigrams)) / len(s_trigrams.union(a_trigrams))


def custom_union(a: str, b: str) -> bool:
    if edit_distance(a, b) < 2:
        return True
    elif soundex(a) == soundex(b):
        return True
    elif jaro_winkler(a, b) > 0.95:
        return True
    elif trigram(a, b) > 0.95:
        return True
    return False


def custom_intersect(a: str, b: str) -> bool:
    if (
        (edit_distance(a, b) < 5)
        and (edit_distance(soundex(a), soundex(b)) < 5)
        and (jaro_winkler(a, b) > 0.5)
        and (trigram(a, b) > 0.5)
    ):
        return True
    return False

def tuned_metric(a: str, b: str) -> bool:
    if(edit_distance(a, b)/max(len(a),len(b)) > 0.333335) or (trigram(a, b) < 0.1): 
        return False
    if (jaro_winkler(a, b) > 0.74995): 
        if ((edit_distance(soundex(a), soundex(b)) < 1.1)):
            return True
    return False

# best design while maintaining 90% or above accuracy:
# Johnathan: 99.04, 1745
# Katheryne: 93.11, 1663
# trigram filter:  0.075 <= x <= 0.1
# normalized edit distance filter: 0.33333 <  x <= 0.333335
# jaro_winkler filter: 0.74995 <= x < 0.75 
# Allowed soundex diff: 1,0

#new
def custom_metric(a: str, b: str) -> bool:
    if((trigram(a, b) < 0.0555) or 
       (jaro_winkler(a, b) < 0.6875) or 
       (edit_distance(a, b)/max(len(a),len(b)) > 0.6675) or 
       (edit_distance(soundex(a), soundex(b)) > 1)
       ):
        return False
    return True

# trigram:
# 100%: 0.0555 <= x < 0.056
#jaro_winkler:
# 100%: 0.6875 <= x < 0.69
#Normalized Edit Distance Barriers:
# 100%: 0.665 < x <= 0.6675
#soundex:
# 100%: > 1


def register(con):
    # to call in other files, add this line: from udfs import register

    # add a seperate line for each UDF
    con.create_function("edit_distance", edit_distance, [VARCHAR, VARCHAR], INTEGER)
    con.create_function("jaro_winkler", jaro_winkler, [VARCHAR, VARCHAR], FLOAT)
    con.create_function("soundex", soundex, [VARCHAR], VARCHAR)
    con.create_function("trigram", trigram, [VARCHAR, VARCHAR], FLOAT)
    con.create_function("custom_union", custom_union, [VARCHAR, VARCHAR], bool)
    con.create_function("custom_metric", custom_metric, [VARCHAR, VARCHAR], bool)
    con.create_function("custom_intersect", custom_intersect, [VARCHAR, VARCHAR], bool)
