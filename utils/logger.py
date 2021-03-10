import datetime

def logWarning(WarningMessage):
    print("[{0}][WARNING] {1}".format(datetime.datetime.now(), WarningMessage))

    appendToFile("[WARNING] {0}".format(datetime.datetime.now()))
    return

def logError(ErrorMessage):
    print("[{0}][ERROR] {1}".format(datetime.datetime.now(), ErrorMessage))

    appendToFile("[ERROR] {0}".format(datetime.datetime.now()))
    return

def logAction(action):
    print("[{0}][LOG] {1}".format(datetime.datetime.now(), action))
    return

def appendToFile(ErrorMessage):
    with open("log.txt", "r+") as f:
        existingData = f.readlines()
        existingData.append("[{0}] {1}".format(datetime.datetime.now(), ErrorMessage))
        f.writelines(existingData)
    pass