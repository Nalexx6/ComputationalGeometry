import numpy as np

class Delaunay:
    def __init__(self, points):
        max_cor = 0

        for p in points:
            if max_cor < abs(p[0]):
                max_cor = abs(p[0])
            if max_cor < abs(p[1]):
                max_cor = abs(p[1])

        max_cor += 1
        self.points = [max_cor*np.array((-1, -1)),
                       max_cor*np.array((+1, -1)),
                       max_cor*np.array((+1, +1)),
                       max_cor*np.array((-1, +1))]

        for p in points:
            self.points.append(p)

        # Two dicts to store triangle neighbours and circumcircles.
        self.triangles = {}
        self.circles = {}

        # Create two CCW triangles for the frame
        T1 = (0, 1, 3)
        T2 = (2, 3, 1)
        self.triangles[T1] = [T2, None, None]
        self.triangles[T2] = [T1, None, None]

        # Compute circumcenters and circumradius for each triangle
        for t in self.triangles:
            self.circles[t] = self.circumcenter(t)

        # Add all points to triangulation
        for index in range(4, len(self.points)):
            self.add_point(self.points[index], index)

        self.triangulation = [(a - 4, b - 4, c - 4) for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]

    def circumcenter(self, tri):
        pts = np.asarray([self.points[v] for v in tri])

        pts2 = np.dot(pts, pts.T)
        A = np.bmat([[2 * pts2, [[1],
                                 [1],
                                 [1]]],
                      [[[1, 1, 1, 0]]]])

        b = np.hstack((np.sum(pts * pts, axis=1), [1]))
        x = np.linalg.solve(A, b)
        bary_coords = x[:-1]
        center = np.dot(bary_coords, pts)

        radius = np.sum(np.square(pts[0] - center))
        return center, radius

    def in_circle(self, tri, p):
        center, radius = self.circles[tri]
        return np.sum(np.square(center - p)) <= radius

    def add_point(self, p, index):
        # Search the triangle(s) whose circumcircle contains p
        bad_triangles = []
        for t in self.triangles:
            if self.in_circle(t, p):
                bad_triangles.append(t)

        # Find the CCW boundary (star shape) of the bad triangles,
        # expressed as a list of edges (point pairs) and the opposite
        # triangle to each edge.
        boundary = []
        # Choose a "random" triangle and edge
        t = bad_triangles[0]
        edge = 0
        # get the opposite triangle of this edge
        while True:
            # Check if edge of triangle T is on the boundary...
            # if opposite triangle of this edge is external to the list
            tri_op = self.triangles[t][edge]
            if tri_op not in bad_triangles:
                # Insert edge and external triangle into boundary list
                boundary.append((t[(edge + 1) % 3], t[(edge - 1) % 3], tri_op))

                # Move to next CCW edge in this triangle
                edge = (edge + 1) % 3

                # Check if boundary is a closed loop
                if boundary[0][0] == boundary[-1][1]:
                    break
            else:
                # Move to next CCW edge in opposite triangle
                edge = (self.triangles[tri_op].index(t) + 1) % 3
                t = tri_op

        # print(self.triangles)
        # print(bad_triangles)
        # Remove triangles too near of point p of our solution
        for t in bad_triangles:
            self.triangles.pop(t, None)
            self.circles.pop(t, None)

        # Retriangle the hole left by bad_triangles
        new_triangles = []
        for (e0, e1, tri_op) in boundary:
            # Create a new triangle using point p and edge extremes
            t = (index, e0, e1)

            # Store circumcenter and circumradius of the triangle
            self.circles[t] = self.circumcenter(t)

            # Set opposite triangle of the edge as neighbour of t
            self.triangles[t] = [tri_op, None, None]

            # Try to set T as neighbour of the opposite triangle
            if tri_op:
                # search the neighbour of tri_op that use edge (e1, e0)
                for i, neigh in enumerate(self.triangles[tri_op]):
                    if neigh:
                        if e1 in neigh and e0 in neigh:
                            # change link to use our new triangle
                            self.triangles[tri_op][i] = t

            # Add triangle to a temporal list
            new_triangles.append(t)

        # Link the new triangles each another
        for i, t in enumerate(new_triangles):
            self.triangles[t][1] = new_triangles[(i + 1) % len(new_triangles)]   # next
            self.triangles[t][2] = new_triangles[(i - 1) % len(new_triangles)]   # previous
