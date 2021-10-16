import os
import shutil

d = "unzipped3/messages/archived_threads"

ds = ["photos", "videos", "gifs", "files", "audio"]
for i in os.listdir(d):
    print(i)

    ps = [os.path.join(d, i, j) for j in ds]
    for p in ps:
        if os.path.isdir(p):
            shutil.rmtree(p)
            print("   " + str(p))