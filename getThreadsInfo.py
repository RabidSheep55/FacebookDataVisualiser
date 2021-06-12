import os, json, glob
from time import time

# Workdir
inboxDir = os.path.join("unzipped3", "messages", "inbox")

# The inbox folder contains folders each with the name <chat name>_<some facebook ID>
threadDirs = os.listdir(inboxDir)
print(f"[messages] found {len(threadDirs)} potential threads")

##### Find out which threads are groups, and which are DMs
threadsInfo = {
    "group": [],
    "direct": [],
    "empty": []
}

s = time()
for i, threadDir in enumerate(threadDirs):
    # print(f"\t [{i}/{len(threadDirs)}] {threadDir}")
    with open(os.path.join(inboxDir, threadDir, "message_1.json"), 'r') as file:
        data = json.load(file)

    info = {
        "dir": threadDir,
        "messageFiles": [p.split('\\')[-1] for p in glob.glob(os.path.join(inboxDir, threadDir, "*.json"))]
    }

    if len(info["messageFiles"]) > 1:
        print(f"\t {threadDir.split('_')[0]} has more than 1 message file ({len(info['messageFiles'])})")

    if len(data["messages"]) <= 1:
        threadsInfo["empty"] += [info]
    elif len(data["participants"]) > 2:
        threadsInfo["group"] += [info]
    else:
        threadsInfo["direct"] += [info]

e = time()

# 'Cache'
with open(os.path.join("temp", "threadsInfo.json"), "w") as file:
    json.dump(threadsInfo, file, indent=2)

print(f"[messages] Found: \n\t├── {len(threadsInfo['group'])} groups \n\t├── {len(threadsInfo['direct'])} DMs \n\t└── {len(threadsInfo['empty'])} empty")
print(f"[messages] time taken: {e - s}")
