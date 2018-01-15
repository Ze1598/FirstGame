#A simple turn-based combat "game" that takes the player through 10 stages.
#Players will have the option to name their character and during battle the available actions \
#are: Attack, Use HP Potion (recover HP) and Guard.
#At the end of each stage, the players will be given the chance to quit the game.
#For both the player and the enemies, the attack values will be a randomised value from a\
#given range

#Necessary module import
from random import randint, choice, shuffle

#Class to create characters, both the player and the enemies
class Character():
    def __init__(self, name, max_health, min_atk, max_atk, potions):
        self.name = name
        #max HP for the character
        self.max_health = max_health
        self.min_atk = min_atk
        self.max_atk = max_atk
        #number of HP potions held
        self.potions = potions
        #HP value to be used during battles
        self.health = max_health

#Creates the chance for a character to dodge an incoming attack
#70% chance to be hit, 30% chance to dodge
#The chance is interpreted as "rng" (random number generated)
dodge_rng = ['hit' for i in range(7)] + ['dodge' for i in range(3)]
shuffle(dodge_rng)

#Create the rng for the player to have a boost to his atk values
atk_upg_rng = ['upgrade' for i in range(6)] + ['keep' for i in range(4)]
shuffle(atk_upg_rng)

#possible names for the enemies
enemy_names = ['Aamon', 'Abraxas', 'Satanael', 'Beelzebub', 'Berith', 'Gorgon', 
'Lilith', 'Leviathan', 'Malphas', 'Mamom', 'Orobas', 'Paimon', 'Rahab', 'Tannin', 'Zagan']

#Prompt the player to name their character
player_name = input("Before showing your stats, choose a name for you character: ")
#Instantiate the 'Character' class to create an object for the player
player = Character(player_name, 500, 120, 150, 0)
#Name:player_name; MaxHP: 500; MinAtk: 120; MaxAtk: 150; Potions: 0
print(f'These are your stats:\n\tYour character name is "{player.name}";\
\n\tMax HP: {player.max_health};\n\tAttack range: {player.min_atk} to {player.max_atk};\n\t\
HP Potions held: {player.potions}.')

#Initiate a data attribute for 'player', to keep track of how many turns have been played
player.turns = 0
#Initiate a data attribute for 'player', to keep track if the player has completed a stage or not
player.complt_stg = True
#Initiate a data attribute for 'player', for when it gets an HP Overshield
player.overshield = 0

#function to contain all possible events in each turn, and runs until either the player or the enemy dies
def gameplay(stg):
    #Create the enemy
    #Choose a random name from the list, then delete it so it can't be repeated in future stages
    enemy_name = choice(enemy_names)
    enemy_names.remove(enemy_name)
    #Instantiate an object for this stage's enemy
    #base max_hp: 200; base min_atk: 100; base max_atk: 120
    #Enemy's HP is incremented by 75 per stage, and ATK values are incremented by 20
    #(enemy_name, max_hp, min_atk, max_atk, potions_held)
    enemy = Character(enemy_name, (200+75*(stg-1)), (100+20*(stg-1)), (120+20*(stg-1)), 0)

    #True if the first turn of the stage hasn't been played yet; else False
    stg_start = True

    #While both the player and the enemy are alive
    while player.health > 0 and enemy.health > 0:
    #Introduction for each stage (only executed in the first turn of each stage)
        if stg_start:
            print()
            print('This is stage {}!'.format(stg))
            print(f'The enemy for this stage is {enemy_name}.')
            print('Your HP is {} and {}\'s HP is {}.'.format(player.max_health, enemy_name, enemy.max_health))
            print(f'You have {player.potions} HP Potions.')
            #Makes it so this If clause won't be executed again in this stage
            stg_start = False
            print()
        
    #Message shown at the start of each turn:
        #Prompts the player to choose an action
        print('{:>5} | {:>5} | {:>5}'.format('Attack', 'Guard', 'Use HP Potion'))
        action = input('What are you going to do?')
        print()

    #Player chooses to Attack
        if 'attack' in action.lower():
            #Test if the enemy dodges the attack
            if choice(dodge_rng) == 'dodge':
                print(f'{enemy_name} dodged your attack!')
                shuffle(dodge_rng) 
                print()
            #Enemy is hit
            else:
                damage_to_enemy = randint(player.min_atk, player.max_atk)
                enemy.health -= damage_to_enemy
                print(f'{player_name} dealt {damage_to_enemy} damage to the enemy.')
                fwrd = input()
                #If the enemy died from the attack
                if enemy.health < 1:
                    #Player cleared the stage successfully
                    print()
                    print(f'{enemy_name} has been defeated.')
                    print(f'Congratulations, you have cleared stage {stg}!')
                    #But if this is the last stage make it as if the player has lost, \
                    #so it doesn't execute the while statement outside this function
                    if stg == 10:
                        player.complt_game = True
                    continue

            #If the enemy is still alive
            if enemy.health > 0: 
                #If the player dodges the attack
                if choice(dodge_rng) == 'dodge':
                    print('{} dodged {}\'s attack!'.format(player_name, enemy_name))
                    shuffle(dodge_rng) 
                    print()
                #Else the player is hit
                else:
                    #Damage to be dealt to the player
                    player_damage = randint(enemy.min_atk, enemy.max_atk)
                    #Check if the player currently has an overshield
                    if player.overshield > 0:
                        #If the damage is bigger than the overshield, it is destroyed and the player loses some health
                        if player_damage > player.overshield:
                            player.health -= player_damage - player.overshield
                            player.overshield = 0
                            print(f'{enemy_name} dealt {player_damage} damage to you.')
                            print('You\'ve lost your overshield.')
                        #If the damage is smaller than the overshield, the overshield loses some health
                        elif player_damage < player.overshield:
                            player.overshield -= player_damage
                        #If the damage is equal to the overshield, the overshield is destroyed
                        else:
                            player.overshield = 0
                            print(f'{enemy_name} dealt {player_damage} damage to you.')
                            print('You\'ve lost your overshield.')
                    #Else the player doesn't have an overshield, simply subtract its health
                    else:
                        player.health -= player_damage
                        print(f'{enemy_name} dealt {player_damage} damage to you.')
                    fwrd = input()
                    #If the player dies from the attack
                    if player.health < 1:
                        print()
                        print('You\'ve been defeated by {}.GAME OVER!'.format(enemy_name))
                        player.complt_stg = False
            
    #Player chooses to use a Potion
        elif 'potion' in action.lower(): 
            #If the player doesn't have potions
            if player.potions == 0:
                print()
                print('You currently don\'t have any potions.')
            
            #Else the player has at least 1 potion
            else:
                #Heal the player with 250 HP 
                player.health += 250
                #Decrement the number of potions held by the player by 1
                player.potions -= 1
                #Test if the player got an overshield (current HP > max HP)
                if player.health > player.max_health:
                    #Create an overshield data attribute
                    player.overshield = player.health - player.max_health
                    #Restore current health to the value of max HP
                    player.health = player.max_health
                    print('You\'ve gained an overshield of {} HP.\nCurrent HP:{}+{}'.format(player.overshield, player.health, player.overshield))
                    fwrd = input()
                
                #After the player uses a potion the enemy can attack
                #Test if the player dodges the attack
                if choice(dodge_rng) == 'dodge':
                    print('You dodged {}\'s attack}!'.format(enemy_name))
                #Else the player is hit
                else:
                    player_damage = randint(enemy.min_atk, enemy.max_atk)
                    #Check if the player currently has an overshield
                    if player.overshield > 0:
                        #If the damage is bigger than the overshield, it is destroyed and the player loses some health
                        if player_damage > player.overshield:
                            player.health -= player_damage - player.overshield
                            player.overshield = 0
                            print(f'{enemy_name} dealt {player_damage} damage to you.')
                            print('You\'ve lost your overshield.')
                        #If the damage is smaller than the overshield, the overshield loses some health
                        elif player_damage < player.overshield:
                            player.overshield -= player_damage
                        #If the damage is equal to the overshield, the overshield is destroyed
                        else:
                            player.overshield = 0
                            print(f'{enemy_name} dealt {player_damage} damage to you.')
                            print('You\'ve lost your overshield.')
                    #Else the player doesn't have an overshield, simply subtract its health
                    else:
                        player.health -= player_damage
                        print(f'{enemy_name} dealt {player_damage} damage to you.')
                    fwrd = input()

                #If the player dies from the attack
                if player.health < 1:
                    print()
                    print('You\'ve been defeated by {}.GAME OVER!'.format(enemy_name))
                    player.complt_stg = False

    #Player chooses to Guard
        elif 'guard' in action.lower():
            print('You guarded against {}\'s next attack!'.format(enemy_name))
            #After the player guards it's time for the enemy to attack
            player_damage = randint(enemy.min_atk, enemy.max_atk)
            #Check if the player currently has an overshield
            if player.overshield > 0:
                #If the damage is bigger than the overshield, it is destroyed and the player loses some health
                if player_damage > player.overshield:
                    player.health -= player_damage - player.overshield
                    player.overshield = 0
                    print(f'{enemy_name} dealt {player_damage} damage to you.')
                    print('You\'ve lost your overshield.')
                #If the damage is smaller than the overshield, the overshield loses some health
                elif player_damage < player.overshield:
                    player.overshield -= player_damage
                #If the damage is equal to the overshield, the overshield is destroyed
                else:
                    player.overshield = 0
                    print(f'{enemy_name} dealt {player_damage} damage to you.')
                    print('You\'ve lost your overshield.')
            #Else the player doesn't have an overshield, simply subtract its health
            else:
                player.health -= player_damage
                print(f'{enemy_name} dealt {player_damage} damage to you.')
            fwrd = input()

            #If the player dies from the attack
            #If the player dies from the attack
            if player.health < 1:
                print()
                print('You\'ve been defeated by {}.GAME OVER!'.format(enemy_name))
                player.complt_stg = False

    #Else the player chooses an invalid action
        else:
            print('Invalid action. Please choose one of the actions available.')
            continue

    #End of turn: print the player and the enemy's health, plus a New Turn notification
    #This last part is only executed if both the player and the enemy are still alive
        print('{}\'s health: {} + an overshield of {}\n{}\'s health: {}'.format(player_name, player.health, player.overshield, enemy_name, enemy.health))
        print()
        print('-----New Turn-----')
        player.turns += 1
        fwrd = input()

#Current stage's number; starts at 1
stg = 1
#Create a data attribute for 'player' to hold True if the player wants to play; else False
player.cont_playing = True
#Data attribute to be True only after the player completes stage 10; until then it's False
player.complt_game = False

#Run this loop until either the player has completed all 10 stages, loses or \
#quits the game
while player.complt_stg and player.cont_playing:
    #Function containing everything regarding the turn-based gameplay
    gameplay(stg)
    
    #Prompt the player to quit the game after completing a stage
    quit_prompt = input('Do you wish to keep playing or do you want to quit?')
    
    #If the player chooses to quit then continue to the next iteration \
    #which will execute the else statement instead of the while since the latter
    #will return False
    if ('stop' or 'no' or 'quit') in quit_prompt.lower():
        player.cont_playing = False
        continue
    print('You chose to continue playing!')
    fwrd = input()
    
    print(f'For completing stage {stg} you receive 1 HP Potion and your max HP will be increased in 100 points.')
    fwrd = input()
    #Increment the player's max HP and then "restore" his 'health' attribute to be at max HP
    player.max_health += 100
    player.health = player.max_health
    #Give the player one HP potion
    player.potions += 1
    
    print('Lastly, let\'s test if you will receive an upgrade to your Attack values.\nChecking the answer...')
    fwrd = input()
    #If the player is to receive an ATK upgrade, upgrade its ATK values then print the player's stats
    if choice(atk_upg_rng) == 'upgrade':
        print('Luck is on your side. Your Attack values are going to be increased by 20 points.')
        shuffle(atk_upg_rng)
        player.min_atk += 20
        player.max_atk += 20
        print(f'Let me show you your updated stats:\n\tMax HP: {player.max_health};\n\tAttack range: {player.min_atk} to {player.max_atk};\n\t\HP Potions held: {player.potions}.')
    #If the player does not receive an ATK upgrade, simply print his stats and an information about the upgrade
    else:
        print('Luck is not your side. Your Attack values will stay the same.')
        print(f'In any way, let me remind you of your stats:\n\tMax HP: {player.max_health};\n\tAttack range: {player.min_atk} to {player.max_atk};\n\t\HP Potions held: {player.potions}.')
    fwrd = input()
    #Player advances to the next stage so increment this variable by 1
    stg += 1

#After the player has completed the game, lost or quit the game
else:
    #If the game was completed print a message and the number of turns played
    if player.complt_game:
        print('Congratulations! You\'ve cleared the game.')
        print(f'In total, it took you {player.turns} to complete the 10 stages.')
    #Else simply print a message 
    else:
        print(f'Thanks for playing. {player_name} played {player.turns} turns.')