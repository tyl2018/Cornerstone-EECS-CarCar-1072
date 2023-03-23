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
                    nd2.setSuccessor(int(dt[i]))
                if math.isnan(dt[i]):
                    nd2.setSuccessor(0)

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
        End = []
        distance= 10000
        pt_list = []
        dist_list = []
        for i in self.nd_dict:
            if node.Node.isEnd(self.nd_dict[i]) == True:
                End.append(int(self.nd_dict[i].index))
        
        for j in End:
            dist_list.append(len(self.shortestPath(1, j)))
        print(End)
        
        farthest = max(dist_list)
        pt_pos=dist_list.index(farthest)
        far_point = End[pt_pos]
        End.remove(far_point)

        count = 0
        for path_pt in self.shortestPath(1,far_point)[1:]:
            for end1 in End:
                if end1 != 0:
                    if len(self.shortestPath(int(path_pt),int(end1))) <= 3:
                        pt_list.append(int(end1))
                        a = End.index(end1)
                        End[a] = 0
                        count += 1
        for remove in range(count):
            End.remove(0)
      
        pt_list.append(int(far_point))
        
        dist_list2 = []
        for end2 in End:
            dist_list2.append(len(self.shortestPath(far_point, end2)))

        while len(dist_list2) > 0:
            shortest = min(dist_list2)
            pt_pos=dist_list2.index(shortest)
            pt = End[pt_pos]
            pt_list.append(int(pt))
            dist_list2.remove(shortest)
            End.remove(pt)
        pt_list.remove(2)
        return pt_list
                

        
                
                
            
            
            
            
    

                    


