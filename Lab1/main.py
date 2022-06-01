class ThreadedNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.right_thread = None


def build_threaded_tree(data, parent):

    print(data)
    mid_val = len(data) // 2
    node = ThreadedNode(data[mid_val])

    if mid_val > 0:
        node.left = build_threaded_tree(data[:mid_val], node)
        if len(data) > 2:
            node.right = build_threaded_tree(data[mid_val + 1:], parent)
    else:
        node.right_thread = parent

    return node


def get_list_from_region(root: ThreadedNode, region):
    cur_node = root
    res = []

    while cur_node.left is not None:
        cur_node = cur_node.left

    while cur_node.value[1] < region[0]:
        print(cur_node.value)
        if cur_node.right is not None:
            cur_node = cur_node.right
        elif cur_node.right_thread is not None:
            cur_node = cur_node.right_thread
        else:
            return []

    while cur_node.value[1] < region[1]:
        print(cur_node.value)
        res.append(cur_node.value)
        if cur_node.right is not None:
            cur_node = cur_node.right
        elif cur_node.right_thread is not None:
            cur_node = cur_node.right_thread
        else:
            break

    return res


class RangeNode(object):
    def __init__(self, data, left) -> None:
        self.left_bound = left
        self.right_bound = left + len(data)
        self.left = None
        self.right = None
        self.isLeaf = False
        print(self.left_bound, self.right_bound)
        self.data = build_threaded_tree(unpack_y_range(data), None)


def unpack_y_range(data):
    res = []
    for d in data:
        for y in d[1]:
            res.append([d[0], y])

    return sorted(res, key=lambda x: x[1])


def build_range_tree(data, left):

    node = RangeNode(data, left)
    mid_val = len(data) // 2
    if mid_val > 0:
        node.left = build_range_tree(data[:mid_val], left)
        node.right = build_range_tree(data[mid_val:], left + mid_val)

    return node


def range_search(root: RangeNode, x_range, y_range):

    if root.left_bound >= x_range[1] or root.right_bound <= x_range[0]:
        return []

    if root.right_bound - root.left_bound < 4:
        print(f'seeking {root.left_bound}, {root.right_bound}')
        return get_list_from_region(root.data, y_range)

    res = []
    left_range = range_search(root.left, x_range, y_range)
    if left_range:
        res += left_range
    right_range = range_search(root.right, x_range, y_range)
    if right_range:
        res += right_range

    return res


def inorder(root, level):

    if not root:
        return

    inorder(root.left, level + 1)
    print('\t' * level, root.left_bound, root.right_bound)
    inorder(root.right, level + 1)


def generate_intervals(points):
    intervals = {}
    points = sorted(points, key=lambda x: x[0])

    for p in points:
        if p[0] not in intervals.keys():
            intervals[p[0]] = [p[1]]
        else:
            intervals[p[0]].append(p[1])

    return [[k, v] for k, v in intervals.items()]


def get_intervals_pointers(intervals, x_range):
    x_pointers = []

    flag = False
    for i in range(len(intervals)):
        if intervals[i][0] > x_range[0] and not flag:
            x_pointers.append(i)
            flag = True

        if intervals[i][0] > x_range[1]:
            x_pointers.append(i)
            break

    while len(x_pointers) < 2:
        x_pointers.append(len(intervals))

    return x_pointers


if __name__ == "__main__":
    points = [[0, 8],
            [1, 4],
            [3, 9],
            [4, 5],
            [4, 6],
            [5, 10],
            [6, 6],
            [6, 7],
            [8, 6],
            [9, 2]]

    data = generate_intervals(points)

    root = build_range_tree(data, 0)
    inorder(root, 0)

    x_range = [2, 8.5]
    y_range = [3, 7.5]

    print(range_search(root, get_intervals_pointers(data, x_range), y_range))
