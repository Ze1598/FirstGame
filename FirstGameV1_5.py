#A very simple game that takes you through 10 stages. In each stage the player fights an enemy
#taking into account the following stats: health, attack, and potions (regenerates health)
#enemy stats will be just health and attack. 
#To make sure the fights don't always go the same way each attack will be a randomised number
#between x and y
#there's also some dialogue from both the player and the enemy: intro, dodge, victory and defeat

#modules
from random import randint
from random import choice
from random import shuffle
from math import trunc

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

#player dialogue
p_dial = {
    'intro': ['Top of the morning to you.', 'Let\'s finish this quickly.', 'Let\'s have a nice one.', 'This will end quickly.','Show me what you\'ve got.','Just bring it.'],
    'victory': ['This one was too easy.', 'Next.', 'It\'s over already?', 'Just don\'t show me your ugly mug ever again.'],
    'defeat': ['I guess this is it...', 'This one was a tad too strong for me.', 'It seems like this is the end.', 'You\'re a strong one.'],
    'dodge': ['Missed me.', 'Too bad.','Too fast for your eyes.']
}

#possible names for the enemies
enemy_names = ['Aamon', 'Abraxas', 'Satanael', 'Beelzebub', 'Berith', 'Gorgon', 'Lilith', 'Leviathan', 'Malphas', 'Mamom', 'Orobas', 'Paimon', 'Rahab', 'Tannin', 'Zagan']

#enemy dialogue
enemy_dial = {
    'Aamon': {'intro': 'I\'m not going easy on you.', 'victory': 'Too damn easy.', 'defeat': 'Good job on defeating me human', 'dodge': 'Too slow human.'},
    
    'Abraxas': {'intro': 'Bring it.', 'victory': '*silence*', 'defeat': 'How!?', 'dodge': 'Too slow.'},
    
    'Satanael': {'intro': 'Show me what you can do Human.', 'victory': 'Know your place.', 'defeat': 'How could this happen?', 'dodge': 'You\'ve gotta do better than that.'},
    
    'Beelzebub': {'intro': 'Let\'s have a good one dude.', 'victory': 'You were strong, let\'s fight again sometime.', 'defeat': 'I gotta hand it to ya, you\'re prety strong.', 'dodge': 'Missed me.'},
    
    'Berith': {'intro': 'Let\'s finish quickly so I can go back to sleep.', 'victory': 'Good, now I can go back to sleep.', 'defeat': 'Heh, now it\'s eternal sleep I guess.', 'dodge': 'You really are bad if you can\'t eat a sleepy target.'},
    
    'Gorgon': {'intro': 'I\'ll finish you quickly.', 'victory': 'You never stood a chance.', 'defeat': 'Impressive skills Human.', 'dodge': 'Hah, you fool.'},
    
    'Lilith': {'intro': 'Let\'s do this <3', 'victory': 'Oh, it\'s over :(', 'defeat': 'I wish we could\'ve kept going...', 'dodge': 'Missed me :P'},
    
    'Leviathan': {'intro': 'Let\'s have a good battle.', 'victory': 'It seems I am stronger.', 'defeat': 'You did well in defeating me.', 'dodge': 'You missed me.'},
    
    'Malphas': {'intro': 'Let\'s have a good fight :P', 'victory': 'Got ya!', 'defeat': 'Fuck!', 'dodge': 'You missed me bro.'},
    
    'Mamom': {'intro': 'Let\'s do this.', 'victory': 'You were too weak to challenge me.', 'defeat': 'I\'m ashamed of this outcome', 'dodge': 'Not good enough.'},
    
    'Orobas': {'intro': 'Yo!', 'victory': 'And it\'s done', 'defeat': 'Fucking Hell!', 'dodge': 'You fucking missed me!'},
    
    'Paimon': {'intro': 'Try to entertain me as much as you can', 'victory': 'Just like I thought you were shit.', 'defeat': 'It seems I was too careless.', 'dodge': 'Oy oy, you can\'t even hit me?'},
    
    'Rahab': {'intro': 'Let us start this fight to the death.', 'victory': 'Rest in peace.', 'defeat': 'Thank you for making me figth such a great last battle.', 'dodge': 'You missed me.'},
    
    'Tannin': {'intro': 'Let\'s do this!', 'victory': ' Yeah, I won!', 'defeat': 'Seems like I got careless.', 'dodge': 'Missed me dude!'},
    
    'Zagan': {'intro': 'Let\'s both go all out.', 'victory': 'Fuck yeah!!!', 'defeat': 'Fuck!', 'dodge': 'Where the fuck are you aiming?'}
}

#summary of each stage's stats
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

#visual HP bar 
def hp_bar_visual(hp, hp_now):
    #it looks like this '/----------\' when at full HP
    hp_bar = '/'
    if hp_now > hp: #this if is only used for when the player gets an overshield from using a Potion
        hp_bar += '-' * trunc(((hp/hp) * 10))
        ovrshild = trunc(((hp_now/hp) * 10) -  trunc(((hp/hp) * 10)))
        hp_bar += '+' * ovrshild
        # hp_bar += ' ' * (int() - ovrshild)
    else:
        hp_bar += '-' * trunc(((hp_now/hp) * 10))
        hp_bar += ' ' * (10 - trunc(((hp_now/hp) * 10)))
    hp_bar += '\\'
    return hp_bar
    
    
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
    stagex_max_health = stagex_health #this variable holds the maximum health of the enemy

    
    while player_stats['player_health'] > 0 and stagex_health > 0:
        #making sure it's possible to alter the following variables inside this function
        global stg_start
        global turn
        global fwrd
        global i
        
        #a simple starting message for each new stage
        if stg_start == True: #the following lines will only be executed in the 1st turn of each stage
            print()
            print('{}: {}'.format(stg_name, repr(enemy_dial[stg_name]['intro'])))
            print('{}: {}'.format(player_name, repr(choice(p_dial['intro']))))
            print('\n {}\'s health: {} \n {}\'s health: {}'.format(player_name, player_stats['player_health'], stg_name, stagex_health))
            # print("DEBUG")
            # print('x',x)
            # print('y',y)
            # print('health',stagex_health)
            # print("DEBUG")
            stg_start = False #makes sure only this IF condition is only True in the 1st turn of each stage
            print('{}\'s HP'.format(stg_name).rjust(69))
            print(hp_bar_visual(stagex_max_health, stagex_health).rjust(70))
            print('{}\'s HP'.format(player_name))
            print(hp_bar_visual(player_stats['player_max_health'], player_stats['player_health']))
            print()
        
        #message shown at the start of each turn:
        #prompts the user player for an action and outputs the current number of potions held
        print('Attack, use a Potion or Guard?')
        print('You currently have {} potions.'.format(player_stats['player_potions']))
        action = input('What are you gonna do?') #player input
        print()
        shuffle(dodge_rng) #shuffle the order of the items in dodge_rng
        
        if 'attack' in action.lower(): #player chooses attack
            #'attack' + enemy dodge
            if choice(dodge_rng) == 'dodge':
                print('{} dodged your attack!'.format(stg_name))
                print('{}: {}'.format(stg_name, repr(enemy_dial[stg_name]['dodge'])))
                shuffle(dodge_rng) #shuffle the order of the items in dodge_rng
                print()
            #'attack' 
            else: 
                #damage dealt by player
                stagex_damage = stagex_health - (stagex_health - player_stats['player_attack']) #damage done to the enemy
                stagex_health -= stagex_damage #subtract the damage from the enemy's health
                #output of damage dealt
                print('{} dealt {} damage to {}.'.format(player_name, stagex_damage, stg_name))
                player_stats['player_attack'] = randint(120,150)
                fwrd = input()
            
            #'attack' + enemy dies
            if stagex_health <= 0: #if enemy dies from player attack
                print()
                print('{} has been defeated.'.format(stg_name))
                print('{}: {}'.format(stg_name, repr(enemy_dial[stg_name]['defeat'])))
                print('{}: {}'.format(player_name, repr(choice(p_dial['victory'])))) #player victory dialogue
                print()
                print('Congratulations, you\'ve cleared stage {}!'.format(stg))
                i = True #makes sure the stage was a victory
                if stg == 10: #if player completes stage 10 aka last stage
                    i = False
            
            #enemy attacks
            if stagex_health > 0: 
                
                #enemy attacks + player dodge
                if choice(dodge_rng) == 'dodge': #if player dodges an attck
                    print('{} dodged {}\'s attack!'.format(player_name, stg_name))
                    print('{}: {}'.format(player_name, repr(choice(p_dial['dodge']))))
                    shuffle(dodge_rng) #shuffle the order of the items in dodge_rng
                    print()
                    
                #enemy attacks
                else: 
                    player_damage = player_stats['player_health'] - (player_stats['player_health'] - stagex_attack) #damage dealt to the player
                    player_stats['player_health'] -= player_damage #subtract the damage dealt by the enemy from the player's health
                    #outputs damage dealt by the enemy
                    print('{} dealt {} damage to you.'.format(stg_name, player_damage))
                    fwrd = input()
                    stagex_attack = randint(x,y) #reset the enemy's attack to a random value between x and y

                    #enemy attack + player dies
                    if player_stats['player_health'] <= 0: 
                        print()
                        print('{}: {}'.format(stg_name, repr(enemy_dial[stg_name]['victory'])))
                        print('{}: {}'.format(player_name, repr(choice(p_dial['defeat']))))
                        print('You\'ve been defeated by', stg_name, ', GAME OVER!')
                        print('In total, your attempt to clear this game lasted', turn,'turns.')
                        i = False #makes sure the stage was failed == player died
            
        #'potion'
        if 'potion' in action.lower(): #player chooses to use a potion
            
            #'potion' + player doesn't have potions
            if player_stats['player_potions'] == 0: #in case player doesn't have potions
                print()
                print('You currently don\'t have any potions.')
            
            #'potion' + player has at least 1 potion
            else: 
                player_stats['player_health'] += potion #heal player
                
                current_health = player_stats['player_health'] #variable used to calculate the overshield
                
                #overshield
                if player_stats['player_health'] > player_stats['player_max_health']:
                    overshield = current_health - player_stats['player_max_health']
                    #overshield = (current health) - (current max health)
                    print('You\'ve gained an overshield of', overshield, 'Health.' )
                    #output the overshield ammount
                overshield = 0 #resets the overshield to 0
                print('Current Health: {}'.format(current_health)) #output current ammount of health
                player_stats['player_potions'] -= 1 #remove 1 potion from the player inventory
                fwrd = input() #giving the player a chance to read all the outputs
                
                #'potion' + enemy attacks + player dodges
                if choice(dodge_rng) == 'dodge': #if player dodges the enemy attack
                    print('{} dodged {}\'s attack!'.format(player_name, stg_name))
                    print('{}: {}'.format(player_name, repr(choice(p_dial['dodge']))))
                
                #'potion' + enemy attacks
                else:
                    #enemy attacks the player
                    player_damage = player_stats['player_health'] - (player_stats['player_health'] - stagex_attack) #damage dealt to the player
                    player_stats['player_health'] -= player_damage #subtract the damage dealt by the enemy from the player's health
                    #outputs damage dealt by the enemy
                    print(stg_name, 'dealt', player_damage, 'damage to you.')
                    fwrd = input()
                    stagex_attack = randint(x,y) #reset the enemy's attack to a random value between x and y
    
                #'potion' + enemy attacks + player dies
                if player_stats['player_health'] <= 0: 
                    print()
                    print('{}: {}'.format(stg_name, repr(enemy_dial[stg_name]['victory']))) #enemy victory dialogue
                    print('{}: {}'.format(player_name, repr(choice(p_dial['defeat'])))) #player defeated dialogue
                    print('You\'ve been defeated by', stg_name, ', GAME OVER!')
                    print('In total, your attempt to clear this game lasted', turn,'turns.')
                    i = False #makes sure the stage was failed
        
        #'guard'
        if 'guard' in action.lower(): #player chooses to guard
            print('{} guarded against {}\'s next attack!'.format(player_name, stg_name)) #output an information confirming that the player guarded
            
            #'guard' + enemy attacks
            if stagex_health > 0: #if enemy is still alive
                        #enemy attacks the player
                        player_damage = player_stats['player_health'] - (player_stats['player_health'] - stagex_attack)
                        player_stats['player_health'] -= round(0.3 * player_damage) #if the player guarded then the enemy's attack will only deal 30% of it's original damage
                        #outputs damage dealt by the enemy
                        print(stg_name, 'dealt', round(0.3 * player_damage), 'damage to you.')
                        fwrd = input()
                        stagex_attack = randint(x,y) #reset the enemy's attack to a random value between x and y
    
                        #'guard' + enemy attacks + player dies
                        if player_stats['player_health'] <= 0: 
                            print()
                            print('{}: {}'.format(stg_name, repr(enemy_dial[stg_name]['victory']))) #enemy victory dialogue
                            print('{}: {}'.format(player_name, repr(choice(p_dial['defeat'])))) #player defeated dialogue
                            print('You\'ve been defeated by', stg_name, ', GAME OVER!')
                            print('In total, your attempt to clear this game lasted', turn,'turns.')
                            i = False #makes sure the stage was failed
            
        #end of turn: output player and enemy's HP bars, plus a ---New Turn--- visual queue
        if player_stats['player_health'] > 0 and stagex_health > 0:
            print('{}\'s HP'.format(stg_name).rjust(69))
            print(hp_bar_visual(stagex_max_health, stagex_health).rjust(70))
            print('{}\'s HP'.format(player_name))
            print(hp_bar_visual(player_stats['player_max_health'], player_stats['player_health']))
            print()
            print('---New Turn---')
        turn += 1 #add 1 to the number of turns since the start of the game

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
    quit_prompt = input('Do you wish to keep playing or do you wanna stop? (y/n)')
    if ('stop' in quit_prompt.lower()) or  ('no' in quit_prompt.lower()) or ('n' in quit_prompt.lower()):
        i = False #this means the next stage won't start and the game will end
    else:
        print('Then let\'s keep going!')
        fwrd = input()

stg = 1
i = True #variable to identify if a stage was cleared or failed == player died; starts as True to make the loop work; this variable will also be used to test if a player wants to keep playing after clearing a stage

while stg < 11: #while the player doesn't fail a stage or completes all stages
    
    stg_start = True #variable to indicate it's the first turn of a new stage, therefore execute the specific code
    #give a name to the enemy
    stg_name = choice(enemy_names) #choose a name from the list
    enemy_names.remove(stg_name) #remove the chosen name from the possible names list
    stage() #give the function stage() arguments of stage x's stats
    if i == False: #if the player lost then the loop terminates
        break
    stage_clear() #rewards from clearing a stage
    fwrd = input() #giving the player a chance to read all the outputs

    #test if the player wants to keep playing
    quit_game() 
    if i == False: #if it doesn't output the following message and terminate the loop
        print('You chose to quit the game. You\'ve managed to clear the game up to stage',stg)
        break
    stg += 1
    

#player completes the game (10 stages)
else: 
    print('Congratulations, you\'ve cleared all the stages, which means you\'ve completed the game!')
    print(player_name,'completed the game in', turn, 'turns.')
    print('Thank you very much for playing my very first game.')
    last_words = input('Any words of triumph to say? ')
    print('Everyone, remember the words the Hero said after victory:', repr(last_words))