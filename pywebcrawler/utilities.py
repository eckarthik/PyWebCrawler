import os, requests, csv, shutil


def create_directory(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)


def create_files(project_name, file_name, data):
    path = os.path.join(project_name, file_name)
    if not os.path.isfile(path):
        write_to_file(project_name, file_name, data)


def create_csv_file(project_name, file_name, header_row):
    path = os.path.join(project_name, file_name)
    if not os.path.isfile(path):
        with open(file_name, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header_row)


def write_to_file(project_name, file_name, data):
    path = os.path.join(project_name, file_name)
    f = open(path, "w")
    f.write(data + "\n")
    f.close()


def append_to_file(project_name, file_name, data):
    path = os.path.join(project_name, file_name)
    f = open(path, 'a')
    f.write(data + "\n")
    f.close()


def file_to_set(project_name, file_name):
    path = os.path.join(project_name, file_name)
    results = set()
    with open(path, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def set_to_file(data, project_name, file_name):
    contents = ""
    path = os.path.join(project_name, file_name)
    with open(path, "w") as f:
        for l in sorted(data):
            try:
                f.write(l + "\n")
            except UnicodeEncodeError as e:
                print("Skipping link due to UnicodeEncodeError - ", str(e))


def append_to_csv(project_name, file_name, data):
    path = os.path.join(project_name, file_name)
    with open(path, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)

def check_proxy(proxy):
    try:
        requests.get("http://google.com", proxies={proxy.split(":")[0]: proxy.split(":")[1]})
    except Exception as e:
        return False
    return True

def check_project_directory_exists(project_name):
    return os.path.exists(project_name)

def delete_project(project_name):
    shutil.rmtree(project_name)