
from node import *
import maze as mz
from BT import * 

maze_path = "data/maze_1.csv"
maze = mz.Maze(maze_path)

def main(nf,nt): # 改寫自main.py，並將起點終點從亂數表產生改為輸入參數，回傳動作指令str
    
    nd_from = nf
    nd_to = nt
    path = maze.shortestPath(nd_from, nd_to) # 起點終點 -> 路徑

    print('From %s to %s: %s' % (nd_from, nd_to, path))
    
    mazedir = maze.direction(path) # 路徑 -> 指令串
    print(mazedir)
    return mazedir

'''
def waiting():
    print(read())
    if read() == 'done':
        print('done')
        return True
    else:
        return False
'''

def read(): # BT的函式抓到這裡來了
    while True:
        if bt.waiting():
            msg = str(bt.readString())
            print(msg)
            return(msg)
    
if __name__=='__main__':
    bt = bluetooth(portname)
    while not bt.is_open(): pass
    print("BT Connected!")

    while True:
        msgWrite = input()
        if msgWrite == "T": # 接收到T之後開始走迷宮
            end_list = maze.findend()
            print(end_list)
            start_pt = 1
            for pt in end_list:
                nd_from = int(start_pt)
                nd_to = int(pt)
                action = main(nd_from,nd_to) # 指令串
                bt.write('T')   # 開始循跡
                print('Tracing')
                # 我其實看不懂下面這邊，用range(1, len(action))不好嗎
                for num_act in range(len(action)-1): # 反正簡單講這個loop就是：送一個指令，送一個T，送下一個指令...etc.
                    while True: # 收到'done'訊息之前卡在這裡面
                        #print('hi') ＃？？？
                        if read() =='done': # 抵達node
                            msgWrite = action[num_act+1]
                            bt.write(msgWrite)  
                            print(num_act+1)
                            print(msgWrite)
                            while True:
                                if read() =='done':
                                    bt.write('T')
                                    print('Tracing2')
                                    break
                            break
                while True: # 走到終點的時候會跑到這裡來
                    if read() =='done': # 完成動作後原地回轉，
                        bt.write('V')
                        while True :
                           if read() =='done':
                               break
                        break
                print('jump')
                start_pt = pt
            
            msgWrite = 'V'
                
        bt.write(msgWrite) # 這句怎麼不在68-70行的if內

