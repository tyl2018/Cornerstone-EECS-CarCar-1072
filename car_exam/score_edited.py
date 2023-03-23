"""這個版本有附加我加的註解。除了註解和if __name__ == "__main__"沒改別的。by廖"""

import pandas
import numpy as np 

# ================================================================
# Scoreboard
#   add_UID(UID_str)
#     UID_str : UID string ("0x" excluded)
#   getCurrentScore()
#     return current score (int)
# ================================================================

class Scoreboard:
    def __init__(self, filepath): # 令Scoreboard的時候括號裡就要餵一個csv檔的path
        raw_data = np.array(pandas.read_csv(filepath))#.values
        
        self.cardList = [int(a, 16) for a in raw_data.T[0]] # 所有rfid的資料，存在csv檔的第0行
        self.visitList = list() # 經過的rfid
        self.totalScore = 0     # 總分
        self.cardValue = dict() # 把cardList對應分數弄成一個dict

        for i in range(len(raw_data)):
            self.cardValue[self.cardList[i]] = raw_data[i][1]

        print ("Successfully read the UID file!")

    def add_UID(self, UID_str): # 呼叫這個函式的時候輸入獨到的UID，資料型態是str，16進位格式。呼叫之後它會幫你記錄分數，沒有輸出。
        UID = int(UID_str,16) # UID從這邊開始會以十進位顯示，所以跟主程print出來的UID看起來不一樣是正常的。

        if UID not in self.cardList: # 偵測到的UID不在讀取的檔案內
            print("This UID doesn't exist in the UID list file:", UID)
        elif UID in self.visitList: # 偵測到的UID已經走過了
            print("This UID is already visited:", UID)
        else: # 讀到新的UID -> 加分嘍！
            point = self.cardValue[UID]
            self.totalScore += point
            print("A treasure is found! You got " + str(point) + " points.")
            print("Current score: "+ str(self.totalScore))
            print("")
            self.visitList.append(UID)

    def getCurrentScore(self):
        return int(self.totalScore)

if __name__ == "__main__":
    # let the scoreboard get the following UID in order:
    # 84EAB017 -> FFFFFFFF-> 50335F7E -> 353D0AD6 -> 84EAB017
    # The result should be: get 1 pt -> doesn't exist -> get 2 pt -> get 3 pt -> already visited
    s = Scoreboard("data/UID.csv")
    car_path = ["84EAB017", "FFFFFFFF", "50335F7E", "353D0AD6", "84EAB017"]
    for u in car_path:
        msg = "RFID Detected: " + u
        if msg[:15] == "RFID Detected: ": # 收到RFID
            print("A UID is found.")
        uid = msg[15:]
        print(f"UID: {uid}")
        print("Checking...")
        s.add_UID(uid)
        