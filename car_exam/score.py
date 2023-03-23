import pandas
import numpy as np
import requests

# ================================================================
# Scoreboard
#   add_UID(UID_str)
#     UID_str : UID string ("0x" excluded)
#   getCurrentScore()
#     return current score (int)
# ================================================================

class Scoreboard:
    def __init__(self, filepath):
        raw_data = np.array(pandas.read_csv(filepath))#.values
        self.cardList = [int(a, 16) for a in raw_data.T[0]]
        self.visitList = list()
        self.totalScore = 0
        self.cardValue = dict()
        self.ip = "114.34.123.174:5000"
        ## Here to set group name!!!
        self.team_name = "一早一組"
        self.url_start = 'http://' + self.ip + '/{}/start/'.format(self.team_name)

        for i in range(len(raw_data)):
            self.cardValue[self.cardList[i]] = raw_data[i][1]


        ##################################
        ## Http request !! Start Juding ##
        ##################################
        try:
            print("####### Start Judging !!")
            r = requests.get(self.url_start)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            sys.exit(1)



    def add_UID(self, UID_str):
        UID = int(UID_str,16)

        if UID not in self.cardList:
            print("This UID doesn't exist in the UID list file:", UID)
        elif UID in self.visitList:
        	print("This UID is already visited:", UID)
        else:
            point = self.cardValue[UID]
            self.totalScore += point
            print("A treasure is found! You got " + str(point) + " points.")
            print("Current score: "+ str(self.totalScore))
            print("")
            self.visitList.append(UID)


            ##################################
            ## Http request !! Adding Score ##
            ##################################
            try:
                print("####### Valid UID !! Adding Score !!")
                url = 'http://' + self.ip + '/{}/{}/'.format(
                    self.team_name, self.totalScore)
                r = requests.get(url)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print(e)



    def getCurrentScore(self):
        return int(self.totalScore)
