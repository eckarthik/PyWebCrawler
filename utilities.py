import os

def create_directory(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)

def create_files(project_name,file_name,data):
    path = os.path.join(project_name,file_name)
    if not os.path.isfile(path):
        write_to_file(project_name,file_name,data)

def write_to_file(project_name,file_name,data):
    path = os.path.join(project_name,file_name)
    f = open(path,"w")
    f.write(data+"\n")
    f.close()

def append_to_file(path,data):
    f = open(path,'a')
    f.write(data+"\n")
    f.close()

def file_to_set(project_name,file_name):
    path = os.path.join(project_name,file_name)
    results = set()
    with open(path, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(data,project_name,file_name):
    contents = ""
    path = os.path.join(project_name,file_name)
    with open(path,"w") as f:
        for l in sorted(data):
            try:
                f.write(l+"\n")
            except UnicodeEncodeError as e:
                print("Skipping link due to UnicodeEncodeError - ",str(e))
