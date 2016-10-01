import sys
import math
import numpy as np

# Shoot enemies before they collect all the incriminating data!
# The closer you are to an enemy, the more damage you do but don't get too close or you'll get killed.

enemies = {}
data = {}
data_distance = {}
enemy_distance_dict = {}
    
# game loop
while True:
    enemies.clear()
    data.clear()
    x, y = [int(i) for i in input().split()]
    data_count = int(input())
    for i in range(data_count):
        data_id, data_x, data_y = [int(j) for j in input().split()]
        data[data_id] = (data_x, data_y)
    enemy_count = int(input())
    for i in range(enemy_count):
        enemy_id, enemy_x, enemy_y, enemy_life = [int(j) for j in input().split()]
        enemies[enemy_id] = (enemy_x, enemy_y, enemy_life)
        
    data_distance.clear()
    enemy_distance_dict.clear()
    enemy_distance_list = []
    for enemy_key in enemies:
        enemy_distance_for_one = math.hypot(enemies[enemy_key][0] - x, enemies[enemy_key][1] - y)
        enemy_distance_dict[enemy_key] = enemy_distance_for_one
        enemy_distance_list.append(enemy_distance_for_one)
        
        print(enemies[enemy_key], enemy_key, file=sys.stderr)
        
        data_distances_for_one_enemy = []
        
        for data_key in data:
            data_distances_for_one_enemy.append(math.hypot(data[data_key][0] - enemies[enemy_key][0], data[data_key][1] - enemies[enemy_key][1]))
            
        data_distance[enemy_key] = min(data_distances_for_one_enemy)
    #    for j in range(enemy_count):
    
    index_of_enemy_to_data = min(data_distance, key=data_distance.get)
    data_distance_to_enemy = data_distance[index_of_enemy_to_data]
    
    index_of_enemy_to_player = min(enemy_distance_dict, key=enemy_distance_dict.get)
    for key in enemy_distance_dict:
        print(enemy_distance_dict[key], key, file=sys.stderr)
    enemy_distance_to_player = enemy_distance_dict[index_of_enemy_to_player]
    
    if enemy_distance_to_player < 4000:    
        enemy = enemies[index_of_enemy_to_player]
        enemy_x = enemy[0]
        enemy_y = enemy[1]
        
        x_to_move = x + (x - enemy_x)
        y_to_move = y + (y - enemy_y)
    
        print("MOVE {} {}".format(x_to_move, y_to_move))
    
    print(enemies[index_of_enemy_to_player][2], file=sys.stderr)
    
    if enemy_distance_to_player < 4000:    
        print("SHOOT {} 1".format(index_of_enemy_to_player))
    else:
        print("SHOOT {} 2".format(index_of_enemy_to_data))
    
    '''
    min_enemy_distance = min(enemy_distance)
    if min_enemy_distance < 3000:
        index_of_enemy = enemy_distance.index(min_enemy_distance)
        print("SHOOT {}".format(index_of_enemy))
        enemies[index_of_enemy] = (90000, 80000)
    else:
        min_data_distance = min(data_distance)
        if min_data_distance < min_enemy_distance:
            data_coord = data[data_distance.index(min_data_distance)]
            print("MOVE {} {}".format(data_coord[0], data_coord[1]))
        
    print(data_distance, enemy_distance, file=sys.stderr)
    print(data, enemies, file=sys.stderr)
    '''
