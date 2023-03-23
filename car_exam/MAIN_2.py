#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
競賽二的主程式
除了import maze的地方改成maze_1，其餘都跟Checkpoint資料夾中的MAIN相同
"""
from node import * # (from test.py)
import maze as mz # (from test.py)
from BT import * # (from both)
import score # (from BT_cmd.py)
import time

maze_path = "data/maze_exam.csv" # (from test.py)
maze = mz.Maze(maze_path)
def main(nf,nt): # (from test.py)
    nd_from = nf
    nd_to = nt
    path = maze.shortestPath(nd_from, nd_to) # 起點終點 -> 路徑

    print('From %s to %s: %s' % (nd_from, nd_to, path))
    
    mazedir = maze.direction(path) # 路徑 -> 指令串
    print(mazedir)
    return mazedir

def read(): # (from test.py)
    while True:
        if bt.waiting():
            msg = str(bt.readString())
            print(msg)
            return(msg)

# bt commands: (from BT_cmd.py)
msgcheck = \
{'nodeReach': "done", \
 'moveDone': "done", \
 'RFIDdet': "RFID Detected: "}

uid = "" # the uid just got (from BT_cmd.py)
scoreboard = score.Scoreboard("data/UID_game2.csv") # scoreboard (from BT_cmd.py)

# bluetooth initializing (from both)
bt = bluetooth(portname)
while not bt.is_open(): pass
print("BT Connected!")


if __name__=='__main__':
    state = 0 # 我不想疊太多層
    while True:
        if state == 0:
            # (from test.py)
            # 初始模式，由"T"啟動下一個模式
            # Python發遙控指令，車子收指令
            msgWrite = input()
            if msgWrite == "T": # 接收到T之後開始走迷宮
                print("Start") # by myself
                state = 1
        
        elif state == 1:
            # (from test.py)
            # 循跡模式
            # Python接收訊息，車子抵達node後發送訊息
            
            # 這裏起點終點該怎麼給？我只能暫時照抄test.py的過來
            end_list = maze.findend()
            print('最短路徑:',end_list)
            start_pt = 1
            for pt in end_list:
                nd_from = int(start_pt) # 要改掉
                nd_to = int(pt)   # 要改掉
                action = main(nd_from,nd_to)    # 產生指令串
                bt.write('T')   # 開始循跡
                print('Tracing')
                
                for num_act in range(len(action)-1): # 指令串按次發送 
                    while True: 
                        
                        if read() =='done': # 抵達node
                            print("Reached a node.") # (from BT_cmd.py)
                            
                            # (from test.py)
                            # 一個口令一個動作模式（誤
                            # Python給車子指令
                            msgWrite = str(action[num_act+1])
                            bt.write(msgWrite) 
                            print('第{}個動作:'.format(num_act+1))
                            print('動作:',msgWrite)
                            
                            while True:
                                if read() =='done':
                                    bt.write('T')
                                    print('Tracing2')
                                    break
                            break
                while True: # 走到終點的時候會跑到這裡來
                    if read() =='done': # 完成動作，成功抵達
                        bt.write('F')
                        # (from BT_cmd.py)
                        # 讀RFID模式
                        # Python 等車子傳rfid
                        t = time.time()
                        while time.time() - t < 1:
                            msg = read()
                            if msg[:15] == msgcheck['RFIDdet']: # 收到RFID.    
                                print("A UID is found.")
                                uid = msg[15:]
                                print(f"UID: {uid}")
                                print("Checking...")
                                scoreboard.add_UID(uid)
                                break
                        bt.write('V')
                        while True :
                           if read() =='done':
                               break
                        break
                print('jump')
                start_pt = pt
            state = 0
            msgWrite = 'V'
                    
                    
        bt.write(msgWrite)
        
            
