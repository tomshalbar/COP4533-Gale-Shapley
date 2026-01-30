import argparse

from gale_shapley import GaleShapley
from collections.abc import Iterable  # Checking if a hospital is matched with multiple students
from pathlib import Path

def parse_input(filename) -> list[dict[int, list[int]]]:
    """
        Parses the file provided by cleaning the input, storing hospital and student preferences, and sending a
        dictionary to the gale_shapley algorithm.

        Args:
            filename --> file to be parsed

        Returns a list of dicts if the file was found:
            1st element --> hospital preferences [int, list[int]]
            2nd element --> student preferences [int, list[int]]

            - If there is an 'Error' an empty list is returned so that the output is empty and the program does not crash
    """

    if Path(filename).stat().st_size == 0:
        print("NOTE: the inputted file is empty!")
        return [{}, {}]

    try:
        with open(filename, 'r') as file:
            n = file.readline()
            hospital_preferences: dict[int, list[int]] = {}
            student_preferences: dict[int, list[int]] = {}

            for hospital_id in range(int(n)):
                current_hospital_preferences = [int(num) for num in file.readline().split()]
                hospital_preferences[hospital_id+1] = current_hospital_preferences

            for student_id in range(int(n)):
                current_student_preferences = [int(num) for num in file.readline().split()]
                student_preferences[student_id+1] = current_student_preferences

                if len(student_preferences[student_id+1]) != len(hospital_preferences[student_id+1]):
                    print("INVALID INPUT ERROR: the number of hospitals is not equal to the number of students")
                    return [{}, {}]

            return [hospital_preferences, student_preferences]
    except FileNotFoundError:
        print(f"INVALID INPUT ERROR: '{filename}' was not found!")
        return [{}, {}]


def write_output(hospital_student_matching: dict[int, int], output_file: str) -> None:
    """
        Writes the resulting match from the Gale Shapley algorithm into an output file in the directory 'output_files/'

        Args:
            result -> the match returned from the algorithm
            output_file -> the file being written to with a .out extension (e.g. example_1.in --> example_1.out)
    """

    # remove the file extension and add '.out'
    output_dir = "output_files/"
    output_file_path = output_dir + output_file[output_file.find('/') + 1 : output_file.find('.')] + ".out"

    # We now have a file that does not exist, we can write our data to it now
    with open(output_file_path, 'w') as file:
        for hospital in hospital_student_matching:
            student = hospital_student_matching[hospital]
            file.write(f"{hospital} {student}\n")


def verify_matching(matching: dict[int, int], hospital_preferences: dict[int, list[int]], student_preferences: dict[int, list[int]]) -> bool:
    """
        Verifies the matching of the Gale Shapley algorithm. Checks if each hospital and each student is matched to exactly one partner, with no duplicates.
        Lastly, it also checks for unstable/blocking pairs

        Args:
            matching -> the matching returned from the Gale-Shapley Algorithm   [hospital] -> student
            hospital_preferences -> the preferences of each hospital in descending order (first student is favorite)
            student_preferences -> the preferences of each student in descending order (first hospital is favorite)

        If the matching is valid, the program prints VALID STABLE and returns True
        If the matching is invalid, it prints out a clear failure message (e.g. INVALID [with reason] or UNSTABLE [with example blocking pair]) and returns False
    """

    hospitals_matched: list[int] = []
    students_matched: list[int] = []

    for hospital in matching:
        student = matching[hospital]

        # Make sure a hospital is only matched to 1 student
        if isinstance(student, Iterable):
            print(f"INVALID MATCHING: hospital({hospital}) is matched to more than one student!")
            return False

        # If a hospital was already matched, they should not try to match to another student
        if hospital in hospitals_matched:
            print(f"INVALID MATCHING: hospital({hospital}) is already matched and can't match with another student!")
            return False
        else:
            hospitals_matched.append(hospital)

        # If a student was already matched, they should not try to match to another hospital
        if student in students_matched:
            print(f"INVALID MATCHING: student({student}) is already matched and can't match with another hospital!")
            return False
        else:
            students_matched.append(student)

    # Need another for loop because the top one checks for a perfect matching (one-to-one relationship).
    # As a result, the verifier should only check for stability if there is a perfect matching, otherwise it would not work correctly

    reversed_matching = {val: key for key, val in matching.items()}  # Creates a reversed dict that allows us to query what hospital a student is matched to efficiently
    for hospital in matching:
        student = matching[hospital]

        # First find where the student is located in the hospital's preference list
        student_pos: int = hospital_preferences[hospital].index(student)

        # If it's not at position 0, the hospital prefers another student over its current matching
        if student_pos != 0:
            # Iterate over the students in the hospital's preference list that come before the current matching student
            for i in range(student_pos):
                # If any of these students also prefer this current hospital over their matched hospital --> UNSTABLE PAIR
                preferred_student = hospital_preferences[hospital][i]
                preferred_student_hospital = reversed_matching[preferred_student]
                preferred_student_hospital_pos = student_preferences[preferred_student].index(preferred_student_hospital)
                for j in range(preferred_student_hospital_pos):
                    if student_preferences[preferred_student][j] == hospital:
                        print(f"INVALID MATCHING: (h{hospital}, s{preferred_student}) are an unstable pair!")
                        return False

    if len(matching) == 0:
        return False

    # If the verifier made it this far then the matching is stable
    print("VALID STABLE")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parses input file, storing both hospital preferences and student "
                                     "preferences. It creates a map based on these preferences, and "
                                     "then passes them into the Gale-Shapley algorithm.")

    parser.add_argument("filename", type=str,
                        help="The input file (complete filepath from the home project directory). A simple example "
                             "would be "
                             "`python src/main.py input_files/example_1.in`")

    args = parser.parse_args()
    hospital_pref, student_pref = parse_input(args.filename)

    gs = GaleShapley()
    result = gs.find_matches(hospital_pref, student_pref)
    verify_matching(result, hospital_pref, student_pref)
    write_output(result, args.filename)
