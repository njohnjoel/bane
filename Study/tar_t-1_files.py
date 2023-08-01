import os
import tarfile
import datetime

# Set the path to the directory containing the files you want to compress
dir_path = "/path/to/directory"

# Get the current year and the previous year
current_year = datetime.datetime.now().year
previous_year = current_year - 1

# Create the name for the tar archive
tar_name = f"previous_year_{previous_year}.tar.gz"

# Create a list of files from the previous year
previous_year_files = []
for filename in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, filename)):
        file_year = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(dir_path, filename))).year
        if file_year == previous_year:
            previous_year_files.append(os.path.join(dir_path, filename))

# Create the tar archive
with tarfile.open(tar_name, "w:gz") as tar:
    for file in previous_year_files:
        tar.add(file)

print(f"Compressed {len(previous_year_files)} files from {previous_year} into {tar_name}")