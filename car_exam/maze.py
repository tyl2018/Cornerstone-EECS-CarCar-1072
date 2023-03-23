import node
import math
import csv
import pandas

class Maze:
    def __init__(self, filepath):
        """
        read file and build graph
        """
        # data read from csv
        self.raw_data = pandas.read_csv(filepath).values
        # graph if saved here
        self.nd_dict = dict()
        self.nd_dict2 = dict()

        # process raw_data
        for dt in self.raw_data:
            nd = node.Node(dt[0])
            nd2 = node.Node(dt[0])
            for i in range(1,5):
                if not math.isnan(dt[i]):
                    nd.setSuccessor(int(dt[i]))
                    nd2.setSuccessor_2(int(dt[i]))
                if math.isnan(dt[i]):
                    nd2.setSuccessor_2(0)

            self.nd_dict[dt[0]] = nd
            self.nd_dict2[dt[0]] = nd2
    def print(self):
        print(self.nd_dict)
        for i in range(1, len(self.nd_dict)+1):
            print(i, [ nd[0] for nd in self.nd_dict[i].getSuccessors() ])

    
    def shortestPath(self, nd_from, nd_to):
        
        """ 
        return a path (sequence of nodes) from the current node to the nearest unexplored deadend 
        e.g.
            1 -- 2 -- 3     
                 |    |  ->  shortestPath(1,4) returns [1,2,4]
                 4 -- 5
        """
        explored = []
        exp = []
        path = []
        explored.append(nd_from)
        exp.append(nd_from)
        path.append(nd_to)

        distance = {str(nd_from):0}
        step = {}

        a = nd_to
        
        while explored != []:
            for i in self.nd_dict[explored[0]].getSuccessors():
                if explored[0] == nd_to:
                    break
                if not i in exp:
                    explored.append(i)
                    exp.append(i)
                    distance[str(i)] = distance[str(explored[0])]+1
                    step[str(i)] = explored[0]
            explored.pop(0)
        while True:
            if a == nd_from:
                return path[::-1]
            else:
                a = step[str(a)]
                path.append(a)

    def direction(self,ans):
        i = 0
        dir_list = []
        for node in ans[:-1]:
            i += 1
            #print(self.nd_dict2[node].Successors)
            direction = self.nd_dict2[node].Successors.index(ans[i])+1
            if direction == 1 :
                dir_list.append(1)
            if direction == 2 :
                dir_list.append(3)
            if direction == 3 :
                dir_list.append(4)
            if direction == 4 :
                dir_list.append(2)

        turn = []
        turn.append('F')
        for i in range(0,len(dir_list)-1):
            dif = dir_list[i+1]-dir_list[i]
            if dif == -1 or dif == 3:
                turn.append('L')
            elif dif == 1 or dif == -3:
                turn.append('R')
            elif dif == 0:
                turn.append('F')
            elif dif == 2 or dif == -2:
                turn.append('B')

        return turn

    def findend(self):
        global End,pt_list
        
        End = []
        pt_list = []
        for i in self.nd_dict:
            if node.Node.isEnd(self.nd_dict[i]) == True:
                End.append(int(self.nd_dict[i].index))
        print('要走的點:',End)
        return self.findshortest(1, -1)

    def findshortest(self,start_pt, reached_pt):
        dist_list = []
        
        if reached_pt in End:
            End.remove(reached_pt)
        print('剩下的點:',End)
        
        if len(End) == 0:
            return pt_list
            
        for j in End:
            dist_list.append(len(self.shortestPath(start_pt, j)))

        #print(End)
        #print(dist_list)
        #while len(dist_list) > 0:
        shortest = min(dist_list)
        #print(shortest)
        pt_pos=dist_list.index(shortest)
        print('[剩下的點]第{}個點'.format(pt_pos))
        pt = End[pt_pos]
        print(pt,'點被增加到pt_list')
        pt_list.append(int(pt))
        print('目前路徑:',pt_list)
        print('----------------------')
        #dist_list.remove(shortest)
        #End.remove(pt)
        #print(End)
        #print(dist_list)
        start_pt = pt
        reached_pt = pt
            
        return self.findshortest(start_pt,reached_pt)
            
            


        
                
                
            
            
            
            
    

                    


