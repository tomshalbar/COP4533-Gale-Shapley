import argparse

from gale_shapley import GaleShapley

def parse_input(filename):
    """
        Parses the file provided by cleaning the input, storing hospital and student preferences, and sending a
        dictionary to the gale_shapley algorithm.

        Args:
            filename --> file to be parsed

        Returns a list of dicts if the file was found:
            1st element --> hospital preferences [int, list[int]]
            2nd element --> student preferences [int, list[int]]

    """

    try:
        with open(filename, 'r') as file:
            n = file.readline()

            hospital_preferences: dict[int, list[int]] = {}
            for hospital_id in range(int(n)):
                current_hospital_preferences = [int(num) for num in file.readline().split()]
                hospital_preferences[hospital_id+1] = current_hospital_preferences

            student_preferences: dict[int, list[int]] = {}
            for student_id in range(int(n)):
                current_student_preferences = [int(num) for num in file.readline().split()]
                student_preferences[student_id+1] = current_student_preferences

            return [hospital_preferences, student_preferences]
    except FileNotFoundError:
        return f"Error: '{filename}' was not found!"


def verify_matching():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parses input file, storing both hospital preferences and student "
                                     "preferences. It creates a map based on these preferences, and "
                                     "then passes them into the Gale-Shapley algorithm.")

    parser.add_argument("filename", type=str,
                        help="The input file (complete filepath from the home project directory). A simple example "
                             "would be "
                             "`python src/main.py input_files/example.in`")

    args = parser.parse_args()
    hospital_pref, student_pref = parse_input(args.filename)

    gs = GaleShapley()
    result = gs.find_matches(hospital_pref, student_pref)
    print(result)

    # Save output into a file
