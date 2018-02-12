import random
from entity_types import *



def pick_enemy():
    return random.choice(enemy_types)

def display_stats(player, curr_enemy, n_round):
    print('#{}==========================================={}#'.format(n_round, n_round))
    print('\n\t\tPLAYER\t{}'.format(curr_enemy.name.upper()))
    print('\t\tHP: {}\tHP: {}'.format(str(player.hp), str(curr_enemy.hp)))
    print('\t\tMP: {}\tMP: {}'.format(str(player.mp), str(curr_enemy.mp)))
    print(curr_enemy.text)
    print('\t1. Attack\t 2. Magic\n\t3. Inventory\t 4. Run')
    user_in = -1
    while user_in < 1 or user_in > 4:
        print('\t>> ', end='')
        user_in = int(input())
    return user_in

def is_alive(entity):
    if entity.hp > 0:
        return True
    else:
        return False

def player_turn(user_in, player, curr_enemy):
    if user_in == 1:
        curr_enemy.hp -= player.attack(curr_enemy)
    elif user_in == 2:
        curr_enemy.hp -= player.magic(curr_enemy)
    elif user_in == 3:  #TODO
        pass
    else:               #TODO
        pass

def enemy_turn(player, enemy):
    rand = random.randint(1,2)
    if rand == 1:
        player.hp -= enemy.attack(player)
    elif rand == 2:
        player.hp -= enemy.magic(player)

def next_round(player):
    player.hp += 5
    player.mp += 5
    player.atk += 1
    player.sag += 1
    player.armor += 1
    player.magic_res += 1

    next_enemy = Entity(pick_enemy())
    print('\t{} APPEARED !'.format(next_enemy.name.upper()))
    return next_enemy

def main():
    n_round = 1
    player = Entity('player')
    curr_enemy = Entity(pick_enemy())
    while(1):   # Game Loop
        user_input = display_stats(player, curr_enemy, n_round)
        player_turn(user_input, player, curr_enemy)
        if not is_alive(curr_enemy):
            print('\t{} DEFEATED !'.format(curr_enemy.name.upper()))
            n_round += 1
            curr_enemy = next_round(player)
        enemy_turn(player, curr_enemy)
        if not is_alive(player):
            print('\t{} DEFEATED !'.format(player.name.upper()))
            print('\tYOU\'VE REACHED ROUND #{}'.format(n_round))
            break
        
        
    
if __name__ == '__main__':
    main()
