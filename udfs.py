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
    if edit_distance(a, b) < 3:
        return True
    elif soundex(a) == soundex(b):
        return True
    elif jaro_winkler(a, b) > 0.8:
        return True
    elif trigram(a, b) > 0.7:
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


def register(con):
    # to call in other files, add this line: from udfs import register

    # add a seperate line for each UDF
    con.create_function("edit_distance", edit_distance, [VARCHAR, VARCHAR], INTEGER)
    con.create_function("jaro_winkler", jaro_winkler, [VARCHAR, VARCHAR], FLOAT)
    con.create_function("soundex", soundex, [VARCHAR], VARCHAR)
    con.create_function("trigram", trigram, [VARCHAR, VARCHAR], FLOAT)
    con.create_function("custom_union", custom_union, [VARCHAR, VARCHAR], bool)
    con.create_function("custom_intersect", custom_intersect, [VARCHAR, VARCHAR], bool)
