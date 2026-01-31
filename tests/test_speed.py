from src.gale_shapley import GaleShapley
from src.main import verify_matching
import numpy as np
import time
import matplotlib.pyplot as plt
import argparse


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--number", required=True, help="n * 500 to test up to", type=int
    )
    parser.add_argument(
        "-o", "--output", default="results.png", help="Path to save runtime plot comparing gs algorithm with the verifier"
    )
    return parser


def generate_pref_list(n: int, seed):
    """generate a random pref list with n objects"""

    rng = np.random.default_rng(seed)

    pref_list = {}
    ns = np.arange(1, n + 1)
    for i in range(1, n + 1):
        pref_list[i] = rng.permutation(ns).tolist()

    return pref_list


def test_times(n):
    """
    params
    n where n is 500 * n the testing will go to"""
    vals_to_test = [500 * i for i in range(n)]
    perf_times = []
    verif_times = []
    gs = GaleShapley()

    for val in vals_to_test:
        print(f"testing val {val}")
        pref_a = generate_pref_list(val, 11)
        pref_b = generate_pref_list(val, 12)

        st = time.perf_counter()
        res = gs.find_matches(pref_a, pref_b)
        perf_times.append(time.perf_counter() - st)

        st = time.perf_counter()
        verify_matching(res, pref_a, pref_b)
        verif_times.append(time.perf_counter() - st)

    return perf_times, verif_times


def test_and_graph(n, path_to_save):
    xs = [500 * i for i in range(n)]

    times = test_times(n)
    ys = times[0]  # For GS algorithm
    y2s = times[1] # For verifier

    plt.figure()

    plt.plot(xs, ys, marker="o", label="Gale-Shapley (GS)")
    plt.plot(xs, y2s, marker="x", label="Verifier")

    plt.title("Comparing GS and Verifier Times")

    plt.xlabel("N")
    plt.ylabel("Run time (s)")

    plt.grid(True, which="both", axis="x")
    plt.legend()

    plt.savefig(path_to_save)
    plt.close()


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.number <= 0:
        parser.error("--number must be a positive integer")

    test_and_graph(args.number, args.output)


if __name__ == "__main__":
    """run like this:
    python -m tests.test_speed --number="""
    main()
