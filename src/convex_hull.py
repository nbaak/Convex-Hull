from typing import List, Tuple
import math

Point = Tuple[int, int]

# QuickHull Algorithm
def quick_hull(points: List[Point]) -> List[Point]:
    if len(points) < 3:
        return points

    def cross_product(o: Point, a: Point, b: Point) -> int:
        # Cross product of vectors OA and OB. Positive if counterclockwise, negative if clockwise.
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def distance(p1: Point, p2: Point, p: Point) -> float:
        # Distance from point p to the line formed by p1 and p2
        return abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1]))

    def hull_part(p1: Point, p2: Point, points: List[Point]) -> List[Point]:
        if not points:
            return []

        farthest_point = max(points, key=lambda p: distance(p1, p2, p))
        left_of_line = [p for p in points if cross_product(p1, farthest_point, p) > 0]
        right_of_line = [p for p in points if cross_product(farthest_point, p2, p) > 0]

        return hull_part(p1, farthest_point, left_of_line) + [farthest_point] + hull_part(farthest_point, p2, right_of_line)

    min_point = min(points)
    max_point = max(points)

    left_set = [p for p in points if cross_product(min_point, max_point, p) > 0]
    right_set = [p for p in points if cross_product(max_point, min_point, p) > 0]

    return [min_point] + hull_part(min_point, max_point, left_set) + [max_point] + hull_part(max_point, min_point, right_set)


# Gift Wrapping (Jarvis March) Algorithm
def jarvis_march(points: List[Point]) -> List[Point]:
    if len(points) < 3:
        return points

    def orientation(p: Point, q: Point, r: Point) -> int:
        # Returns:
        # 0 if p, q, and r are collinear
        # 1 if clockwise
        # 2 if counterclockwise
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    hull = []

    leftmost = min(points)  # Start from the leftmost point
    p = leftmost
    while True:
        hull.append(p)
        q = points[0]
        for r in points:
            if orientation(p, q, r) == 2:  # counterclockwise turn
                q = r
        p = q
        if p == leftmost:  # When we return to the start point
            break

    return hull


# Graham's Scan Algorithm
def graham_scan(points: List[Point]) -> List[Point]:
    if len(points) < 3:
        return points

    def polar_angle(p0: Point, p1: Point) -> float:
        # Returns the polar angle between p0 and p1
        return math.atan2(p1[1] - p0[1], p1[0] - p0[0])

    def distance(p0: Point, p1: Point) -> float:
        # Returns the squared distance between two points
        return (p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2

    def cross_product(o: Point, a: Point, b: Point) -> int:
        # Cross product to determine counterclockwise or clockwise
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Step 1: Find the point with the lowest y-coordinate, breaking ties by x-coordinate
    start = min(points)

    # Step 2: Sort points by polar angle with respect to the starting point
    sorted_points = sorted(points, key=lambda p: (polar_angle(start, p), distance(start, p)))

    # Step 3: Use a stack to maintain the convex hull
    hull = [sorted_points[0], sorted_points[1]]

    for p in sorted_points[2:]:
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull
