from queue import PriorityQueue

class Task:
    def __init__(self, id, priority, type, point, do, complited_percent, is_complited, max, time):
        self.id = id
        self.priority = priority
        self.type = type
        self.point = point
        self.do = do
        self.complited_percent = complited_percent
        self.is_complited = is_complited
        self.max = max
        self.time = time


# task_info = {
#     "id"
#     "priority"
#     "type"
#     "do" = [],
#     "point"
#     "complited"
#     "max"
# }

# location = {
#     "drone_id" 
#     "point"
# }

# self_location

# task_plane_info {
#     "id"
#     "data"
# }

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

tasks = PriorityQueue()
locations = dict[str, Point]

class Table:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

    def sort_rows_by_second_column(self):
        self.data[1:] = sorted(self.data[1:], key=lambda x: x[1])

    def add_row(self, row_data):
        if len(row_data) != len(self.headers):
            raise ValueError("Number of items in row_data must match the number of headers")
        self.data.append(row_data)

    def remove_row(self, index):
        del self.data[index]

    def get_column(self, index):
        return [row[index] for row in self.data]

    def get_cell_value(self, row_index, col_index):
        return self.data[row_index][col_index]

    def set_cell_value(self, row_index, col_index, value):
        self.data[row_index][col_index] = value

    def print_table(self):
        for row in self.data:
            print("\t".join(str(item) for item in row))

headers = ["task_id", "task_priority", ["id", "current_priority"]] # можно реализовать проще

headers_id = {"id": "index"}

data = [
    ["id", "priority", ["min1.1", "min1.2"]]
]

#       1     2       3
#       7     4       5
# A 5   4,8   10,15
# B 4
# C 2


def add_task(task_info):
    global tasks
    task = Task(task_info["id"], task_info["priority"], task_info["type"], task_info["point"], [], 0, False, task_info["max"])
    tasks.put((task_info["priority"], task))

