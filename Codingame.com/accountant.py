import sys
import math
import numpy as np
from operator import itemgetter

# Shoot enemies before they collect all the incriminating data!
# The closer you are to an enemy, the more damage you do but don't get too close or you'll get killed.

enemies = {}
data = {}
data_distance = {}
enemy_distance_dict = {}
enemy_distance_list = []
    
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
        enemies[enemy_id] = [enemy_x, enemy_y, enemy_life, 0, 0]
        
        
    data_distance.clear()
    enemy_distance_dict.clear()
    del enemy_distance_list[:]
    for enemy_key in enemies:
        enemy_distance_for_one = math.hypot(enemies[enemy_key][0] - x, enemies[enemy_key][1] - y)
        enemy_distance_dict[enemy_key] = enemy_distance_for_one
        enemy_distance_list.append(enemy_distance_for_one)
        
        closest_data_to_enemy = 100000000
        closest_data_x = 0
        closest_data_y = 0
        
        for data_key in data:
            distance_to_data_point = math.hypot(data[data_key][0] - enemies[enemy_key][0], data[data_key][1] - enemies[enemy_key][1])
            
            if distance_to_data_point < closest_data_to_enemy:
                closest_data_to_enemy = distance_to_data_point
                closest_data_x = data[data_key][0]
                closest_data_y = data[data_key][1]
            
        data_distance[enemy_key] = closest_data_to_enemy
        
        enemies[enemy_key][3] = closest_data_x
        enemies[enemy_key][4] = closest_data_y
    
    index_of_enemy_to_data = min(data_distance, key=data_distance.get)
    data_distance_to_enemy = data_distance[index_of_enemy_to_data]
    
    index_of_enemy_to_player = min(enemy_distance_dict, key=enemy_distance_dict.get)
    enemy_distance_to_player = enemy_distance_dict[index_of_enemy_to_player]
    
    if enemy_distance_to_player < 3000:    
        enemy = enemies[index_of_enemy_to_player]
        enemy_x = enemy[0]
        enemy_y = enemy[1]
        data_x = enemy[3]
        data_y = enemy[4]
        user_distance_to_data = math.hypot(x - data_x, y - data_y)
        close_enemy_distance_to_data = math.hypot(enemy_x - data_x, enemy_y - data_y)
        print(user_distance_to_data, enemy_distance_to_player, file=sys.stderr)
        
        if user_distance_to_data < close_enemy_distance_to_data:
            x_to_move = x + (x - enemy_x)
            y_to_move = y + (y - enemy_y)
            
            if x_to_move > 16000:
                x_to_move = 16000
            if y_to_move > 9000:
                y_to_move = 9000
            
            print(x_to_move, y_to_move, x, y, file=sys.stderr)
            if abs(x - x_to_move) + abs(y - y_to_move) < 500:
                print("done fucked up", file=sys.stderr)
            
        
            print("MOVE {} {}".format(x_to_move, y_to_move))
            continue

    if enemy_distance_to_player - 3500 < data_distance_to_enemy: 
        print("SHOOT {}".format(index_of_enemy_to_player))
    else:
        print("SHOOT {}".format(index_of_enemy_to_data))
