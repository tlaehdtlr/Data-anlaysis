from pathlib import Path

"""
directory architecture

main
 - data file config
  - data input
  - parser
   - .py


"""

current_path = Path.cwd()
target_path = Path("../")
print(Path.exists(target_path))
print(Path.is_dir(target_path))
print(Path.is_file(target_path))
print(target_path.resolve())