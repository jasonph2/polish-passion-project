import os

def change_file_extension(file_path, new_extension):
    directory, filename_with_extension = os.path.split(file_path)
    filename, _ = os.path.splitext(filename_with_extension)

    new_file_path = os.path.join(directory, f"{filename}.{new_extension}")

    return new_file_path

# def polish_to_english_path(file_path):
#     last_hyphen_index = file_path.rfind("-")

#     if last_hyphen_index != -1:
#         updated_string = file_path[:last_hyphen_index + 1] + "English-" + file_path[last_hyphen_index + 1:]
#         return updated_string
#     else:
#         print("No hyphen found in the string.")
#         return file_path
