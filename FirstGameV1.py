#A very simple rpg which takes you through 10 stages. In each stage the player fights an enemy
#taking into account the following stats: health, attack, and potions (regenerates health). The
#enemy stats will be just health and attack. 
#To make sure the fights don't always go the same way each attack will be a randomised number
#between x and y

#modules
from random import randint
from random import choice
from random import shuffle

#variables
potion = 250 #potion restores this much health
turn = 0 #total number of turns to clear the game/turns taken in the atempt

#chance of dodging an attack
dodge_rng = [] #list to hold the possible rng
for i in range(7): 
    dodge_rng.append('hit') #70% chance of getting hit
for i in range(3):
    dodge_rng.append('dodge') #30% of dodging


#player_stats
player_stats = {
    'player_health': 500, #player health
    'player_attack': randint(120, 150), #player attack range
    'player_potions': 0, #player potion stock
    'player_max_health': 500 #needed for operations
}

#possible names for the enemies
enemy_names = ['Aamon', 'Abraxas', 'Satanael', 'Beelzebub', 'Berith', 'Gorgon', 'Lilith', 'Leviathan', 'Malphas', 'Mamom', 'Orobas', 'Paimon', 'Rahab', 'Tannin', 'Zagan']

#easy to read info about each stage
'''
#stage stats
stage1_stats = {'stage1_health': 200, 'stage1_attack': randint(100, 120)}

stage2_stats = {'stage2_health': 275, 'stage2_attack': randint(120, 140)}

stage3_stats = {'stage3_health': 350,'stage3_attack': randint(140, 160)}

stage4_stats = {'stage4_health': 425,'stage4_attack': randint(160, 180)}

stage5_stats = {'stage5_health': 500,'stage5_attack': randint(180, 200)}

stage6_stats = {'stage6_health': 575,'stage6_attack': randint(200, 220)}

stage7_stats = {'stage7_health': 650,'stage7_attack': randint(220, 240)}

stage8_stats = {'stage8_health': 725,'stage8_attack': randint(240, 260)}

stage9_stats = {'stage9_health': 800,'stage9_attack': randint(260, 280)}

stage10_stats = {'stage10_health': 900,'stage10_attack': randint(280, 300)}
'''

#name and stats output
player_name = input("Before showing you your stats, please choose your name:")
print()
print("Your player name is '{}'.".format(player_name))
fwrd = input()
print()
print("Now, let\'s show you your stats: ")
print("Health: {}; Attack: 120-150; Potions: {}".format(player_stats['player_health'], player_stats['player_potions']))
fwrd = input()

#function to contain all possible events in each turn, and runs until either the player or the enemy dies
def stage():
    x= 100 + 20*(stg-1) #enemy's minimum damage; increased by 20 points each stage, starts at 100
    y= 120 + 20*(stg-1) #enemy's maximum damage; increased by 20 points each stage, starts at 120
    stagex_attack = randint(x,y) #how to calculate the enemy's damage output
    stagex_health = 200 + 75*(stg-1) #enemy's health; increased by 75 points each stage, starts at 200

    
    while player_stats['player_health'] > 0 and stagex_health > 0:
        #making sure it's possible to alter the following variables inside this function
        global stg_start
        global turn
        global fwrd
        
        #a simple starting message for each new stage
        if stg_start == True: #the following lines will only be executed in the 1st turn of each stage
            print()
            print('This is stage {}!'.format(stg))
            print('You\'ll be fighting against {}.'.format(stg_name))
            print('Your health is {} and {}\'s health is {}.'.format(player_stats['player_health'], stg_name, stagex_health))
            # print("DEBUG")
            # print('x',x)
            # print('y',y)
            # print('health',stagex_health)
            # print("DEBUG")
            stg_start = False #makes sure only this IF condition is only True in the 1st turn of each stage
            print()
        
        #message shown at the start of each turn:
        #prompts the user player for an action and outputs the current number of potions held
        print('Attack, use a Potion or Guard?')
        print('You currently have {} potions.'.format(player_stats['player_potions']))
        action = input('What are you gonna do?') #player input
        print()
        shuffle(dodge_rng) #shuffle the order of the items in dodge_rng
        
        if 'attack' in action.lower(): #player chooses attack
            if choice(dodge_rng) == 'dodge': #if the enemy dodges the attack
                print('{} dodged your attack!'.format(stg_name))
                shuffle(dodge_rng) #shuffle the order of the items in dodge_rng
                print()
            else: 
                #damage dealt by player
                stagex_damage = stagex_health - (stagex_health - player_stats['player_attack']) #damage done to the enemy
                stagex_health -= stagex_damage #subtract the damage from the enemy's health
                #output of damage dealt
                print('{} dealt {} damage to the enemy.'.format(player_name, stagex_damage))
                player_stats['player_attack'] = randint(120,150)
                fwrd = input()
            
            if stagex_health <= 0: #if enemy dies from player attack
                print()
                print('{} has been defeated.'.format(stg_name))
                print('Congratulations, you\'ve cleared stage {}!'.format(stg))
                i = True #makes sure the stage was a victory
                if stg == 10: #if player completes stage 10 aka last stage
                    i = False
            
            if stagex_health > 0: #if enemy is still alive
                if choice(dodge_rng) == 'dodge': #if player dodges an attck
                    print('{} dodged {}\'s attack!'.format(player_name, stg_name))
                    shuffle(dodge_rng) #shuffle the order of the items in dodge_rng
                    print()
                else: 
                    #enemy attacks the player
                    player_damage = player_stats['player_health'] - (player_stats['player_health'] - stagex_attack) #damage dealt to the player
                    player_stats['player_health'] -= player_damage #subtract the damage dealt by the enemy from the player's health
                    #outputs damage dealt by the enemy
                    print('{} dealt {} damage to you.'.format(stg_name, player_damage))
                    fwrd = input()
                    stagex_attack = randint(x,y) #reset the enemy's attack to a random value between x and y

                    #if the player dies from the enemy attack
                    if player_stats['player_health'] <= 0: 
                        print()
                        print('You\'ve been defeated by', stg_name, ', GAME OVER!')
                        print('In total, your attempt to clear this game lasted', turn,'turns.')
                        i = False #makes sure the stage was failed == player died
            

        if 'potion' in action.lower(): #player chooses to use a potion
            if player_stats['player_potions'] == 0: #in case player doesn't have potions
                print()
                print('You currently don\'t have any potions.')
            
            else: #in case the player has at least 1 potion
                player_stats['player_health'] += potion #heal player
                
                current_health = player_stats['player_health'] #variable used to calculate the overshield
                #overshield only exists if player's health exceeds its current max health
                if player_stats['player_health'] > player_stats['player_max_health']:
                    overshield = current_health - player_stats['player_max_health']
                    #overshield = (current health) - (current max health)
                    print('You\'ve gained an overshield of', overshield, 'Health.' )
                    #output the overshield ammount
                overshield = 0 #resets the overshield to 0
                print('Current Health: {}'.format(current_health)) #output current ammount of health
                player_stats['player_potions'] -= 1 #remove 1 potion from the player inventory
                fwrd = input() #giving the player a chance to read all the outputs
        
                if choice(dodge_rng) == 'dodge': #if player dodges the enemy attack
                    print('{} dodged {}\'s attack}!'.format(player_name, stg_name))
                else:
                    #enemy attacks the player
                    player_damage = player_stats['player_health'] - (player_stats['player_health'] - stagex_attack) #damage dealt to the player
                    player_stats['player_health'] -= player_damage #subtract the damage dealt by the enemy from the player's health
                    #outputs damage dealt by the enemy
                    print(stg_name, 'dealt', player_damage, 'damage to you.')
                    fwrd = input()
                    stagex_attack = randint(x,y) #reset the enemy's attack to a random value between x and y
    
                #if the player dies from the enemy attack
                if player_stats['player_health'] <= 0: 
                    print()
                    print('You\'ve been defeated, GAME OVER!')
                    print('In total, your attempt to clear this game lasted', turn,'turns.')
                    i = False #makes sure the stage was failed
        
        if 'guard' in action.lower(): #player chooses to guard
            print('{} guarded against {}\'s next attack!'.format(player_name, stg_name))
            #output an information telling confirming that the player guarded
            if stagex_health > 0: #if enemy is still alive
                        #enemy attacks the player
                        player_damage = player_stats['player_health'] - (player_stats['player_health'] - stagex_attack)
                        player_stats['player_health'] -= round(0.3 * player_damage) #if the player guarded then the enemy's attack will only deal 30% of it's original damage
                        #outputs damage dealt by the enemy
                        print(stg_name, 'dealt', round(0.3 * player_damage), 'damage to you.')
                        fwrd = input()
                        stagex_attack = randint(x,y) #reset the enemy's attack to a random value between x and y
    
                        #if the player dies from the enemy attack
                        if player_stats['player_health'] <= 0: 
                            print()
                            print('You\'ve been defeated, GAME OVER!')
                            print('In total, your attempt to clear this game lasted', turn,'turns.')
                            i = False #makes sure the stage was failed
            
        #end of a turn; output both player and enemy health, plus a New Turn notification
        if player_stats['player_health'] > 0 and stagex_health > 0:
            print('{}\'s health: {}.'.format(player_name, player_stats['player_health']))
            print('{}\'s health: {}.'.format(stg_name, stagex_health))
            print()
            print('---New Turn---')
        turn += 1 #add 1 to the number of turns since the start of the game
        fwrd = input() #giving the player a chance to read all the outputs

#a function to be called after clearing a stage
#restores health; adds 100 to player's max health; gives player 1 potion 
def stage_clear():  
    global fwrd
    global count_inc

    print('For completing stage', stg, 'you receive 1 Potion and your max Health will be increased in 100 points.')
    player_stats['player_max_health'] += 100 #increase player's max health by 100
    player_stats['player_potions'] += 1 #give the player 1 potion
    print('Your health will also be completely restored.') #restore health
    player_stats['player_health'] = player_stats['player_max_health'] #make sure both of the player's health variables are at the same value
    fwrd = input() #giving the player a chance to read all the outputs
    #outputs current max health and number of potions held
    print('Current Max Health: {}.'.format(player_stats['player_max_health']))
    print('Number of Potions held: {}.'.format(player_stats['player_potions']))
    print()

def quit_game(): #tests if the player wants to keep playing after clearing each stage
    global i
    global fwrd
    quit_prompt = input('Do you wish to keep playing or do you wanna stop?')
    if ('stop' or 'no') in quit_prompt.lower():
        i = False #this means the next stage won't start and the game will end
    else:
        print('Then let\'s keep going!')
        fwrd = input()


i = True #variable to identify if a stage was cleared or failed == player died; starts as True to make the loop work; this variable will also be used to test if a player wants to keep playing after clearing a stage
while i == True: #while the player doesn't fail a stage or completes all stages
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg = 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs

    #test if the player wants to keep playing
    quit_game() 
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs

    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs

    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs
    
    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs
    
    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs
    
    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs
    
    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs
    
    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs
    
    #test if the player wants to keep playing
    quit_game()
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    stg += 1 #variable to be used during the outputs
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs

else:
    print('Congratulations, you\'ve cleared all the stages, which means you\'ve completed the game!')
    print(player_name,'completed the game in', turn, 'turns.')
    print('Thank you very much for playing my very first game.')
