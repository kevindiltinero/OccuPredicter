import random
import Stack
from datetime import timedelta

mac_addresses = ['11:23:aa', '11:23:ab', '11:23:ac', '11:29:ad', '11:13:ae', '11:44:af', '11:49:ag']

#Graph of the school nodes APs
adjlist_dict = {'ap1': [[], ['ap2', 'ap3', 'ap14', 'ap15', 'ap18', 'ap30']],
                'ap2': [[], ['ap1', 'ap30']],
                'ap3': [[], ['ap1', 'ap4']],
                'ap4': [[], ['ap5', 'ap6', 'ap7', 'ap8', 'ap9', 'ap10', 'ap11', 'ap12']],
                'ap5': [[], ['ap4']],
                'ap6': [[], ['ap4']],
                'ap7': [[], ['ap4']],
                'ap8': [[], ['ap4']],
                'ap9': [[], ['ap54']],
                'ap10': [[], ['ap54']],
                'ap11': [[], ['ap54']],
                'ap12': [[], ['ap54']],
                'ap13': [[], ['ap1']],
                'ap14': [[], ['ap1']],
                'ap15': [[], ['ap1', 'ap18']],
                'ap16': [[], ['ap18']],
                'ap17': [[], ['ap18']],
                'ap18': [[], ['ap17', 'ap16', 'ap15', 'ap1']],
                'ap19': [[], ['ap9', 'ap10', 'ap11', 'ap12']],
                'ap20': [[], ['ap30']],
                'ap21': [[], ['ap30']],
                'ap22': [[], ['ap31']],
                'ap23': [[], ['ap31']],
                'ap24': [[], ['ap31']],
                'ap25': [[], ['ap31']],
                'ap26': [[], ['ap31']],
                'ap27': [[], ['ap31', 'ap32']],
                'ap28': [[], ['ap32', 'ap33']],
                'ap29': [[], ['ap33']],
                'ap30': [[], ['ap1', 'ap2', 'ap20', 'ap21', 'ap31', 'ap33']],
                'ap31': [[], ['ap22', 'ap23', 'ap24', 'ap25', 'ap26']],
                'ap32': [[], ['ap27', 'ap28', 'ap31']],
                'ap33': [[], ['ap28', 'ap29', 'ap30']],
                'ap34': [[], ['ap4', 'ap35', 'ap37', 'ap38', '']],
                'ap35': [[], ['ap36', 'ap39', 'ap40', 'ap41', 'ap42', 'ap43', 'ap44']],
                'ap36': [[], ['ap45', 'ap45', 'ap46', 'ap47', 'ap48', 'ap49']],
                'ap37': [[], ['ap34']],
                'ap38': [[], ['ap34']],
                'ap39': [[], ['ap35']],
                'ap40': [[], ['ap35']],
                'ap41': [[], ['ap35']],
                'ap42': [[], ['ap35']],
                'ap43': [[], ['ap35']],
                'ap44': [[], ['ap35']],
                'ap45': [[], ['ap36']],
                'ap46': [[], ['ap36']],
                'ap47': [[], ['ap36']],
                'ap48': [[], ['ap36']],
                'ap49': [[], ['ap36']],
                'ap50': [[], ['ap53']],
                'ap51': [[], ['ap53']],
                'ap52': [[], ['ap53']],
                'ap53': [[], ['ap34', 'ap50', 'ap51', 'ap52']],
                'ap54': [[], ['ap9', 'ap10', 'ap11', 'ap12']],
                '':['ap34', 'ap50', 'ap51', 'ap52'],
                'a':['ap34', 'ap50', 'ap51', 'ap52'],
                'p':['ap34', 'ap50', 'ap51', 'ap52'],
                '5':['ap34', 'ap50', 'ap51', 'ap52'],
                '0':['ap34', 'ap50', 'ap51', 'ap52']
                }

# PATH FINDING ALGORITHM
def path_profiling(adjlist_dict):
    for key in adjlist_dict:
        route_stack = Stack.Stack()
        visited_list = []
        paths = []

        route_stack.push(key)
        visited_list.append(key)

        while not route_stack.is_empty():

            current = route_stack.top()

            #Get the unvisited neighbours for observation
            neighbours = []
            for neighbour in adjlist_dict[current][1]:
                if neighbour not in visited_list:
                    neighbours.append(neighbour)

            if len(neighbours) == 0:
                print(route_stack.my_array)  #paths.append(route_stack.my_array)
                route_stack.pop()
    #
            else:
                route_stack.push(neighbours[0])
                visited_list.append(neighbours[0])







#
# #Deployment of mac addresses from a path
# for mac in mac_addresses:
#     num_neigh = 5
#     current_ap = 'ap1'
#     while num_neigh > 0:
#         adjlist_dict[current_ap][0].append(mac)
#         num_neigh = len(adjlist_dict[current_ap][1])
#         if num_neigh > 0:
#             choice = random.randrange(0, num_neigh, 1)
#             current_ap = adjlist_dict[current_ap][1][choice]
#
# keys = adjlist_dict.keys()
# for key in keys:
#     print(key, adjlist_dict[key][0])

# d = timedelta()
# for i in range(1000):
#     print(d.microseconds)