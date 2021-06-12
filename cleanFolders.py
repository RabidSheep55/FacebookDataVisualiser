import os
from os.path import join as join_path

workDir = join_path("unzipped3")

# Clean out all the empty folders
count = 0
for folder in os.listdir(workDir):
    curDir = join_path(workDir, folder)
    if os.path.exists(join_path(curDir, 'no-data.txt')):
        os.remove(join_path(curDir, 'no-data.txt'))
        os.rmdir(curDir)
        count += 1

print(f"[cleanFolders] Cleanded {count} empty folders")
