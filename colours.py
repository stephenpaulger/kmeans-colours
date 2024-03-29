"""
K-means dominant colours

Usage: colours.py [-h] [-n N] filename

-n N    Number of dominant colours [default: 3].
"""

from collections import namedtuple
from math import sqrt
import random
import argparse

from PIL import Image


Point = namedtuple("Point", ("coords", "n", "ct"))
Cluster = namedtuple("Cluster", ("points", "center", "n"))


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color[:3], 3, count))
    return points


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


def colorz(filename, n=3):
    img = Image.open(filename)
    img.thumbnail((200, 200))

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rgb_to_hex, rgbs)


def euclidean(p1, p2):
    return sqrt(sum([(p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)]))


def calculate_center(points, n):
    vals = [0.0] * n
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += p.coords[i] * p.ct
    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for _ in range(k)]

        for p in points:
            idx = 0
            smallest_distance = float("Inf")
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


def main():
    parser = argparse.ArgumentParser(description="K-means dominant colours")
    parser.add_argument("filename", help="The filename of the image")
    parser.add_argument(
        "-n", type=int, default=3, help="Number of dominant colours (default: 3)"
    )
    args = parser.parse_args()

    for colour in colorz(args.filename, args.n):
        print(colour)


if __name__ == "__main__":
    main()
