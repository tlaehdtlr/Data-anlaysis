from pathlib import Path
import os

# p_dir = Path('../edf_data')


# p_sub_dir_file = p_dir.joinpath('edf_input', '1234_20220127_182356_EC.edf')
# print(p_sub_dir_file)
# print(p_sub_dir_file.is_file())


# ## convert to absolute path , return Path class
# print(p_dir.resolve())

# ## convert to relative path
# p_abs_path = Path("D:\\Data-anlaysis\\raw_data_visualization")
# print(p_abs_path.resolve().relative_to(Path.cwd()))


current_path = Path.cwd()
target_path = Path("../")
print(Path.exists(target_path))
print(Path.is_dir(target_path))
print(Path.is_file(target_path))
print(target_path.resolve())

if __name__ == __


"""

# input_data_path = Path(r'D:\Data-anlaysis\raw_data_visualization\edf_data\edf_input')
input_data_path = Path('../edf_input')
print(input_data_path)
file_name = '\1234_20220127_182356_EC.edf'

file_path = os.path.abspath(os.path.join(input_data_path, file_name))
file = open(os.path.dirname(file_path), 'rb')
print(file)
file.close()
"""