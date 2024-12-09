def read_input(file_path):
    with open(file_path, mode='r', newline='\r') as file:
        data = file.read()
    return data