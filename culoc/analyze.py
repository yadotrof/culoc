import os


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def cloc(path):
    if os.path.isfile(path):
        # if path.endswith('.py'):
        with open(path, "rb") as f:
            c_generator = _count_generator(f.raw.read)
            return sum(buffer.count(b"\n") for buffer in c_generator)


def count_lines():
    res = {}
    for root, dirs, files in os.walk(".", topdown=False):
        res[root] = 0
        for file in files:
            new_path = os.path.join(root, file)
            val = cloc(new_path)
            res[new_path] = val
            res[root] += val
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            res[root] += res[dir_path]
    return res


def get_dir_data(data, path):
    current_data = []
    for file in os.listdir(path):
        sub_path = os.path.join(path, file)
        current_data.append((sub_path, data[sub_path]))
    current_data.sort(key=lambda x: x[1], reverse=True)
    return current_data
