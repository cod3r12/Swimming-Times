import PyPDF2

def getEvent (line):
    """Gets the event from a line of times"""
    reversedLine = line[::-1].split(" ")
    while reversedLine.count("*") > 0:
        reversedLine.remove("*")
    dist = reversedLine[2][::-1] + " "
    unit = reversedLine[1][::-1] + " "
    stroke = reversedLine[0][::-1]
    event = dist + unit + stroke
    return event.lower()

def mmssToSeconds (time):
    timesList = time.split(":")
    timesList.append(timesList[1].split(".")[1])
    timesList[1] = timesList[1].split(".")[0]
    timeInSeconds = (int(timesList[0]) * 60) + int(timesList[1]) + (int(timesList[2]) / 100)
    return timeInSeconds

# Opening and Reading PDF
timesPDF = open("swimmingTimes.pdf", "rb")
pdfReader = PyPDF2.PdfReader(timesPDF)

# Converting each line of each page into lists
page1 = pdfReader.pages[0].extract_text().split("\n")
page2 = pdfReader.pages[1].extract_text().split("\n")
page3 = pdfReader.pages[2].extract_text().split("\n")
page4 = pdfReader.pages[3].extract_text().split("\n")
page5 = pdfReader.pages[4].extract_text().split("\n")
page6 = pdfReader.pages[5].extract_text().split("\n")

# Getting prompts
poolLength = input("What pool length? ").lower()
event = input("What event? ").lower()
ageGroup = input("What age group? ").lower()
gender = input("Boys or Girls? ").lower()
userTime = input("What is your time? ").lower()

# Getting Age Group Start Indexes (where the times start for each age group)
if poolLength == "long course meters" or poolLength == "lcm":
    ageGroupStartPage = 1
    ageGroupStartIndex = 0
    ageGroupStartIndexFound = False
    if ageGroup == "10 & under":
        ageGroupStartIndexFound = True
    else:
        for line in page1:
            if line.split(" ").count(ageGroup) > 0:
                ageGroupStartIndexFound = True
                break
            ageGroupStartIndex += 1
    if not ageGroupStartIndexFound:
        ageGroupStartPage = 2
        ageGroupStartIndex = 0
        for line in page2:
            if line.split(" ").count(ageGroup) > 0:
                ageGroupStartIndexFound = True
                break
            ageGroupStartIndex += 1
elif poolLength == "short course meters" or poolLength == "scm":
    ageGroupStartPage = 3
    ageGroupStartIndex = 0
    ageGroupStartIndexFound = False
    if ageGroup == "10 & under":
        ageGroupStartIndex = 2
        ageGroupStartIndexFound = True
    else:
        for line in page3:
            if line.split(" ").count(ageGroup) > 0:
                ageGroupStartIndexFound = True
                break
            ageGroupStartIndex += 1
    if not ageGroupStartIndexFound:
        ageGroupStartPage = 4
        ageGroupStartIndex = 0
        for line in page4:
            if line.split(" ").count(ageGroup) > 0:
                ageGroupStartIndexFound = True
                break
            ageGroupStartIndex += 1
elif poolLength == "short course yards" or poolLength == "scy":
    ageGroupStartPage = 5
    ageGroupStartIndex = 0
    ageGroupStartIndexFound = False
    if ageGroup == "10 & under":
        ageGroupStartIndex = 2
        ageGroupStartIndexFound = True
    else:
        for line in page5:
            if line.split(" ").count(ageGroup) > 0:
                ageGroupStartIndexFound = True
                break
            ageGroupStartIndex += 1
    if not ageGroupStartIndexFound:
        ageGroupStartPage = 6
        ageGroupStartIndex = 0
        for line in page6:
            if line.split(" ").count(ageGroup) > 0:
                ageGroupStartIndexFound = True
                break
            ageGroupStartIndex += 1

# Getting Line of Times from Event
eventTimesLine = ""
if ageGroupStartPage == 1:
    eventLineCounter = 1
    while True:
        if getEvent(page1[ageGroupStartIndex + eventLineCounter]) == event:
            eventTimesLine = page1[ageGroupStartIndex + eventLineCounter]
            break
        eventLineCounter += 1
elif ageGroupStartPage == 2:
    eventLineCounter = 1
    while True:
        if getEvent(page2[ageGroupStartIndex + eventLineCounter]) == event:
            eventTimesLine = page2[ageGroupStartIndex + eventLineCounter]
            break
        eventLineCounter += 1
elif ageGroupStartPage == 3:
    eventLineCounter = 1
    while True:
        if getEvent(page3[ageGroupStartIndex + eventLineCounter]) == event:
            eventTimesLine = page3[ageGroupStartIndex + eventLineCounter]
            break
        eventLineCounter += 1
elif ageGroupStartPage == 4:
    eventLineCounter = 1
    while True:
        if getEvent(page4[ageGroupStartIndex + eventLineCounter]) == event:
            eventTimesLine = page4[ageGroupStartIndex + eventLineCounter]
            break
        eventLineCounter += 1
elif ageGroupStartPage == 5:
    eventLineCounter = 1
    while True:
        if getEvent(page5[ageGroupStartIndex + eventLineCounter]) == event:
            eventTimesLine = page5[ageGroupStartIndex + eventLineCounter]
            break
        eventLineCounter += 1
elif ageGroupStartPage == 6:
    eventLineCounter = 1
    while True:
        if getEvent(page6[ageGroupStartIndex + eventLineCounter]) == event:
            eventTimesLine = page6[ageGroupStartIndex + eventLineCounter]
            break
        eventLineCounter += 1

# Interpreting Times from Line
# Format Girls B BB A AA AAA AAAA - Boys B BB A AA AAA AAAA
eventTimesLineList = eventTimesLine.split(" ")
timeRankingOrder = ["B", "BB", "A", "AA", "AAA", "AAAA"]
# Taking off event name
for i in range(0, 3):
    eventTimesLineList.pop(len(eventTimesLineList)-1)
if gender == "boys" or gender == "b":
    for i in range(0, 6):
        eventTimesLineList.pop(0)
    eventTimesLineList = eventTimesLineList[::-1]
elif gender == "girls" or gender == "g":
    for i in range(0, 6):
        eventTimesLineList.pop(len(eventTimesLineList)-1)
# List Time Rankings By Gender
print("Time Rankings:")
timeCounter = 0
for time in eventTimesLineList:
    print(timeRankingOrder[timeCounter] + ": " + time)
    timeCounter += 1
# Convert User's Time to Seconds
userTimeInSeconds = mmssToSeconds(userTime)
# Determine Timing Rank of User Time
timeCounter = 0
for time in eventTimesLineList[::-1]:
    if mmssToSeconds(time) > userTimeInSeconds:
        break
    timeToBreak = mmssToSeconds(time)
    timeCounter += 1

if timeCounter == 6:
    print("Your time is slower than a B time. You have " + str(round((userTimeInSeconds - timeToBreak)*100)/100) + " seconds to shave of to get a B time.")
elif timeRankingOrder[::-1][timeCounter] != "AAAA":
    print("You have a " + timeRankingOrder[::-1][timeCounter] + " time. You have " + str(round((userTimeInSeconds - timeToBreak)*100)/100) + " seconds to shave off to get a " + timeRankingOrder[::-1][timeCounter-1] + " time.")
else:
    print("You have an AAAA time! Fantastic!")

timesPDF.close
