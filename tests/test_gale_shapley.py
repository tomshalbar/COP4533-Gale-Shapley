from src.gale_shapley import GaleShapley
from src.main import verify_matching

gs = GaleShapley()

def test_simple_gs():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 3, 1],
        3: [2, 1, 3]
    }
    s_pref: dict[int, list[int]] = {
        1: [2, 1, 3],
        2: [1, 2, 3],
        3: [1, 2, 3]
    }
    assert gs.find_matches(h_pref, s_pref) == {
        1: 1,
        2: 2,
        3: 3
    }

def test_simple_verification():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [3, 2, 1]
    }
    s_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [1, 2, 3]
    }
    matching: dict[int, int] = {
        1: 1,
        2: 2,
        3: 3
    }
    assert verify_matching(matching, h_pref, s_pref) == True

def test_invalid_verification():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [3, 2, 1]
    }
    s_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [1, 2, 3]
    }
    matching: dict[int, int] = {
        1: 2,
        2: 1,
        3: 3
    }
    assert verify_matching(matching, h_pref, s_pref) == False

def test_invalid_missing_val():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [3, 2, 1]
    }
    s_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [1, 2, 3]
    }
    matching: dict[int, int] = {
        1: 2,
        2: 1,
        3: 0
    }
    assert verify_matching(matching, h_pref, s_pref) == False

def test_invalid_duplicated_student():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [1, 2, 3]
    }
    s_pref: dict[int, list[int]] = {
        1: [3, 2, 1],
        2: [1, 2, 3],
        3: [3, 2, 1]
    }
    matching: dict[int, int] = {
        1: 3,
        2: 1,
        3: 3
    }
    assert verify_matching(matching, h_pref, s_pref) == False

def test_simple_correct_verification():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [1, 2, 3]
    }
    s_pref: dict[int, list[int]] = {
        1: [2, 1, 3],
        2: [1, 2, 3],
        3: [1, 2, 3]
    }
    matching = {
        1: 2,
        2: 1,
        3: 3
    }
    assert verify_matching(matching, h_pref, s_pref) == True

def test_unstable_pairs():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [3, 2, 1],
        3: [2, 3, 1]
    }
    s_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [1, 2, 3],
        3: [1, 3, 2]
    }
    matching = {
        1: 2,
        2: 3,
        3: 1
    }
    assert verify_matching(matching, h_pref, s_pref) == False

def test_stable_pairs():
    h_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [3, 2, 1],
        3: [2, 3, 1]
    }
    s_pref: dict[int, list[int]] = {
        1: [1, 2, 3],
        2: [1, 2, 3],
        3: [1, 3, 2]
    }
    matching = {
        1: 1,
        2: 2,
        3: 3
    }
    assert verify_matching(matching, h_pref, s_pref) == True