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
    "mainUser": mainUser,
    "totalSent": 0,
    "totalReceived": 0,
    "firstMessages": [0 for i in range(30)]
}
simpleMessagesChart = {}
messageTypes = []
firstTimestamp = 1e20
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
                if msg['timestamp_ms'] < firstTimestamp:
                    dashInfo["firstMessages"].pop()     # Pop last message
                    msg['recipient_name'] = threadTitle if msg["sender_name"] == mainUser else mainUser
                    dashInfo["firstMessages"].insert(0, msg)
                    firstTimestamp = msg['timestamp_ms']

                if msg["sender_name"] == mainUser:
                    parsedData[threadTitle]["sentTimestamps"] += [msg["timestamp_ms"]]

                else:
                    parsedData[threadTitle]["receivedTimestamps"] += [msg["timestamp_ms"]]


        sent = len(parsedData[threadTitle]["sentTimestamps"])
        received = len(parsedData[threadTitle]["receivedTimestamps"])

        parsedData[threadTitle]["sentTotal"] = sent
        parsedData[threadTitle]["receivedTotal"] = received

        dashInfo["totalSent"] += sent
        dashInfo["totalReceived"] += received

        simpleMessagesChart[threadTitle] = {
            "sent": sent,
            "received": received
        }

dashInfo["simpleMessageSeries"] = sorted([(t, simpleMessagesChart[t]['sent'], simpleMessagesChart[t]['received']) for t in simpleMessagesChart.keys()], key=lambda x: x[1]+x[2], reverse=True)[:5]

print(f"[getDMsInfo] Saving to files")
with open(os.path.join("temp", "dashInfo.json"), 'w') as file:
    json.dump(dashInfo, file, indent=2)

with open(os.path.join("temp", "DMsInfo.json"), "w") as file:
    json.dump(parsedData, file)

print(collections.Counter(messageTypes))
