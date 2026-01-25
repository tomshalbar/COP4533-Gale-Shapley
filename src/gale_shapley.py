

class GaleShapley:
    '''Implementation of the Gale-Shapley algorithem
     
    takes it 2 preference list as a 2D array of ints. First one is the 
    proposing side. 

      
    '''

    def find_matches(self, preference_list1 : dict[int, list[int]], preference_list2 : dict[int, list[int]]) -> list[tuple[int, int]]:
        free_proposer = [key for key in preference_list1.keys()]
        # while 
        

    

p1 = {1: [1, 2, 3], 2: [2, 1, 3], 3: [2, 3, 1],}
p2 = {1: [1, 2, 3], 2: [2, 1, 3], 3: [2, 3, 1],}
gs = GaleShapley()
gs.find_matches(p1, p2)
