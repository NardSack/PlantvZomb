#zombie when pass by acher .... archer still shoots zombie.##cannot place in A26 ####################............ also able to customise max threat level and number of kills to win

import random
import math
#dictionary
#ABC naming
columnname={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z',}
letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
r=5
c=7
#dictionary
game_vars = {
    'turn': 1,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }
#[field#,sub#,gamvar#,defenders,monsters]##[field#,PC#,gamvar#,defence,mon]
defender_list = ['blank','ARCHR', 'WALL','MINE','CANON']#'blank' to make sorting easier
monster_list = ['ZOMBI', 'WWOLF',
                'SKELE']
defenders = {'ARCHR':['Archer',#name
                       5,#maxhp
                       1,#min damage
                       4,#max damage
                       5,#price
                       8,#upgrade price
                       ],
             'WALL':['Wall',#name
                      20,#maxhp
                      0,#min damage
                      0,#max damage
                      3,#price
                      6,#upgrade price
                      ],
             'MINE':['Mine',#name
                      0,#maxhp
                      10,#min damage
                      10,#max damage
                      8,#price
                      0,#upgrade price
                      ],
             'CANON':['Cannon',#name
                      8,#maxhp
                      3,#min damage
                      5,#max damage
                      7,#price
                      0,#upgrade price
                      ]
            }

monsters = {'ZOMBI': [ 'Zombie',#name
                      15,#maxhp
                       3,#min damage
                      6,#max damage
                      1,#moves
                      2#reward
                      ],

            'WWOLF': ['Werewolf',#name
                      10,#maxhp
                      1,#min damage
                      4,#max damage
                      2,#moves
                      3#reward
                      ],
            'SKELE':['Skeleton',#name
                      10,#maxhp
                      1,#min damage
                      3,#max damage
                      1,#moves
                      5#reward
                      ],
            }
deflong=[]#long name for defenders
monlong=[]#long name for monsters
for name in defenders:
    deflong.append(defenders.get(name)[0])
for name in monsters:
    monlong.append(monsters.get(name)[0])


#num=[count]
#parameters of field
def starting_field(r,c):
    field = []
    sub=[]
    box=[]
    
    for C in range(0,r):
        for N in range(0,c):
            sub.append(None)
        sub.insert(0,[C+1])
        
        field.append(sub)
        sub=[]
        
       #name, health, placement in row
        # field = [[[1], ['ARCHR', 5, 1], None, None, None, None, None,]
        #['WWOLF', 10, 7]], [[2], None, None, None, None, None, None, None],
        #[[3], None, None, None, None, None, None,]
        #['WWOLF', 10, 7]], [[4], None, None, None, None, None, None, None],
        #[[5], None, None, None, None, None, None, None]]
    return field

#making sure reply is 1,2,3
def show_main_menu():
    print('Desperate Defenders\n-------------------\nDefend the city from undead monsters!\n')
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")
    while True:
        choice=input('your choice ? ')
        if choice.isdigit() == True and int(choice) in range(1,4) :
            choice=int(choice)
            break
        else:
            print('Please enter option 1,2,3')
            
    return choice
#parameters for new game
def start_new(r,c,game_vars,defenders,monsters):
    success=0

    while True:
        if r==5 and c==7:
            print('1.Default field    2.Customise field')
            ans=(input('choice ? '))
            if ans.isdigit():
                ans=int(ans)
            else:
                continue
        else:
            field=starting_field(r,c)
        if ans not in range(1,3):#if choice not 1 or 2
            print('Please enter either 1 or 2')
            continue
            
        if ans == 1:
            field=starting_field(r,c)
            sub=3+1#plus one cause of going until excule the value
            break
        elif ans==2:
            while True:
                r=input('number of rows : ')
                c=input('number of column : ')
                sub=input('number of playable columns : ')
                threat=input('Threat meter (when threat meter full new monster spawns): ')
                target=input('How many monster kill to win : ')
                if r.isdigit() and c.isdigit()and sub.isdigit() and int(sub)<=int(c) and threat.isdigit()and target.isdigit():
                    if int(r)<=26:
                        r=int(r)
                        c=int(c)
                        sub=int(sub)+1
                        threat=int(threat)
                        target=int(target)
                        game_vars['monster_kill_target']=target
                        game_vars['max_threat']=threat
                        field=starting_field(r,c)
                        success=1
                        break
                    else:
                        print('max rows is 26 and that play columns is less than or equal to number of column\n Pls re-enter again')
                else:
                    print('Try again')
                    continue
            if success==1:
                break
    gamvar=[]
    for unit in game_vars:
        gamvar.append(game_vars.get(unit))
    defence=[]
    for unit in defenders:
        defence.append(defenders.get(unit))
    mon=[]
    for unit in monsters:
        mon.append(monsters.get(unit))
    
    return [field,sub,gamvar,defence,mon]
#parameter for loaded game#
def load_save(deflong,monlong):
    field=[]
    #\n counts as 1 position not 2
    data=open('datafield.txt','r')
    for line in data :
        
        #playable col
        if line[:2]=='PC':
            PC=line[2:-1]
            
        #game variable
        elif line[:2]=='va':
            line=line[2:-1].split(',')
            count=0
            for unit in line:
                if unit.isdigit():
                    line[count]=int(unit)
                count+=1
            gamvar=line
            
        #field
        elif line[:2]=='1m':
            line=line.split(' n,')
            print()
            #print(line)
            for row in line:
                row=row.split(',')
                rowfield=[]
                for unit in row:
                    
                    unit=unit.split('m')
                    
                    if unit[-1]=='':
                        unit=unit[:-1]
                    if unit ==['None']:
                        unit='None'
                    #print(unit)
                    count=0
                    for letter in unit:
                        
                        if letter.isdigit():
                            unit[count]=int(letter)
                        count+=1
                    #print(unit)
                    if unit == 'None':
                        rowfield.append(None)
                    else:
                        rowfield.append(unit)
                field.append(rowfield)
            
        else:
            
            line=line[:-1]
            line=line.split('.')
            subline=[]
            for unit in line:
                unit=unit.split(',')
                count=0
                for letter in unit:
                    if letter.isdigit():
                        unit[count]=int(letter)
                    count+=1
                subline.append(unit)
            line=subline
            
            
            if line[0][0] in deflong:
                defence=line
                
            elif line[0][0] in monlong:
                mon=line
                
      
    
    return [field,PC,gamvar,defence,mon] 
#quit   
def quit():
    print('See You next time')
    return 0

#save game ####### ##########################################
def save_game(field,PC,game_vars,defenders,monsters):
    total= ''
    playable='PC'+str(PC)+'\n'
    turn=str(game_vars.get('turn'))+','
    montar=str(game_vars.get('monster_kill_target'))+','
    monkill=str(game_vars.get('monsters_killed'))+','
    nummon=str(game_vars.get('num_monsters'))+','
    gold=str(game_vars.get('gold'))+','
    threat=str(game_vars.get('threat'))+','
    maxthreat=str(game_vars.get('max_threat'))+','
    danger=str(game_vars.get('danger_level'))
    newgame='va'+turn+montar+monkill+nummon+gold+threat+maxthreat+danger+'\n'
    defend=''
    #defender list
    for unit in defenders:
        x=''
        for data in range(0,len(defenders.get(unit))):
            Z=str(defenders.get(unit)[data])+','
            x+=Z
        x=x[:-1]
        defend+=x+'.'
    defend=defend[:-1]+'\n'
    
    #monster list
    monster=''
    for unit in monsters:
        x=''
        for data in range(0,len(monsters.get(unit))):
            Z=str(monsters.get(unit)[data])+','
            x+=Z
        x=x[:-1]
        monster+=x+'.'
    monster=monster[:-1]+'\n'
    
    #field list
    for line in field:
        for word in line:
            newword=''
            if word != None:
                for unit in word:
                    newword+=str(unit)+'m'
            else:
                newword='None'
            total+=newword+','
        total=total[:-1]
        total+=(' n,')
    total=total[:-3]
    

    data=open('datafield.txt','w')
    data.write(playable)#playable column
    data.write(newgame)#variable
    data.write(defend)#defender
    data.write(monster)#monster
    data.write(total)#field
    data.close
######Total takes only one line
   

    print('Game Saved')

#draw board
    
def board(field,c,PC):
    count=0
    #variable of range can change
    for word in range(0,PC):
        if count==0:
            print(f'{"":^7}',end='')
        else:
            
            print(f'{count:^7}',end='')
        count+=1
    print()
    for data in field:
        print('      ',end='')
        for word in range(1,len(data)):
            print(f'+------',end='')
        print('+')
        for word in data:
            #need to use dictionary
            if word==None or word=='None':
                word= ''
            elif word[0] in columnname:#dic
                word=columnname.get(word[0])
            else:
                word=word[0]
                
            print(f'{word:^6}',end='|')
        print()
        for word in data:
            #need to use dictionary
            if word==None:
                word= ''
            elif word[0] in columnname:#dic
                word=''
            elif word=='D':
                word=''
            elif word[0] in defender_list or  monster_list:
                if word[0] in defender_list:
                    maxi=defenders.get(word[0])[1]
                else:
                    maxi=monsters.get(word[0])[1]
                word=word[1]
                if maxi > 0:
                    print(f'{word:>3}/{maxi:^2}',end='|')#(current health / max health)
                else:
                    print(f"{'':^6}",end='|')#(current health / max health) for the mine
            if word=='':
                print(f'{word:^6}',end='|')
        print()
    #variable of range can change
    print('      ',end='')
    for data in range(1,c):
        print(f'+------',end='')
    print('+')

#gameaction
#add a comfirm screen
def gameact():#need to add math but cannot do it here
    print(f"{'Turn':<8}{game_vars.get('turn')}",end='  ')
    print(f"{'Threat':<8}",end='')
    draw='-'*game_vars.get('threat')
    print(f"=[{draw}",end='')
    space=' '*(game_vars.get('max_threat')-game_vars.get('threat'))
    print(f"{space}]",end='  ')
    print(f"{'Danger Level':<8} {game_vars.get('danger_level')}")
    print(f"{'Gold':<4}={game_vars.get('gold')}",end='  ')
    print(f"{'Monster killed':<8} {game_vars.get('monsters_killed')}/{game_vars.get('monster_kill_target')}",end='')
    
    print()
    while True:
        count=0
        print('1. Buy unit        2. End turn')
        count+=1
        print('3. Save game       4. Quit')
        count+=1
        print(f'5. Upgrade Unit    6. Heal/Repair (5 Gold)')
        count+=1
        action=input('Your choice? ')
        if action.isdigit() and int(action)<= (count*2):
            action=int(action)
            break
        else:
            print('try again')
    
    return action

def buyunit():
    while True:
        print('What unit do you wish to buy? ')
        num=1
        for word in defender_list[1:]:
            print(num,end='  ')
            print(word,end='  ')
            dic=defenders.get(word)
            price=dic[4]
            print(f'({price}Gold)')
            num+=1
        print(num,end="  Don't buy\n")
        choice=input('your choice ? ')
        if choice.isdigit() and int(choice) <= num:
            choice=int(choice)
            break
        else:
            print('Try Again')
    return choice

def upgradeunit():######################################################################
    while True:
        print('What unit do you wish to upgrade? ')
        num=1
        for word in defender_list[1:]:
            print(num,end='  ')
            print(word,end='  ')
            dic=defenders.get(word)
            price=dic[5]
            print(f'({price} Gold)')
            num+=1
        print(num,end="  Don't upgrade\n")
        choice=input('your choice ? ')
        if choice.isdigit() and int(choice) <= num:
            choice=int(choice)
            break
        else:
            print('Try Again')
    return choice

#Spawn creep
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list,c):
    num=random.randrange(0,len(monster_list))
    unit=monster_list[num]
    #monster_zombie
    monster_health =monsters.get(unit)[1]
    monster_unit = [unit,monster_health,c-1]

    #monster_spawn_position
    while True:
        row = random.randrange(0, len(field))
        if field[row][c-1] != None:
            continue
        else:
            field[row][c-1] = monster_unit
            break
    return field
#coding that is running to for the program to start
#######make a function for one complete turn and then just while loop [might as well restart]
def choosing(choice,r,c,deflong,monlong,game_vars,defenders,monsters):
    if choice==1:
        ans=start_new(r,c,game_vars,defenders,monsters)
        

    elif choice == 2:
        ans=load_save(deflong,monlong)

    elif choice == 3:
        ans=exit()
        
    return ans#[field,sub,game_vars,defenders,monsters]##[field,PC,gamvar,defence,mon]
#-----------------------------------------------------------
reply=show_main_menu()
#if reply==2: ####for game variable [can also put for the number of playable squares]

choosemain=choosing(reply,r,c,deflong,monlong,game_vars,defenders,monsters)#[field,PC,game_vars,defenders,monsters]

if choosemain==0:
    print('See You Next time')
else:
    field=choosemain[0]
    #playable columns
    PC=int(choosemain[1])
    gamno=0#for the for loop
    #################################################################################################
    for num in game_vars:
        game_vars[num]=choosemain[2][gamno]
        gamno+=1
    gamno=0
    for unit in defenders:
        defenders[unit]=choosemain[3][gamno]
        gamno+=1
    gamno=0
    for unit in monsters:
        monsters[unit]=choosemain[4][gamno]
        gamno+=1
        
    for data in field :
        c=len(data)
        break
    
#------------------------------------------------------------
r=len(field)
#r = number of rows in field
#c = number of columns including Letters
win=0

while win ==0:
    monnumber=0
    #need to make it so only when no mosnter then will spawn new ##################################################################################
    for row in field :
        for unit in row:
            
            if unit != None and unit[0] in monsters:
                monnumber+=1
    game_vars['num_monsters']=monnumber
    #print(monsters)##############################################################################for testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingvfor testing
    #print(field)#########################################################################################for testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testing

    if game_vars.get('num_monsters') == 0:
        field=spawn_monster(field, monster_list,c)
    
    board(field,c,PC)
    action=gameact()
    #---------------------------------------------------------------
    #buy
    
    if action== 1:
        choice=buyunit()
        if choice == len(defender_list):
            
            continue
        else:
            unit=defender_list[choice]#'ARCHR'
            if game_vars.get('gold')<defenders.get(unit)[4]:
                print(f'Insufficient gold to purchase {defenders.get(unit)[0]}')
                continue
            else:
                success=0
                while success<2:
                    location=input('Place where ? ')
                    #print(PC)
                    #print(len(str(PC)))
                    if len(location)not in range(1,2+len(str(PC))):###############################################################################################
                        print('please use correct format')
                        continue
                    cap=location[0].upper()
                     
                    if cap not in letters:
                        
                        A=0
                    else:################# what if letters larger than field area
                    
                        count=0
                        for word in columnname:#numbers
                            if columnname.get(word) == cap:
                                break
                            else:
                                count+=1
                        if count > r:
                            A=0
                        else:
                            A=1
                    
                        #count is which row in the field
                    if location[1:].isdigit() and int(location[1:]) <= PC-1:
                        place=int(location[1:])
                        #place is which column of the field
                        B=1
                        
                    else:
                        B=0
                    #print(A)
                    #print(B)
                    success=A+B
                    
                        
                    if success<2:
                        print('Invalid Input')
                        print('Try again')
                        continue
                    if field[count][place]!= None and success == 2:
                        success=0
                        print('Space is occupied')
                        print('Try again')
            ###need to find a way to replace in list
                alive=1
                field[count][place]=[unit,defenders.get(unit)[1],place,alive]
                game_vars['gold']=game_vars.get('gold')-defenders.get(unit)[4]
    elif action == 2:#end turn
        count=1
        for row in field: #row =[[1], None, None, None, None, None, None, None]
            arrow=0
            position=0
            
            new_mon_in_row = []
            alldefinrow=[]
            for pos in range(len(row)):
                if row[pos] != None and row[pos][0] in monster_list:
                    
                    new_mon_in_row.append(row[pos])
                if row[pos] != None and row[pos][0] in defender_list:
                    alldefinrow.append(row[pos])
            
            if len(alldefinrow) != 0:
                KO=0
                for unit in alldefinrow:#unit=['ARCHR', 5, 1,1]
                    #print(unit)#############################.
                    if unit[0] == 'ARCHR':
                        arrows=str(random.randrange(defenders.get(unit[0])[2],defenders.get(unit[0])[3]+1))+unit[0]#archer in string
                    elif unit[0] == 'CANON':#not archer CANON
                        if unit[3]%2==0:
                            
                            arrows=str(random.randrange(defenders.get(unit[0])[2],defenders.get(unit[0])[3]+1))+unit[0] #not archer in string
                            knockback=random.randrange(0,2)
                            #knockback=1#################################for testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testing
                        else:
                            arrows = 0
                            
                    else:
                        arrows = 0
                    #print(arrows)
                
                    if len(new_mon_in_row)!=0 and unit[0] != 'WALL' and unit[0] != 'MINE' and unit[2] <new_mon_in_row[0][2] and arrows!=0:# damge when there is monsters in row
                        if new_mon_in_row[0][0]=='SKELE' and unit[0]=='ARCHR':
                            arrows=float(arrows[0])/2
                            #print(arrows)
                            #print(type(arrows))
                            #print(new_mon_in_row[0][1])
                            #print(type(new_mon_in_row[0][1]))
                            new_mon_in_row[0][1]=float(new_mon_in_row[0][1])-arrows###########################
                        elif unit[0]=='CANON':
                            arrows=int(arrows[0])
                            new_mon_in_row[0][1]=new_mon_in_row[0][1]-arrows
                            if knockback == 1 and row[new_mon_in_row[0][2]+1]== None and new_mon_in_row[0][1] > 0:
                                print(f'{new_mon_in_row[0][0]} in lane {columnname.get(row[0][0])} has been knock back')
                                #print(new_mon_in_row[0][2])
                                new_mon_in_row[0][2]=new_mon_in_row[0][2]+1
                                KO=10
                        else:
                            arrows=int(arrows[0])
                            new_mon_in_row[0][1]=new_mon_in_row[0][1]-arrows
                        print(f'{unit[0]} in lane {columnname.get(row[0][0])} shoots {new_mon_in_row[0][0]} for {arrows} damage !')
                        ###############################KNOCK back how much############################################

                        
                        if new_mon_in_row[0][1] <= 0:# removing of monsters when dies
                            print(f'{new_mon_in_row[0][0]} dies !')
                            gold=game_vars.get('gold')
                            #print(row[new_mon_in_row[0][2]])
                            print(f'You gain {monsters.get(row[new_mon_in_row[0][2]][0])[5]} gold as a reward')
                            game_vars['threat']+=monsters.get(row[new_mon_in_row[0][2]][0])[5]
                            game_vars['gold']=gold+monsters.get(row[new_mon_in_row[0][2]][0])[5]
                            row[new_mon_in_row[0][2]]=None
                            new_mon_in_row.remove(new_mon_in_row[0])
                            KO=0
                            # things got after kill monster
                            game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                            
                    elif len(new_mon_in_row)!=0 and unit[0] != 'WALL' and unit[0] != 'MINE' and unit[2] > new_mon_in_row[0][2] and arrows!=0:#damage when monster behind defender
                        count=0
                        for mon in new_mon_in_row:
                            if unit[2] < mon[2]:
                                if new_mon_in_row[0][0]=='SKELE' and unit[0]=='ARCHR':
                                    arrows=float(arrows[0])/2
                                    new_mon_in_row[count][1]=float(new_mon_in_row[count][1])-arrows################################
                                elif unit[0]=='CANON':
                                    arrows=int(arrows[0])
                                    new_mon_in_row[count][1]=new_mon_in_row[count][1]-arrows
                                    if knockback == 1 and row[new_mon_in_row[count][2]+1]== None and new_mon_in_row[0][1] > 0:
                                        print(f'{new_mon_in_row[count][0]} in lane {columnname.get(row[0][0])} has been knock back')
                                        #print(new_mon_in_row[count][2])
                                        new_mon_in_row[count][2]=new_mon_in_row[count][2]+1
                                        KO=10
                                else:
                                    arrows=float(arrows[0])
                                    new_mon_in_row[count][1]=new_mon_in_row[count][1]-arrows
                                print(f'{unit[0]} in lane {columnname.get(row[0][0])} shoots {new_mon_in_row[0][0]} for {arrows} damage !')
                                
                                    
                            count+=1
                            
                        if new_mon_in_row[0][1] <= 0:# removing of monsters when dies
                            print(f'{new_mon_in_row[0][0]} dies !')
                            print(f'You gain {monsters.get(row[new_mon_in_row[0][2]][0])[5]} gold as a reward')
                            gold=game_vars.get('gold')
                            game_vars['threat']+=monsters.get(row[new_mon_in_row[0][2]][0])[5]
                            game_vars['gold']=gold+monsters.get(row[new_mon_in_row[0][2]][0])[5]
                            row[new_mon_in_row[0][2]]=None
                            new_mon_in_row.remove(new_mon_in_row[0])
                            KO=0
                            
                            # things got after kill monster
                           
                            game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                    unit[3]+=1
                for unit in new_mon_in_row:###############
                    if KO ==10:
                       # print(row[unit[2]-1])
                        row[unit[2]-1]=None
                        row[unit[2]]=unit
                        #print(row[unit[2]])
                    else:
                        row[unit[2]]=unit
                
                
                        
                

            #whenever there is a defender left to right... 
            for unit in row:#None or ['Achr',5,7]_______________________________________________________________________________________________
                if unit != None and unit[0] in monsters:
                    re=0
                    count=row[0][0]
                    #print(count,'count begin')
                    #print(row[unit[2]])     ['ARCHR',5,3col,0] row=[None,None,None,None,None,None,None,['ARCHR',5,3,0]]
                    while re < monsters.get(unit[0])[4]:#monster move
                        
                        if row[unit[2]-1]== None:
                            
                            row[unit[2]-1]=unit
                            row[unit[2]]=None
                            unit[2]=unit[2]-1
                            
                            print(f'{unit[0]} in lane {columnname.get(row[0][0])} advances !')
                        elif row[unit[2]-1][0] in defenders and row[unit[2]-1][0] != 'MINE':#[defenders] but not mines
                            maxdmg=monsters.get(unit[0])[3]
                            mindmg=monsters.get(unit[0])[2]
                            damage=random.randrange(monsters.get(unit[0])[2],monsters.get(unit[0])[3]+1)
                            currenthp=row[unit[2]-1][1]
             
                            row[unit[2]-1][1]=currenthp-damage
                            
                            print(f'{unit[0]} in lane {columnname.get(row[0][0])} hits {defenders.get(row[unit[2]-1][0])[0]} for {damage} damage ! ')
                            if row[unit[2]-1][1] <= 0:
                                row[unit[2]-1]=None
                        elif row[unit[2]-1][0] == 'MINE':#unit[2]-1 = 5 from ['Achr',5,7] -1
                            row[unit[2]-1]=[row[unit[2]-1]]+[[unit[0],unit[1],unit[2]-1]]
                            row[unit[2]]=None
                            #print(row[unit[2]-1])
                
                        elif row[unit[2]-1][0] in monsters:
                            print(f'{unit[0]} in lane {columnname.get(row[0][0])} is blocked from advancing.')
                    #############################################################
                        ## mine problem
##                        print(unit,'unit[2]')
##                        print(unit[2])
                        if unit[2]==1:#unit= ['SKELE', 8.0, 6] move already
                            #unit[2] = monster step
                            break
                    
                            
                            
##                            print(count,'count end')
                        re+=1
##                    print('break....gg')
        for row in field:
            for unit in row:
                if unit != None and len(unit)==2:
                    count=row[0][0]# number fo da row
##                    print(unit)
##                    print(count)
##                    print(row)
                    if unit[0][0]=='MINE':#[name,health,pos,alive turns]
                                #print('yay1')
                                #print(unit[2])
                                    
                                    
                                place=unit[0][2]# place in column
                                    #print('yay2')
        ##                            print(place,'place')
        ##                            print(count,'count')
        ##                            print(len(field),'len')
        ##                            print(field)
        ##                            print(field[count-1][place])
                                    #print(field[count-1][place-1],end='yay3 \n')###########wall not mine
                                    #if field[count-1][place][0][1] == 'MINE' and  field[count-1][place][1][1] in monster_list:
                                        
                                if 0<=count-1 <=len(field)-1 and field[count-1][place+2]!= None and  field[count-1][place+2][0] in monsters :
                                    field[count-1][place-1][1]=field[count-1][place-1][1]-10
                                        #print(field[count-1][place-1])
                                    if field[count-1][place-1][1]<=0:
                                        print(f'{field[count-1][place-1][0]} in lane {columnname.get(count)} dies')
                                        print(f'You gain {monsters.get(field[count-1][place+2][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count-1][place+2][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count-1][place+2][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count-1][place-1]=None
                                    
                                    #print(field[count-1][place])
                                    #print(count)
                                    #print(len(field))
                                if 0<=count-1 <=len(field)-1 and field[count-1][place]!= None and  field[count-1][place][1][0] in monsters:
                                    field[count-1][place][1][1]=field[count-1][place][1][1]-10
                                        #print(field[count-1][place])
                                        #print('no')
                                    if field[count-1][place][1][1]<=0:
                                        print(f'{field[count-1][place][1][0]} in lane {columnname.get(count)} dies')
                                        print(f'You gain {monsters.get(field[count-1][place][1][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count-1][place][1][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count-1][place][1][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count-1][place]=None
                                            #print('yaya')
                                    else:
                                            #print('ya')
                                        field[count-1][place]=field[count-1][place][1]
                                    
                                    #print(field[count-1][place])
                                    #print(field[count-1][place+1])
          
                                if 0<=count-1 <=len(field)-1 and field[count-1][place+1]!= None and  field[count-1][place+1][0] in monsters:
                                    field[count-1][place+1][1]=field[count-1][place+1][1]-10
                                    #print(field[count-1][place+1])
                                    if field[count-1][place+1][1]<=0:
                                        print(f'{field[count-1][place+1][0]} in lane {columnname.get(count)} dies')
                                        print(f'You gain {monsters.get(field[count-1][place+1][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count-1][place+1][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count-1][place+1][0])[5]
                                
                                        # things got after kill monster
                               
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count-1][place+1]=None
                                    
                                    


                                if 0<=count<len(field)-1 and field[count][place-1]!= None and  field[count][place-1][0] in monsters:
                                    field[count][place-1][1]=field[count][place-1][1]-10
                                    #print(field[count][place-1])
                                    if field[count][place-1][1]<=0:
                                        print(f'{field[count][place-1][0]} in lane {columnname.get(count+1)} dies')
                                        print(f'You gain {monsters.get(field[count][place-1][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count][place-1][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count][place-1][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count][place-1]=None
                                    
                                    #print(field[count][place])
                                   # print('yat')
                                    #print(count)

                                #print(field[count][place],'real?')
                                if 0<=count<len(field)-1 and field[count][place]!= None and  field[count][place][0] in monsters:
                                    field[count][place][1]=field[count][place][1]-10
                                        #print('yat')
                                        #print(field[count][place])
                                    if field[count][place][1]<=0:
                                        print(f'{field[count][place][0]} in lane {columnname.get(count+1)} dies')
                                        print(f'You gain {monsters.get(field[count][place][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count][place][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count][place][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count][place]=None
                                    else:
                                            #print(field[count][place][1])
                                        field[count][place]=field[count][place][1]
                                    
                                    #print(field[count][place+1])

                                if 0<=count<=len(field)-1 and field[count][place+1]!= None and  field[count][place+1][0] in monsters:
                                    field[count][place+1][1]=field[count][place+1][1]-10
                                    #print(field[count][place+1])
                                    if field[count][place+1][1]<=0:
                                        print(f'{field[count][place+1][0]} in lane {columnname.get(count+1)} dies')
                                        print(f'You gain {monsters.get(field[count][place+1][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count][place+1][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count][place+1][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count][place+1]=None
                                    
                                    #print(field[count+1][place-1])
                                    
                                    
                                if 0<=count-2<=len(field)-1 and field[count-2][place-1]!= None and  field[count-2][place-1][0] in monsters:
                                    field[count-2][place-1][1]=field[count-2][place-1][1]-10
                                        #print(field[count+1][place-1])
                                    if field[count-2][[place-1]][1]<=0:
                                        print(f'{field[count-2][[place-1]][0]} in lane {columnname.get(count+2)} dies')
                                        print(f'You gain {monsters.get(field[count-2][[place-1]][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count-2][[place-1]][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count-2][[place-1]][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count-2][[place-1]]=None
                                    
                                    #print(field[count+1][place])
                                            


                                if 0<=count-2<=len(field)-1 and field[count-2][place]!= None and  field[count-2][place][0] in monsters:
                                    field[count-2][place][1]=field[count-2][place][1]-10
                                        #print(field[count+1][place])
                                        #print(f'yay{columnname.get(count+2)}')
                                    if field[count-2][place][1]<=0:
                                        print(f'{field[count-2][place][0]} in lane {columnname.get(count+2)} dies')
                                        print(f'You gain {monsters.get(field[count-2][place][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count-2][place][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count-2][place][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count-2][place]=None
                                    
                                    #print(field[count+1][place+1])

                                if 0<=count-2<=len(field)-1 and field[count-2][place+1]!= None and  field[count-2][place+1][0] in monsters:
                                    field[count-2][place+1][1]=field[count-2][place+1][1]-10
                                        #print(field[count+1][place+1])
                                    if field[count-2][place+1][1]<=0:
                                        print(f'{field[count-2][place+1][0]} in lane {columnname.get(count+2)} dies')
                                        print(f'You gain {monsters.get(field[count-2][place+1][0])[5]} gold as reward')
                                        gold=game_vars.get('gold')
                                        game_vars['threat']+=monsters.get(field[count-2][place+1][0])[5]
                                        game_vars['gold']=gold+monsters.get(field[count-2][place+1][0])[5]
                                    
                                            # things got after kill monster
                                   
                                        game_vars['monsters_killed']=game_vars.get('monsters_killed')+1
                                        field[count-2][place+1]=None
##                                field[count-2][place+1]='D'
##                                field[count-2][place]='D'
##                                field[count-2][place-1]='D'
##                                field[count][place+1]='D'
##                                field[count][place]='D'
##                                print(count,'count')
##                                field[count][place-1]='D'
##                                field[count-1][place+1]='D'
##                                field[count-1][place-1]='D'
##                                field[count-1][place]='D'


        game_vars['turn']+=1
        game_vars['gold']+=1
        game_vars['threat']+=random.randrange(1,game_vars['danger_level']+1)
        print('You have gain 1 gold for this turn')
        if game_vars.get('turn')%12==0:#increase in monster stat
            print('The evil grows stronger')
            game_vars['danger_level']+=1
            for unit in monsters:
                monsters.get(unit)[1]+=1
                monsters.get(unit)[2]+=1
                monsters.get(unit)[3]+=1
                monsters.get(unit)[5]+=1
        while game_vars.get('threat') >= game_vars.get('max_threat'):
            game_vars['threat']=game_vars.get('threat')-game_vars.get('max_threat')
            field=spawn_monster(field, monster_list,c)
        #field=spawn_monster(field, monster_list,c)########################################################################for testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testingfor testing
        count+=1
#####################################################################################################################################################################################################          
        
    elif action == 3:#save field
        save_game(field,PC,game_vars,defenders,monsters)
        
    elif action == 4:#quit
        print('See you next time!')
        win = 1
    #upgrade units
    elif action == 5:#Upgrade Unit
        choice=upgradeunit()
        if choice == len(defender_list):
            
            continue
        else:
            unit=defender_list[choice] #archr
            if game_vars.get('gold')<defenders.get(unit)[5]:
                print(f'Insufficient gold to upgrade {defenders.get(unit)[0]}')
                continue
            elif defenders.get(unit)[5] == 0:
                print(f'{defenders.get(unit)[0]} not avaiable for upgrade')
                continue
            else:
                if unit == 'ARCHR':
                    defenders.get(unit)[5]+=2
                    defenders.get(unit)[1]+=1
                    defenders.get(unit)[2]+=1
                    defenders.get(unit)[3]+=1
                elif unit == 'WALL':
                    defenders.get(unit)[1]+=5
    elif action == 6:#Heal / Repair
        if game_vars.get('gold')< 5:
            print(f'Insufficient gold to use Heal')
        else:
            success=0
            while success<2:
                location=input('Place where ? ')
                if len(location)!= 2:
                    print('please use correct format')
                    continue
                cap=location[0].upper()
                     
                if cap not in letters:
                        
                    A=0
                else:################# what if letters larger than field area
                    
                    count=0
                    for word in columnname:#numbers
                        if columnname.get(word) == cap:
                            break
                        else:
                            count+=1
                    if count > r:
                        A=0
                    else:
                        A=1
                    
                    #count is which row in the field
                if location[1].isdigit() and int(location[1]) <= PC-1:
                    place=int(location[1])
                    #place is which column of the field
                    B=1
                        
                else:
                    B=0
                    
                success=A+B
                    
                        
                if success<2:
                    print('Invalid Input')
                    print('Try again')
            if count<=len(field)and field[count-1][place-1]!= None and  field[count-1][place-1][0] in defenders:
                field[count-1][place-1][1]=field[count-1][place-1][1]+5
                #defenders.get(field[count-1][place-1][0])[1] === max health of unit
                if field[count-1][place-1][1] > defenders.get(field[count-1][place-1][0])[1]:
                    field[count-1][place-1][1]=defenders.get(field[count-1][place-1][0])[1]
        #

            if count<=len(field)and  field[count-1][place]!= None and  field[count-1][place][0] in defenders:
                field[count-1][place][1]=field[count-1][place][1]+5
                #print(defenders.get(field[count-1][place])[1])
                if field[count-1][place][1] > defenders.get(field[count-1][place][0])[1]:
                    field[count-1][place][1]=defenders.get(field[count-1][place][0])[1]
        #

            if count<=len(field)and field[count-1][place+1]!= None and  field[count-1][place+1][0] in defenders:
                field[count-1][place+1][1]=field[count-1][place+1][1]+5
                #print(defenders.get(field[count-1][place+1])[1])
                if field[count-1][place+1][1] > defenders.get(field[count-1][place+1][0])[1]:
                    field[count-1][place+1][1]=defenders.get(field[count-1][place+1][0])[1]
        #

            if count<=len(field)and field[count][place-1]!= None and  field[count][place-1][0] in defenders:
                field[count][place-1][1]=field[count][place-1][1]+5
                #print(defenders.get(field[count][place-1])[1])
                if field[count][place-1][1] > defenders.get(field[count][place-1][0])[1]:
                    field[count][place-1][1]=defenders.get(field[count][place-1][0])[1]
        #

            if count<=len(field)and field[count][place]!= None and  field[count][place][0] in defenders:
                field[count][place][1]=field[count][place][1]+5
                #print(defenders.get(field[count][place])[1])
                if field[count][place][1] > defenders.get(field[count][place][0])[1]:
                    field[count][place][1]=defenders.get(field[count][place][0])[1]
        #

            if count<=len(field)and field[count][place+1]!= None and  field[count][place+1][0] in defenders:
                field[count][place+1][1]=field[count][place+1][1]+5
                #print(defenders.get(field[count1][place+1])[1])
                if field[count][place+1][1] > defenders.get(field[count][place+1][0])[1]:
                    field[count][place+1][1]=defenders.get(field[count][place+1][0])[1]
        #

            if count<=len(field)and field[count+1][place-1]!= None and  field[count+1][place-1][0] in defenders:
                field[count+1][place-1][1]=field[count+1][place-1][1]+5
                #print(defenders.get(field[count+1][place+1])[1])
                if field[count+1][place-1][1] > defenders.get(field[count+1][place-1][0])[1]:
                    field[count+1][place-1][1]=defenders.get(field[count+1][place-1][0])[1]
        #


            if count<=len(field)and field[count+1][place]!= None and  field[count+1][place][0] in defenders:
                field[count+1][place][1]=field[count+1][place][1]+5
                #print(defenders.get(field[count+1][place])[1])
                if field[count+1][place][1] > defenders.get(field[count+1][place][0])[1]:
                    field[count+1][place][1]=defenders.get(field[count+1][place][0])[1]
        #


        #

            if count<=len(field)and field[count+1][place+1]!= None and  field[count+1][place+1][0] in defenders:
                field[count+1][place+1][1]=field[count+1][place+1][1]+5
                #print(defenders.get(field[count+1][place+1])[1])
                if field[count+1][place+1][1] > defenders.get(field[count+1][place+1][0])[1]:
                    field[count+1][place+1][1]=defenders.get(field[count+1][place+1][0])[1]
            
            game_vars['gold']-=5
        
    if game_vars['monsters_killed']==game_vars['monster_kill_target']:
        win = 1
    for row in field:
        if row[1]!= None and row[1][0] in monsters:
            print('You Lose!')
            board(field,c,PC)
            print('Showing final board')
            win=1
            break
if win == 1:
    exit()
