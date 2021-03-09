import json, subprocess
import utils.replayHandler as replayHandler
from discordBot import runBot
import utils.sqlManager
import requests

#replayHandler.processReplays(["Replays/g1.replay", "Replays/g2.replay", "Replays/g3.replay"])

if __name__ == "__main__":
    runBot()
