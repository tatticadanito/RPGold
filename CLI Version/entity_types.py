enemy_types = ('goblin', 'zombie', 'mage', 'drake')

class Entity:
    name = str()
    hp = int()
    mp = int()
    atk = int()
    sag = int()
    armor = int()
    magic_res = int()
    text = str()
    
    def __init__(self, type_entity):
        self.name = type_entity
        if self.name == 'player':
            self.hp = 100
            self.mp = 25
            self.atk = 5
            self.sag = 5
            self.armor = 2
            self.megic_res = 2
            self.text = (r'')
        # Goblin
        elif self.name == enemy_types[0]:
            self.hp = 30
            self.mp = 3
            self.atk = 4
            self.sag = 0
            self.armor = 1
            self.megic_res = 2
            self.text = (r'''                     
               /(.-""-.)\
           |\  \/      \/  /|
           | \ / =.  .= \ / |
           \( \   o\/o   / )/
            \_, '-/  \-' ,_/
              /   \__/   \
              \ \__/\__/ /
            ___\ \|--|/ /___
          /`    \      /    `\
         /       '----'       \'''')
        # Zombie
        elif self.name == enemy_types[1]:
            self.hp = 60
            self.mp = 0
            self.atk = 2
            self.sag = 0
            self.armor = 0
            self.magic_res = 0
            self.text = (r'''                           (()))
                           /|x x|
                          /\( - )
                     ___.-._/\/
                 /=`_'-'-'/  !!
                 |-{-_-_-}     !
                 (-{-_-_-}    !
                  \{_-_-_}   !
                    }-_-_-}
                   {-_|-_}
                   {-_|_-}
                   {_-|-_}
                   {_-|-_}  
                ____%%@ @%%____''')
        # Mage
        elif self.name == enemy_types[2]:
            self.hp = 45
            self.mp = 60
            self.atk = 3
            self.sag = 12
            self.armor = 3
            self.magic_res = 4
            self.text = (r'''                 ,    _
                /|   | |
              _/_\_  >_<
             .-\-/.   |
            /  | | \_ |
            \ \| |\__(/
            /(`---')  |
           / /     \  |
        _.'  \'-'  /  |
        `----'`=-='   '   ''')
        # Drake
        elif self.name == enemy_types[3]:
            self.hp = 90
            self.mp = 20
            self.atk = 15
            self.sag = 5
            self.armor = 7
            self.magic_res = 7
            self.text = (r'''                      ,-,-      
                     / / |      
   ,-'             _/ / /       
  (-_          _,-' `Z_/        
   "#:      ,-'_,-.    \  _     
    #'    _(_-'_()\     \" |    
  ,--_,--'                 |    
 / ""                      L-'\ 
 \,--^---v--v-._        /   \ | 
   \_________________,-'      | 
                    \           
                     \          
                      \         ''')

    def attack(self, enemy):
        print('\t{} ATTACKED !'.format(self.name.upper()))
        dmg = int((self.atk - enemy.armor)*2)
        if self.atk - enemy.armor < 1:
            dmg = 1
        return dmg

    def magic(self, enemy):
        if self.mp > 4:
            print('\t{} CASTED A SPELL !'.format(self.name.upper()))
            dmg = int((self.sag - enemy.magic_res)*2)
            if self.sag - enemy.magic_res < 1:
                dmg = 1
            self.mp -= 5
            return dmg
        else:
            print('\t{} DOESN\'T HAVE ENOUGH MP !'.format(self.name.upper()))
            return 0
