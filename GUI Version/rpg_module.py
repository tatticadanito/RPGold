import pygame

Aqua = (0, 255, 255)
Black = ( 0, 0, 0)
Blue = (0, 0, 255)
Fuchsia = (255, 0, 255)
Gray = (128, 128, 128)
Green = (0, 128, 0)
Lime = (0, 255, 0)
Maroon = (128, 0, 0)
Navy_Blue = (0, 0, 128)
Olive = (128, 128, 0)
Purple = (128, 0, 128)
Red = (255, 0, 0)
Silver = (192, 192, 192)
Teal = (0, 128, 128)
White = (255, 255, 255)
Yellow = (255, 255, 0)

display_w = 800
display_h = 600
enemy_types = ('goblin', 'zombie', 'mage', 'drake')

class Entity:
    name = str()
    hp = int()
    mp = int()
    atk = int()
    sag = int()
    armor = int()
    magic_res = int()
    sprite = None
    last_attack = int() # 0=Attack 1=Magic 2=No mana
    
    def __init__(self, type_entity, n_round=None, player_stat=None):
        self.name = type_entity
        if self.name == 'player':
            self.hp = 100
            self.mp = 25
            self.atk = 5
            self.sag = 5
            self.armor = 2
            self.megic_res = 2
            self.sprite = None
            self.inv = {'potion':1, 'bomb':1}
        # Goblin
        elif self.name == enemy_types[0]:
            self.hp = 30
            self.mp = 3
            self.atk = 4 + n_round * 1.5
            self.sag = 0
            self.armor = 1
            self.megic_res = 2
            self.sprite = pygame.image.load('sprites/goblin-ene.png')
            self.can_attack = False
            self.attacks=['BACKSTAB', 'STUPID MAGIC']
        # Zombie
        elif self.name == enemy_types[1]:
            self.hp = 60
            self.mp = 0
            self.atk = 1 + n_round * 2
            self.sag = 0
            self.armor = 1
            self.magic_res = 1
            self.sprite = pygame.image.load('sprites/zombie-ene.png')
            self.can_attack = False
            self.attacks=['BITE', 'STUPID MAGIC']
        # Mage
        elif self.name == enemy_types[2]:
            self.hp = 45
            self.mp = 60
            self.atk = 3 + n_round * 1.2
            self.sag = 12
            self.armor = 3
            self.magic_res = 4
            self.sprite = pygame.image.load('sprites/wizard-ene.png')
            self.can_attack = False
            self.attacks=['FIREBALL', 'FIRESTORM']
        # Drake
        elif self.name == enemy_types[3]:
            self.hp = 90
            self.mp = 20
            self.atk = 15 + n_round * 1.2
            self.sag = 5
            self.armor = 5
            self.magic_res = 5
            self.sprite = pygame.image.load('sprites/dragon-ene.png')
            self.can_attack = False
            self.attacks=['CHARGE', 'FIRE BREATH']

    def attack(self, enemy):
        #print('\t{} ATTACKED !'.format(self.name.upper()))
        dmg = int((self.atk - enemy.armor)*2)
        if self.atk - enemy.armor < 1:
            dmg = 1
        self.last_attack = 0
        return dmg

    def magic(self, enemy):
        if self.mp >= 5:
            #print('\t{} CASTED A SPELL !'.format(self.name.upper()))
            dmg = int((self.sag - enemy.magic_res)*2)
            if self.sag - enemy.magic_res < 1:
                dmg = 1
            self.mp -= 5
            self.last_attack = 1
            return dmg
        else:
            self.last_attack = 2
            return 0
