import json, os
import collections

# Get user name
profileInfo = os.path.join("unzipped3", "profile_information", "profile_information.json")
with open(profileInfo, 'r') as file:
    mainUser = json.load(file)["profile_v2"]["name"]["full_name"]

print(f"Main User is {mainUser}")

# Workdir
inboxDir = os.path.join("unzipped3", "messages", "inbox")

# Load threadsInfo from temp
with open(os.path.join("temp", "threadsInfo.json"), 'r') as file:
    threadsInfo = json.load(file)

# Iterate through each DM thread folder
parsedData = {}
messageTypes = []
for i, threadInfo in enumerate(threadsInfo["direct"]):
    threadDir = threadInfo["dir"]
    threadTitle = threadInfo["title"]
    print(f"\t[{i}/{len(threadsInfo['direct'])}] {threadTitle}")

    parsedData[threadTitle] = {
        "sentTimestamps": [],
        "receivedTimestamps": []
    }

    for messageFile in threadInfo["messageFiles"]:
        # Read file
        with open(os.path.join(inboxDir, threadDir, messageFile), "r") as file:
            data = json.load(file)

        # Iterate through each message and add
        for msg in data["messages"]:
            messageTypes += [msg["type"]]

            if msg["type"] not in ["Call", "Unsubscribe"]:
                if msg["sender_name"] == mainUser:
                    parsedData[threadTitle]["sentTimestamps"] += [msg["timestamp_ms"]]
                else:
                    parsedData[threadTitle]["receivedTimestamps"] += [msg["timestamp_ms"]]

        parsedData[threadTitle]["sentTotal"] = len(parsedData[threadTitle]["sentTimestamps"])
        parsedData[threadTitle]["receivedTotal"] = len(parsedData[threadTitle]["receivedTimestamps"])


with open(os.path.join("temp", "DMsInfo.json"), "w") as file:
    json.dump(parsedData, file, indent=2)

print(collections.Counter(messageTypes))
