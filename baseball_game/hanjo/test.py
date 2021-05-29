from itertools import permutations
import random


number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
num_list = list(map(''.join, permutations(number, 4)))
server_answer = num_list[random.randrange(0, len(num_list))]
print(server_answer)