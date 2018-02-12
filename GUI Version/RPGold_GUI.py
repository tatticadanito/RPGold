import pygame
import sys
from pygame.locals import *
import random
from rpg_module import *

def terminate(n):
    ''' Exit the game and display end screen '''
    gameDisplay.fill(Black)
    end_surface = gen_txt_surface('YOU HAVE REACHED ROUND #{}'.format(n), 40, White, Black)
    end_text = end_surface.get_rect()
    end_text.center = (display_w/2, display_h/2)
    gameDisplay.blit(end_surface, end_text)
    pygame.display.update()
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN or event.type == QUIT:
            pygame.quit()
            sys.exit()

def general_print(original_txt, size, color, bg_color, x, y):
    ''' Function to put a text on the next display update '''
    surface = gen_txt_surface(original_txt, size, color, bg_color)
    text = surface.get_rect()
    text.center = (x, y)
    gameDisplay.blit(surface, text)

def pick_enemy():
    ''' Returns a random enemy '''
    return random.choice(enemy_types)

def gen_txt_surface(text, dim, color, bg_color):
    ''' Returns text surface'''
    font = pygame.font.Font('freesansbold.ttf', dim)
    return font.render(text, True, color, bg_color)

def display_stats(player, curr_enemy, n_round):
    ''' Displays the GUI '''
    enemy_loc = (display_w*0.6, display_h*0.2)
    # Background
    gameDisplay.fill(White)
    # N round
    general_print('ROUND #{}'.format(n_round), 17, Black, White, 70, 40)
    # Enemy action
    if curr_enemy.can_attack:
        if curr_enemy.last_attack != 2:
            general_print('{} USED {}'.format(curr_enemy.name.upper(), curr_enemy.attacks[curr_enemy.last_attack]), 17, Black, White, 500, 60)
        else:
            general_print('{} DOESN\'T HAVE ENOUGH MANA TO CAST {}'.format(curr_enemy.name.upper(), curr_enemy.attacks[1]), 17, Black, White, 500, 60)
    # Display actions
    general_print('[1] Attack        [2] Magic        [3] Inventory        [4] Run', 18, Black, White, display_w/2, display_h*0.8)
    # Enemy sprite
    gameDisplay.blit(curr_enemy.sprite, enemy_loc) 
    # Player text
    general_print('[PLAYER]', 20, Blue, White, 200, 150)
    # Player HP
    general_print('HP: {}   MP: {}'.format(player.hp, player.mp), 17, Blue, White, 200, 180)
    # Enemy text
    general_print('[ENEMY]', 20, Red, White, 200, 250)
    # Enemy HP
    general_print('HP: {}   MP: {}'.format(curr_enemy.hp, curr_enemy.mp), 17, Red, White, 200, 280)

    pygame.display.update()

def is_alive(hp):
    ''' Check if entity is alive or not '''
    if hp > 0:
        return True
    else:
        return False

def run(player, curr_enemy, n_round):
    if random.randint(1, 5) == 1:
        next_enemy = Entity(pick_enemy(), n_round, player)
        next_enemy.can_attack = True
        gameDisplay.fill(White)
        general_print('YOU RAN AWAY FROM THE {} !'.format(curr_enemy.name.upper()), 16, Black, White, display_w/2, 40)
        general_print('INCOMING ATTACK FROM A {} !'.format(next_enemy.name.upper()), 16, Black, White, display_w/2, 80)
        gameDisplay.blit(next_enemy.sprite, (370, 150))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                break
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        return next_enemy
    else:
        return curr_enemy
        pass
        

def potion(player):
    ''' Use potion '''
    player.inv['potion'] -= 1
    player.hp += 30
    if player.hp > 50:
        player.hp = 50

def bomb(player, enemy):
    ''' Use bomb '''
    player.inv['bomb'] -= 1
    enemy.hp -= 30

def no_item():
    ''' Display messagge when the item select isn't available '''
    gameDisplay.fill(White)
    general_print('ITEM NOT AVAILABLE !', 16, Black, White, display_w/2, 40)
    general_print('TURN LOST', 16, Black, White, display_w/2, 80)
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            break
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

def inventory(player, enemy):
    ''' Open inventory and let the user select what to use '''
    gameDisplay.fill(White)
    general_print('[INVENTORY]', 25, Black, White, display_w*0.5, display_h*0.2)
    general_print('[1]    {} POTION'.format(player.inv['potion']), 17, Black, White, 200, 200)
    gameDisplay.blit(pygame.image.load('sprites/potion.png'), (280, 180))
    general_print('[2]    {} BOMB'.format(player.inv['bomb']), 17, Black, White, 192, 230)
    gameDisplay.blit(pygame.image.load('sprites/bomb.png'), (280, 210))
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            # Select potion
            if event.key == K_1:
                if player.inv['potion'] > 0:
                    potion(player)
                    break
                else:
                    no_item()
                    break
            # Select bomb
            elif event.key == K_2:
                if player.inv['bomb'] > 0:
                    bomb(player, enemy)
                    break
                else:
                    no_item()
                    break


def player_turn(player, curr_enemy, n_round):
    ''' Allow the player to perform an action '''
    curr_enemy.can_attack = True

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_1:
                curr_enemy.hp -= player.attack(curr_enemy)
                break
            elif event.key == K_2:
                curr_enemy.hp -= player.magic(curr_enemy)
                break
            elif event.key == K_3:
                inventory(player, curr_enemy)
                break
            elif event.key == K_4:
                curr_enemy = run(player, curr_enemy, n_round)
                break;
    return curr_enemy
    
            
        

def enemy_turn(player, enemy):
    ''' Enemy "AI" '''
    rand = random.randint(1,2)
    if rand == 1:
        player.hp -= enemy.attack(player)
    elif rand == 2:
        player.hp -= enemy.magic(player)

    return enemy

def check_drop():
    ''' Check if enemy dropped items '''
    drop = [0,0]    # [POTION, BOMB]
    for i in range(2):
        if random.randint(0,1):
            drop[i] = 1
    return drop[0], drop[1]
        
    

def next_round(player, curr_enemy, n_round):
    ''' Buff player and pick next enemy '''
    player.hp += 5
    player.mp += 5
    player.atk += 1
    player.sag += 1
    player.armor += 1
    player.magic_res += 1

    next_enemy = Entity(pick_enemy(), n_round, player)
    gameDisplay.fill(White)
    general_print('{} DEFEATED !'.format(curr_enemy.name.upper()), 16, Black, White, display_w/2, 40)
    general_print('A {} APPEARED !'.format(next_enemy.name.upper()), 16, Black, White, display_w/2, 80)
    gameDisplay.blit(next_enemy.sprite, (370, 150))
    # Enemy drop
    drop_pot, drop_bomb = check_drop()
    player.inv['potion'] += drop_pot
    player.inv['bomb'] += drop_bomb
    general_print('THE {} HAS DROPPED:'.format(curr_enemy.name.upper()), 16, Black, White, display_w/2, 400)
    general_print('{} POTION'.format(drop_pot), 16, Black, White, display_w/2, 430)
    gameDisplay.blit(pygame.image.load('sprites/potion.png'), (440, 410))
    general_print('{} BOMB'.format(drop_bomb), 16, Black, White, display_w/2, 460)
    gameDisplay.blit(pygame.image.load('sprites/bomb.png'), (440, 440))
    
    pygame.display.update()
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            break
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    return next_enemy

def main():
    ''' Main function '''
    player = Entity('player')
    n_round = 1
    curr_enemy = Entity(pick_enemy(), n_round, player)
    while(is_alive(player.hp)):   # Game Loop
        display_stats(player, curr_enemy, n_round)
        curr_enemy = player_turn(player, curr_enemy, n_round)
        if not is_alive(curr_enemy.hp):
            n_round += 1
            curr_enemy = next_round(player, curr_enemy, n_round)
        if curr_enemy.can_attack:
            curr_enemy = enemy_turn(player, curr_enemy)
        clock.tick(30)

    terminate(n_round)

if __name__ == '__main__':
    pygame.init()
    random.seed()
    gameDisplay = pygame.display.set_mode((display_w, display_h))
    pygame.display.set_caption('RPGold')
    clock = pygame.time.Clock()
    main()
