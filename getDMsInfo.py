import json, os
import collections

# Get user name
profileInfo = os.path.join("unzipped3", "profile_information", "profile_information.json")
with open(profileInfo, 'r') as file:
    mainUser = json.load(file)["profile_v2"]["name"]["full_name"]

print(f"[getDMsInfo] Main User is {mainUser}")

# Workdir
inboxDir = os.path.join("unzipped3", "messages", "inbox")

# Load threadsInfo from temp
with open(os.path.join("temp", "threadsInfo.json"), 'r') as file:
    threadsInfo = json.load(file)

# Iterate through each DM thread folder
parsedData = {}
dashInfo = {
    "totalSent": 0,
    "totalReceived": 0,
    "firstSentMessage": {},
    "firstReceivedMessage": {}
}
messageTypes = []
firstTimestampSent = 1e20
firstTimestampReceived = 1e20
for i, threadInfo in enumerate(threadsInfo["direct"]):
    threadDir = threadInfo["dir"]
    threadTitle = threadInfo["title"]
    print(f"\t[{i+1}/{len(threadsInfo['direct'])}] {threadTitle}")

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

                    if msg['timestamp_ms'] < firstTimestampSent:
                        dashInfo["secondSentMessage"] = dashInfo["firstSentMessage"]
                        msg['recipient_name'] = threadTitle
                        dashInfo["firstSentMessage"] = msg
                        firstTimestampSent = msg['timestamp_ms']
                else:
                    parsedData[threadTitle]["receivedTimestamps"] += [msg["timestamp_ms"]]

                    if msg['timestamp_ms'] < firstTimestampReceived:
                        dashInfo["secondReceivedMessage"] = dashInfo["firstReceivedMessage"]
                        dashInfo["firstReceivedMessage"] = msg
                        firstTimestampReceived = msg['timestamp_ms']

        sent = len(parsedData[threadTitle]["sentTimestamps"])
        received = len(parsedData[threadTitle]["receivedTimestamps"])

        parsedData[threadTitle]["sentTotal"] = sent
        parsedData[threadTitle]["receivedTotal"] = received

        dashInfo["totalSent"] += sent
        dashInfo["totalReceived"] += received

print(f"[getDMsInfo] Saving to files")
with open(os.path.join("temp", "dashInfo.json"), 'w') as file:
    json.dump(dashInfo, file, indent=2)

with open(os.path.join("temp", "DMsInfo.json"), "w") as file:
    json.dump(parsedData, file)

print(collections.Counter(messageTypes))
