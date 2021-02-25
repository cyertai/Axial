#enemy collision
#update readme
#update timesheet
#update writeup


from Tkinter import *
#import pygame
#from pygame.locals import *
import time
import string
#import winsound
import random
import sys
import math

##########################################################################
####################### DEBUG CODE #######################################
##########################################################################

def db(text):
    #debug function
    if __debug__:
        print(text)
        

########################################################
################## CLASS PROGRAMMING BELOW #############
########################################################

class MovOb(object): #moveable Object
    # this object can be place din a list, and iterated over
    #for movement, damage, etc
    #all moveOb classes behave the same except as defined by
    #special attributes and the functions that move them and deal
    #with their collisions.
    def __init__(self,health,damage,position,velocity):
        self.health = health
        self.position = position
        self.velocity = velocity
        self.damage = damage
        
class Enemies(MovOb):
    #class will store enemies
    def __init__(self,health=1,damage=0,position=(200,200),
                     velocity=[0,0],affinity= "light",name = "enemy1"):
        super(Enemies,self).__init__(health,damage,position,velocity)
        self.affinity = affinity
        self.name = name

class EnemyProjectile(MovOb):
    # the class for enemy attacks
    def __init__(self,health=-1,damage=1,position=(0,0),
                         velocity=[0,10],affinity = "light"):
        super(EnemyProjectile,self).__init__(health,damage,position,velocity)
        self.affinity = affinity
        
class PlayerProjectile(MovOb):
    #the class for the player's attacks
    def __init__(self,health=-1,damage=1,position=(0,0),
                         velocity=[0,-20],affinity = "light"):
        super(PlayerProjectile,self).__init__(health,damage,position,velocity)
        self.affinity = affinity
        
class Powerups(MovOb):
    #the class to deal with powerups
    def __init__(self,health=-1,damage=1,position=(0,0),velocity=[0,0.25]):
        super(Powerups,self).__init__(health,damage,position,velocity)
        
class Player(MovOb):
    def __init__(self,health = 10,damage = 1,position = (150,550),
                         velocity = [0,0],affinity="light" ):
        super(Player,self).__init__(health,damage,position,velocity)
        self.affinity = affinity


########################################################################
################## GAME PROGRAMMING BELOW ##############################
########################################################################

class Game(object):
    #creating an instance of this class initializes the game,
    #canvas, and calls timerfired
    def __init__(self):
        self.root = Tk()
        self.root.resizable(width=False,height=False)
        self.canvas = Canvas(self.root,width = 400,height = 600)
        self.canvas.pack()
        self.root.canvas = self.canvas.canvas = self.canvas
        class Struct: pass
        self.canvas.data = Struct()
        #pygame.mixer.pre_init(44100, -16,2,2048)
        #pygame.init()
        self.init()
        self.root.bind("<Button-1>",self.mouse1Pressed)
        self.root.bind("<Button-3>",self.mouse3Pressed)
        self.root.bind("<Motion>",self.mouseMotion)
        self.root.bind("<ButtonRelease-1>",self.mouse1Released)
        self.root.bind("<ButtonRelease-3>",self.mouse3Released)
        self.root.bind("<Key>",self.keyPressed)
        self.root.bind("<KeyRelease>",self.keyReleased)
        self.timerFired()
        self.root.mainloop()

    def init(self):
        #loads and initializes all the variables/files needed by the game
        self.framerate = 50 #fps
        self.initImages()
        self.initMenuBools()
        self.initPlayerSettings()
        self.initDictionaries()
        self.initControlVariables()
        self.createEnemies()
        
    def initControlVariables(self):
        #ints variables needed for keyboard/mouse input
        self.timeSinceLastShot = time.time()
        self.timeSinceLastChange = time.time()
        self.backgroundPosition = 0
        self.Button1 = False
        self.Button3 = False
        self.mousePosition = self.player.position
        self.keysPressed = set()
        self.paused = False
        self.boss1AttackTime = -9999

    def initDictionaries(self):
        #creates the dictionaries containing projectiles and powerups
        self.playerProjectiles = dict()
        self.playerProjectilesRemoveList = []
        self.enemyProjectiles = dict()
        self.enemyProjectilesRemoveList = []
        self.enemies = dict()
        self.enemyRemoveList = []
        self.powerups = dict()
        self.powerupRemoveList = []

    def initPlayerSettings(self):
        #creates the player, creates default settings
        #incase no difficulty is chosen, defaults to "easy"
        self.player=Player()
        self.player.health = 10
        self.lives = 4
        self.kills = 0
        self.score = 0
        self.defaultHealth = self.player.health
        self.timeSinceDeath = time.time()
        self.stage = 0
        self.mode="easy"
        self.continues = 0
        self.projectiles = 0
        self.timeStart = time.time()
        self.difficulty()
        self.upgraded = False
        self.soundOn = True
        
    def initMenuBools(self):
        #initializes menu bools such as mouseovers for highlighting and inX's
        #for specifying which menu the program is in.
        self.playGameHover = False
        self.settingsHover = False
        self.helpHover = False
        self.quitHover = False
        self.yesHover = False
        self.noHover = False
        self.inMenu = True
        self.inGame = False
        self.inSettings = False
        self.inHelp = False
        self.gameOver = False
        self.easyHover = False
        self.mediumHover = False
        self.hardHover = False
        self.onHover = False
        self.offHover = False
        self.backHover = False
        self.showStats = False

    def initImages(self):
        #loads all of the images used by the game
        self.canvas.data.playerShip = []
        self.canvas.data.playerShip += \
                                    [PhotoImage(file="Player Ship Light.gif")]
        self.canvas.data.playerShip +=\
                                    [PhotoImage(file="Player Ship Dark.gif")]
        self.canvas.data.playerProjectile = \
                                          [PhotoImage(file="Light Projectile.gif"),
                                            PhotoImage(file="Dark Projectile.gif")]
        self.canvas.data.background = PhotoImage(file="background.gif")
        self.canvas.data.enemyProjectile = \
                                         [PhotoImage(file="enemy light projectile.gif"),
                                        PhotoImage(file="enemy dark projectile.gif")]
        self.canvas.data.enemy1 = [PhotoImage(file="Enemy1 light.gif"),
                                                                PhotoImage(file="Enemy1 dark.gif")]
        self.canvas.data.boss1 = PhotoImage(file = "boss1.gif")
        self.canvas.data.enemy2 = [PhotoImage(file = "enemy2 light.gif"),
                                                        PhotoImage(file = "enemy2 dark.gif")]
        self.canvas.data.livesDisplay = PhotoImage(file="livesDisplay.gif")
        self.canvas.data.shield = PhotoImage(file="Death shield.gif")
        self.canvas.data.helpScreen = PhotoImage(file="helpScreen.gif")
        self.canvas.data.powerupImage = PhotoImage(file="powerup.gif")
        
        
    def timerFired(self):
        #Timerfired, calls the revelant functions depending on the menu bools
        self.redrawAll()
        delay = 1000/self.framerate #ms
        if self.inGame and not(self.paused):
            self.moveProjectiles()
            self.moveEnemyProjectiles()
            self.clearProjectiles()
            self.clearEnemyProjectiles()
            self.movePowerups()
            self.clearPowerups()
            self.moveEnemies()
            self.clearEnemies()
            if self.Button1 or self.Button3:
                self.mouseControlls()
            self.backgroundPosition += 0.5
            if self.backgroundPosition == 1323: #keeps the background repeating
                self.backgroundPosition = 0
            self.movePlayer(0,0)
        self.executeKeys()
        self.canvas.after(delay,self.timerFired)

################## PLAYER PROGRAMMING BELOW  #####################
            
    def shootPlayerWeapon(self):
        #creates the player's attacks, puts them in the
        #playerProjectiles dictionary
        if (time.time() - self.timeSinceLastShot) > 0.1:
            if self.soundOn:
                #winsound.PlaySound("player shoots.wav",winsound.SND_ASYNC)
                pass
            (x,y) = self.player.position
            affinity = self.player.affinity
            left = PlayerProjectile(1,1, (x-18,y-15),[0,-10],affinity)
            right = PlayerProjectile(1,1,(x+16,y-15),[0,-10],affinity)
            self.playerProjectiles[left] = len(self.playerProjectiles)
            self.playerProjectiles[right] = len(self.playerProjectiles)
            if self.upgraded:
                left =PlayerProjectile(1,1,(x-9,y-11),[0,-10],affinity)
                right = PlayerProjectile(1,1,(x+8,y-11),[0,-10],affinity)
                self.playerProjectiles[left] = len(self.playerProjectiles)
                self.playerProjectiles[right] = len(self.playerProjectiles)
            self.timeSinceLastShot = time.time()
            if not self.gameOver:
                self.projectiles += 1
        

    def changePlayerAffinity(self):
        #changes the players affinity, repeat rate is once/200ms
        if time.time()-self.timeSinceLastChange >= 0.20:
            if self.player.affinity == "light":
                self.player.affinity =  "dark"
            else:        
                self.player.affinity = "light"
            self.timeSinceLastChange = time.time()
            
    def movePlayer(self,dx,dy):
        #moves the player by 5dx,5dy
        (x,y) = self.player.position
        x = x + 3*dx
        y = y + 3*dy
        self.player.position = (x,y)
        if self.isLegalPlayer(x,y) == False:
            self.movePlayer(-dx,-dy)

    def isLegalPlayer(self,x,y):
        #conditions for player death and for player collision are called here
        # can return True or False, and changes the player's health upon hit
        #in self.playerCollision(x,y)
        (x,y) = self.player.position
        if self.player.health <= 0:
            if self.soundOn:
                #winsound.PlaySound("explosion.wav",winsound.SND_ASYNC)
                self.lives-=1
                self.timeSinceDeath = time.time()
            if self.lives == 0:
                self.deathTime = time.time()
                self.gameOver = True
                self.inGame = False
            self.player = Player(health = self.defaultHealth)
        return self.playerCollision(x,y)

    def playerCollision(self,x,y):
        #see above comment
        if 25<=x<=375 and 25 <= y <= 575:
            for projectile in self.enemyProjectiles:
                (px,py) = projectile.position
                if px-20<x<px+20 and -20<=py-y<=20:
                    self.enemyProjectilesRemoveList += [projectile]
                    if self.player.affinity ==\
                       projectile.affinity and self.player.health <=\
                       self.defaultHealth:
                        self.player.health += 0.05
                        return True
                    elif projectile.affinity != self.player.affinity:
                        if (time.time()-self.timeSinceDeath) >3:
                            self.player.health -= 1
                        if self.soundOn:
                            #winsound.PlaySound ("player hit.wav",
                                                #winsound.SND_ASYNC)
                            pass
            return True
        else:
            return False
        


################## ENEMY PROGRAMMING BELOW ##############################

#----------------------- LEVEL PROGRAMMING----------
    def createEnemies(self):
        #This is the function that calls various levels of the game.
        #on the first play through to the boss it progresses normally
        #later on it chooses stages randomly and returns to the boss
        #only after a specified time has passed
        t = time.time()
        if  (t - self.boss1AttackTime > 720 and self.boss1AttackTime >0)\
            or (self.score/(self.scoreMult()**0.5) > 30000):# or ((time.time()-self.timeStart)>100):
                #stage 9001 only happens when the player has played for 12
            #minutes or has acheived a score high enough to trigger the level
            self.stage = 9001
        if len(self.enemies) == 0 or self.stage == 8:
            if self.stage == 0:
                self.stage0()
            elif self.stage ==1:
                self.stage = 2
                self.stage1()
            elif self.stage==2:
                self.stage = 3
                self.stage2()
            elif self.stage == 3:
                self.stage = 4
                self.stage3()
            elif self.stage == 4:
                self.stage = 5
                self.stage4()
            elif self.stage == 5:
                self.stage = 6
                self.stage5()
            elif self.stage ==6 and ((t - self.boss1AttackTime > 6)):
                self.stage6()
            elif self.stage == 7:
                self.stage7()
            elif self.stage == 8:
                self.stage8()
            elif self.stage == 9001:
                self.stage9001()
        if self.stage == 9001 and not(self.enemy1Exists()):
            for x in xrange(80,320,40):
                self.createEnemy1(x,-10)


    def enemy1Exists(self):
        #function for the final stage (9001) to keep respawning little enemies
        for enemy in self.enemies:
            if enemy.name == "enemy1":
                return True

    def stage0(self):
        #just basic enemies, repeats until the player has 15 kilsl
        if self.stage == 0:
            self.stage = 0
            for x in xrange(400/10, 399,40):
                self.createEnemy1(x,-20) #x, y co-ordinates
                if self.kills >15:
                    self.stage = 1

    def stage1(self):
        #creates 2 rows of enemies
        for x in xrange(80,320,40):
            self.createEnemy1(x,-20)
            self.createEnemy1(x,-40)

    def stage2(self):
        #creates two slightly larger rows of enemies
        for x in xrange(40,360,40):
            self.createEnemy1(x,-20)
            self.createEnemy1(x,-40)
    
    def stage3(self):
        #3 rows of enemies
        for x in xrange(40,360,40):
            self.createEnemy1(x,-20)
            self.createEnemy1(x,-40)
            self.createEnemy1(x,-60)

    def stage4(self):
        #creates 3 rows of basic enemies, introduces a new enemy
        #that goes down the side and fires sideways and can change afifnity
        for x in xrange(80,320,40):
            self.createEnemy1(x,-15)
            self.createEnemy1(x,-30)
            self.createEnemy1(x,-45)
            self.createEnemy2(30,-10,"light")

    def stage5(self):
        #creates two of the new enemeis, and just 1 row of the basic enemy
        self.createEnemy2(30,-10,"dark")
        self.createEnemy2(370,-10,"light")
        for x in xrange(400/10,399,40):
            self.createEnemy1(x,-20)

    def stage6(self):
        #this is the boss level
        #can only face the boss once every 120 seconds after the first time
        #else it goes to a random level
        if time.time() - self.boss1AttackTime > 120:
            self.createBoss1(200,-40)
        elif self.upgraded:
            self.stage7()

    def stage7(self):
        #this stage plays random levels to make the game infinite
        stage = str(int(round(random.random()*6)))
        func = "self.stage" + stage + "()"
        eval(func)

    def stage8(self): # for getting powerup
        #this stage creates and allows the player to collect the powerup
        (x,y) = self.powerupLocation
        if len(self.powerups) == 0:
            self.createPowerup(x,y)
        if self.upgraded:
            self.stage = 7
        if not(self.upgraded) and ((time.time() - self.boss1AttackTime) >
                                   400.0/0.25/50):
            self.stage = 1

    def stage9001(self):
        #this is the ultimate "screw you" level ,that is still barely playable,
        #and repeats forever until the player is dead
        self.createBoss1(200,-40)
        for x in xrange(80,320,40):
            self.createEnemy1(x,-10)
            self.createEnemy1(x,-20)
            self.createEnemy1(x,-30)
            self.createEnemy1(x,-40)
            self.createEnemy1(x,-50)
            self.createEnemy1(x,-60)
            self.createEnemy1(x,-70)
            self.createEnemy1(x,-80)
            self.createEnemy1(x,-90)
            
        self.createEnemy2(30,-10,"dark")
        
            
 #----------------- END LEVEL PROGRAMMING------------------
        
    def randomAffinity(self):
        #returns a random affinity for creating basic enemies
        return ("light","dark")[int(round(random.random()))]
    
    def createEnemy1(self,x,y):
        #creates a basic enemy with a random affinity at x,y
            enemy1 = Enemies(health=5,damage=1,position=(x,y),velocity=[0,0],
                                            affinity = self.randomAffinity())
            self.enemies[enemy1] = len(self.enemies)

    def createBoss1(self,x,y):
        #creates the boss off screen
        boss = Enemies(health = 1000,damage=1,position=(x,y),velocity=[0,0],
                       affinity = "light",name="boss1")
        self.enemies[boss] = len(self.enemies)
        self.boss1AttackTime = time.time()

    def createEnemy2(self,x,y,aff):
        #creates an enemy2 at x,y with starting affinity = aff
        enemy2 = Enemies(health = 20,damage=2,position=(x,y),velocity=[0,0],
                                     affinity = aff, name = "enemy2")
        self.enemies[enemy2] = len(self.enemies)
        self.enemy2AttackTime = time.time()

############ ENEMY MOVEMENT PROGRAMMING BELOW##############
    def moveEnemies(self):
        #iterates over all enemies in self.enemies and moves them by
        #calling self.moveEnemy(enemy)
        for enemy in self.enemies:
            self.moveEnemy(enemy)
            if enemy.name == "enemy1":
                self.enemy1Attack(enemy)
            if enemy.name == "boss1":
                self.boss1Attack(enemy)
            if enemy.name == "enemy2":
                self.enemy2Attack(enemy)
                

    def moveEnemy(self,enemy):
        #moves an enemy by calling the revelant move function
        (x,y) = enemy.position
        if enemy.name == "enemy1":
            self.moveEnemy1(enemy,x,y)
        elif enemy.name == "enemy2":
            self.moveEnemy2(enemy,x,y)
        elif enemy.name == "boss1":
            self.moveBoss1(enemy,x,y)


    def moveEnemy1(self,enemy,x,y):
        #moves enemy1, their behavior changes as soon as the player gets a hang
        #of shooting/moving to be more difficult
        if self.kills < 10:
            y += 1
        else:
            y += 2 + random.random()*2 -1
            x += 0 +random.random()*10 - 5
        dictPos = self.enemies[enemy]
        enemy.position = (x,y)
        self.enemies[enemy] = dictPos 

    def moveEnemy2(self,enemy,x,y):
        #moves an enemy2 around the perimiter of the map
        if x > 30 and 30< y < 50:
            x -=2
        elif x<= 30 and y<550:
            y +=5
        elif x<370 and y>=550:
            x+=2
        elif x>=370 and y>=50:
            y -= 5
        elif y < 40:
            y +=5
        if random.random() >0.998:
            #randomly changes the enemies affinity with a probablilty of ~
            #once per 10 seconds
            #oh my god there is SNOW OUTSIDE ----------------------------------
            enemy.affinity = self.randomAffinity()
        dictPos = self.enemies[enemy]
        enemy.position = (x,y)
        self.enemies[enemy] = dictPos
        
    def moveBoss1(self,enemy,x,y):
        #moves the boss slowly down to its attack position
        #then keeps it above the player
        (tx,ty) = self.player.position
        (dx,dy) = (tx-x,ty-y)
        mag = (dx**2+dy**2)**0.5 /10
        if y <200:
            y +=  + random.random()*2
        if y >= 200:
            x += dx/mag
            pass
        if enemy.health <=10:
            #defines the location of the powerup for stage8
            self.powerupLocation = enemy.position
        dictPos = self.enemies[enemy]
        enemy.position = (x,y)
        self.enemies[enemy] = dictPos
            
    def clearEnemies(self):
        #first finds all the illegal enemies with by iterating over clearEnemy
        #then removes them with the removelist and the del command
        for enemy in self.enemies:
            self.clearEnemy(enemy)
        for item in self.enemyRemoveList:
            del self.enemies[item]
        self.createEnemies()
        self.enemyRemoveList = []

    def clearEnemy(self,enemy):
        #finds illegal enemeis, does damage and score modifications
        legal = self.isLegalEnemy(enemy)
        if legal == False:
            self.enemyRemoveList += [enemy]
        elif legal == "hit":
            dictPos = self.enemies[enemy]
            enemy.health -= self.player.damage*2
            self.enemies[enemy] = dictPos
        elif legal == "badhit":
            dictPos = self.enemies[enemy]
            enemy.health -= self.player.damage/2.0
            self.enemies[enemy] = dictPos

    def isLegalEnemy(self,enemy):
        #does score calculations,
        #adds to self.kills, and specifies a powerup condition
        (x,y) = enemy.position
        if enemy.health <= 0 and enemy.name == "enemy1":
            if self.soundOn:
                #winsound.PlaySound("explosion.wav",winsound.SND_ASYNC)
                self.score += 10*self.scoreMult()
                self.kills +=1
        if enemy.health <=0 and enemy.name == "boss1":
            self.score += 1000*self.scoreMult()
            self.kills += 1
            if not(self.upgraded):
                self.stage8()
        if enemy.health <= 0 and enemy.name == "enemy2":
            if self.continues == 0:
                self.score += 100*self.scoreMult()
            self.kills += 1
        return self.enemyCollision(enemy,x,y)

    def scoreMult(self):
        #returns the difficulty multiplier for points
        diff = self.mode
        if diff == "easy":
            return 1
        if diff == "medium":
            return 2
        if diff == "hard":
            return 4

    def enemyCollision(self,enemy,x,y):
        #collision condiditions for each enemy, hit box/circle
        #from player attacks
        if 0 <=x<=400 and -50<=y<=600 and enemy.health > 0:
            for projectile in self.playerProjectiles:
                (px,py) = projectile.position
                if enemy.name == "enemy1":
                    if px-12<x<px+12 and 0<=py-y<=20:
                        self.playerProjectilesRemoveList += [projectile]
                        if projectile.affinity == enemy.affinity:
                            if self.continues == 0:
                                self.score += 1
                            return "hit"
                        else:
                            return "badhit"
                if enemy.name == "boss1":
                    dx = abs(x-px)
                    dy = abs(y-py)
                    if (dx**2 + dy**2)**0.5 <=50:
                        self.playerProjectilesRemoveList += [projectile]
                        if self.continues == 0:
                            self.score += 1
                        return "hit"
                if enemy.name == "enemy2":
                    if px-12<=x<=px+12 and py-15<=y<=py+15:
                        self.playerProjectilesRemoveList += [projectile]
                        if projectile.affinity == enemy.affinity:
                            if self.continues == 0:
                                self.score += 1
                            return "hit"
                        else:
                            return "badhit"
                        
                
            return True
        else:
            return False

############### ENEMY PROJECTILE PROGRAMMING BELOW #####################

    def enemy1Attack(self,enemy):
        #enemy1 has a random attack. before 10 kills it goes straight down, and
        #after the attack goes towards the player
        if random.random() >= 0.96:
            (x,y) = enemy.position
            if self.kills <10:
                simpleAttack = EnemyProjectile(1,1,(x,y+10),[0,5],enemy.affinity)
            else:
                (tx,ty) = self.player.position
                (dx,dy) = (tx-x,ty-y)
                mag = (dx**2+dy**2)**0.5 /5
                simpleAttack = EnemyProjectile(1,1,(x,y),[dx/mag,dy/mag]
                                               ,enemy.affinity)
            self.enemyProjectiles[simpleAttack] = len(self.enemyProjectiles)

    def enemy2Attack(self,enemy):
        #enemy 2 attacks sideways out of its ports in both direction
        #this forces the player to move off of the bottom row
        #attacks at a random interval, on average 2seconds
        (x,y) = enemy.position
        t = time.time()
        projectileList = []
        if random.random() >= 0.99:
            leftUp = EnemyProjectile(1,1,(x-10,y+13),[-3,0],enemy.affinity)
            leftMid = EnemyProjectile(1,1,(x-10,y),[-3,0],enemy.affinity)
            leftBot = EnemyProjectile(1,1,(x-10,y-13),[-3,0],enemy.affinity)
            rightUp = EnemyProjectile(1,1,(x+10,y+13),[3,0],enemy.affinity)
            rightMid = EnemyProjectile(1,1,(x+10,y),[3,0],enemy.affinity)
            rightBot  = EnemyProjectile(1,1,(x+10,y-13),[3,0],enemy.affinity)
            projectileList += [leftUp] + [leftMid] + [leftBot] + [rightUp] +\
                [rightMid] + [rightBot]
            for projectile in projectileList:
                self.enemyProjectiles[projectile] = len(self.enemyProjectiles)
            

    def boss1Attack(self,enemy):
        #defines boss1's attack pattern
        #he attacks with sweeping arcs, and after he has been beaten, or
        #on the harder difficulty, one of his attacks is directed at the player
        (x,y) = enemy.position
        t = time.time()
        (tx,ty) = self.player.position
        (dx,dy) = (tx-x,ty-y)
        mag = (dx**2+dy**2)**0.5 /7
        if y >= 190 and t-self.boss1AttackTime>= 0.03:
            leftDarkAttack = EnemyProjectile(1,1,(x-28,y+40),[(7*math.cos(t)),
                                                              abs(10*math.sin(t))],"dark")
            if self.mode == "easy" and not(self.upgraded):
                leftLightAttack = EnemyProjectile(1,1,(x-15,y+47),[(7*math.sin(-t)),
                                                                   abs(10*math.cos(-t))],"light")
            else:
                leftLightAttack = EnemyProjectile(1,1,(x-15,y+47),
                                                  [dx/mag,dy/mag],"light")
            rightDarkAttack = EnemyProjectile(1,1,(x+28,y+40),[(7*math.cos(-t)),
                                                               abs(10*math.sin(-t))],"dark")
            rightLightAttack = EnemyProjectile(1,1,(x+15,y+47),[(7*math.sin(t))
                                                                ,abs(10*math.cos(t))],"light")
            self.boss1AttackTime = t
            self.enemyProjectiles[leftDarkAttack] = len(self.enemyProjectiles)
            self.enemyProjectiles[leftLightAttack] = len(self.enemyProjectiles)
            self.enemyProjectiles[rightDarkAttack] = len(self.enemyProjectiles)
            self.enemyProjectiles[rightLightAttack] = len(self.enemyProjectiles)
            
    def clearEnemyProjectiles(self):
        #clears projectiles that are out of bounds
        #or have been placed in the remove list by collision functions
        for projectile in self.enemyProjectiles:
            self.clearEnemyProjectile(projectile)
        for item in self.enemyProjectilesRemoveList:
            if item in self.enemyProjectiles:
                del self.enemyProjectiles[item]
        self.enemyProjectilesRemoveList= []
            
    def clearEnemyProjectile(self,projectile):
        #places projectile in the remove list if it is outof bounds
        if self.isLegalEnemyProjectile(projectile) == False:
            self.enemyProjectilesRemoveList += [projectile]

    def isLegalEnemyProjectile(self,projectile):
        #tests if the projectile is out of bounds
        (x,y) = projectile.position
        if 0<=x<=400 and 0<=y<=600:
            return True
        else:
            return False
        
    def moveEnemyProjectiles(self):
        #moves the projectiles in self.enemyProjectiles by calling
        #self.moveEnemyProjectile
        for projectile in self.enemyProjectiles:
            self.moveEnemyProjectile(projectile)

    def moveEnemyProjectile(self,projectile):
        #moves projectiles by their velocity, allowing them to be
        #directed toward the player
        (x,y) = projectile.position
        x += projectile.velocity[0]
        y += projectile.velocity[1]
        dictPos = self.enemyProjectiles[projectile]
        projectile.position = (x,y)
        self.enemyProjectiles[projectile] = dictPos


############# PLAYER PROJECITLE PROGRAMMING BELOW ######################

    def clearProjectiles(self):
        #clears the players projectiles, like the one for enemies above
        for projectile in self.playerProjectiles:
            self.clearProjectile(projectile)
        for item in self.playerProjectilesRemoveList:
            if item in self.playerProjectiles:
                del self.playerProjectiles[item]
        self.playerProjectilesRemoveList= []
            
    def clearProjectile(self,projectile):
        #clears it like above
        if self.isLegalProjectile(projectile) == False:
            self.playerProjectilesRemoveList += [projectile]

    def isLegalProjectile(self,projectile):
        #clears like above
        (x,y) = projectile.position
        if 0<=x<=400 and 0<=y<=600:
            return True
        else:
            return False
        
    def moveProjectiles(self):
        #moves player projectiles like above
        for projectile in self.playerProjectiles:
            self.movePlayerProjectile(projectile)

    def movePlayerProjectile(self,projectile):
        #moves player projectiles like above
        (x,y) = projectile.position
        x += projectile.velocity[0]
        y += projectile.velocity[1]
        dictPos = self.playerProjectiles[projectile]
        projectile.position = (x,y)
        self.playerProjectiles[projectile] = dictPos

########## POWERUP PROGRAMMING BELOW ##############################

    def createPowerup(self,x,y):
        #creates a powerup, called in stage8()
        powerup = Powerups(position = (x,y))
        self.powerups[powerup] = len(self.powerups)
        
    def clearPowerups(self):
        #clears the powerup if it is in the remove list
        #acts like previous clear functions for movObs
         for powerup in self.powerups:
             self.clearPowerup(powerup)
         for item in self.powerupRemoveList:
            del self.powerups[item]
         self.powerupRemoveList = []

    def clearPowerup(self,powerup):
        #same a previous clear functions
        legal = self.isLegalPowerup(powerup)
        if legal == False:
            self.powerupRemoveList += [powerup]
        elif legal == "player":
            self.upgrade()
            self.powerupRemoveList += [powerup]

    def movePowerups(self):
        #same as previous move functions
        for powerup in self.powerups:
            self.movePowerup(powerup)

    def movePowerup(self,powerup):
        #moves powerup by its velocity
        (x,y) = powerup.position
        x += powerup.velocity[0]
        y += powerup.velocity[1]
        dictPos = self.powerups[powerup]
        powerup.position = (x,y)
        self.powerups[powerup] = dictPos

    def isLegalPowerup(self,powerup):
        #tests whether or not the powerup is legal
        #conditions are out of bounds or hitting the player
        (x,y) = powerup.position
        if 25<=x<=375 and 0<=y<=600:
            (px,py) = self.player.position
            if px-20<=x<=px+20 and py-20<=y<=py+20:
                return "player"
            else:
                return True
        return False
    
###########################################################################
##############GAME DISPLAY PROGRAMMING BELOW ###########################
###########################################################################
        
    def redrawAll(self):
        #redraws the game
         self.canvas.delete(ALL)
         if self.inGame:
            self.drawGame()
         if self.inMenu:
            self.drawMenu()
         if self.gameOver:
            self.drawGameOver()
         if self.paused:
            self.drawPaused()

    def drawGame(self):
        #calls the game related functions
        self.drawBackground()
        self.drawEnemies()
        self.drawPowerups()
        self.drawEnemyProjectiles()
        self.drawPlayerProjectiles()
        self.drawPlayer()
        self.drawScore()
        self.drawHealthBar()
        self.drawLives()
            
    def drawBackground(self):
        #creates the background, shifted by the backgroundPosition variable
        #for a scrolling background
        self.canvas.create_image(200,600+self.backgroundPosition ,anchor = S,
                                                        image = self.canvas.data.background)

    def drawPlayer(self):
        #draws the player character with the correct appearance and affinity
        if self.player.affinity == "light":
            affinity = 0
        else:
            affinity = 1
        (x,y) = self.player.position
        self.canvas.create_image(x,y,image=
                                 self.canvas.data.playerShip[affinity])
        # draws the players shield if they are during the invulnerabilty period
        if time.time() - self.timeSinceDeath<3:
            self.canvas.create_image(x,y,image=self.canvas.data.shield)

    def drawEnemies(self):
        #draws all of the onscreen enemies
        #and, if they have affinity appearances, draws them
        #in their appropriate affinity
        for enemy in self.enemies:
            if enemy.affinity == "light":
                affinity = 0
            else:
                affinity = 1
            (x,y) = enemy.position
            if enemy.name == "enemy1":
                self.canvas.create_image(x,y,image=
                                         self.canvas.data.enemy1[affinity])
            if enemy.name == "boss1":
                self.canvas.create_image(x,y,image=self.canvas.data.boss1)
                self.drawBossHpBar(enemy,x,y)
            if enemy.name == "enemy2":
                self.canvas.create_image(x,y,image=
                                         self.canvas.data.enemy2[affinity])

    def drawBossHpBar(self,enemy,x,y):
        #creates the hp bar for the boss, a much requested feature
        health = enemy.health
        (lx,ly) = (x-health/10,y-80)
        (rx,ry) = (x+health/10,y-70)
        self.canvas.create_rectangle(x-100,y-80,x+100,y-70,fill = "gray")
        self.canvas.create_rectangle(lx,ly,rx,ry,fill = "red")
            
    def drawEnemyProjectiles(self):
        #calls the draw function f every projectile in
        #the dict of enemy projectiles
        for projectile in self.enemyProjectiles:
            self.drawEnemyProjectile(projectile)

    def drawEnemyProjectile(self,projectile):
        #draws the projectile given to it
        (x,y) = projectile.position
        if projectile.affinity == "light":
            affinity = 0
        else:
            affinity = 1
        self.canvas.create_image(x,y,image=
                                 self.canvas.data.enemyProjectile[affinity])
        
    def drawPlayerProjectiles(self):
        #draws all of the player projectiles in the dict
        #by calling the appropriate function
        for projectile in self.playerProjectiles:
            self.drawPlayerProjectile(projectile)

    def drawPlayerProjectile(self,projectile):
        #draws the player projectile with its appropriate affinity
        (x,y) = projectile.position
        if projectile.affinity == "light":
            affinity = 0
        else:
            affinity = 1
        self.canvas.create_image(x,y,image=
                                 self.canvas.data.playerProjectile[affinity])

    def drawPowerups(self):
        #draws powerups if they exist
        for powerup in self.powerups:
            self.drawPowerup(powerup)

    def drawPowerup(self,powerup):
        #draws the powerup at its location
        (x,y) = powerup.position
        self.canvas.create_image(x,y,image=self.canvas.data.powerupImage)

    def drawScore(self):
        #displays the score in the upper right hand corner
        self.canvas.create_text(300,50,text = "Score =",font = ("FixedSys",12)
                                                ,fill="yellow")
        self.canvas.create_text(340,50,text = str(self.score) ,font = ("FixedSys"
                                                ,12 ),fill="yellow",anchor = W)
        
    def drawPaused(self):
        #displays a big "PAUSED" on the screen when the game is paused
        self.canvas.create_text(200,300,text="PAUSED",font=("FixedSys",36)
                                            ,fill="yellow")

    def drawHealthBar(self):
        #displays the player's health bar and a grey backdrop for it in the
        #upper left hand corner
        healthMax = self.defaultHealth
        health = self.player.health
        self.canvas.create_rectangle(25,25,150,40,fill = "gray", width = 2)
        self.canvas.create_rectangle(25,25,150*health/healthMax,40
                                     ,fill = "red",width = 2)
        self.canvas.create_text(62,12,text = "Health",font = ("FixedSys",12)
                                ,fill="yellow")
        
    def drawLives(self):
        #displays a small ship for each life the player has remaining
        for life in xrange(self.lives-1):
            self.canvas.create_image(25 + 30*life,550, image=
                                     self.canvas.data.livesDisplay)

########################################################################
##############MENU DISPLAY PROGRAMMING BELOW ###########################
########################################################################

    def drawMenu(self):
        #draws the menus, depening on the menu bools
        if self.inMenu and not(self.inSettings and self.inHelp):
            self.drawMenuBackground()
            self.drawMenuItems()
        if self.inMenu and self.inSettings and not(self.inHelp):
            self.drawMenuBackground()
            self.drawSettings()
        if self.inMenu and self.inHelp and not(self.inSettings):
            self.drawMenuBackground()
            self.drawHelp()
            
    def drawMenuBackground(self):
        #draws a black backgorund for the menus
        self.canvas.create_rectangle(0,0,400,600,fill = "black")

    def drawMenuItems(self):
        #draws the main menu items in their corrct color (for hovering)
        colors = ("yellow","red")
        playGameColor = colors[self.playGameHover]
        settingsColor = colors[self.settingsHover]
        helpColor = colors[self.helpHover]
        quitColor = colors[self.quitHover]
        self.canvas.create_text(200,100,text = "AXIAL"
                                ,font=("FixedSys",36),fill="yellow")
        self.canvas.create_text(200,300,text = "PLAY GAME"
                                ,font=("FixedSys",24),fill=playGameColor)
        self.canvas.create_text(200,350,text = "SETTINGS"
                                ,font=("FixedSys",24),fill=settingsColor)
        self.canvas.create_text(200,400,text = "HELP"
                                ,font=("FixedSys",24),fill=helpColor)
        self.canvas.create_text(200,450,text = "QUIT"
                                ,font=("FixedSys",24),fill=quitColor)

    def drawSettings(self):
        #draws the settings menu and its items in the correct color
        colors = ("yellow","red")
        easyColor=colors[self.easyHover]
        mediumColor=colors[self.mediumHover]
        hardColor=colors[self.hardHover]
        onColor = colors[self.onHover]
        offColor = colors[self.offHover]
        #Difficulty
        self.canvas.create_text(200,300,text = "DIFFICULTY"
                                ,font = ("FixedSys",24),fill="yellow")
        self.canvas.create_text(150,320,text = "Easy"
                                ,font = ("FixedSys",12),fill=easyColor)
        self.canvas.create_text(200,320,text = "Medium"
                                ,font = ("FixedSys",12),fill=mediumColor)
        self.canvas.create_text(250,320,text = "Hard"
                                ,font = ("FixedSys",12),fill=hardColor)
        #Sound
        self.canvas.create_text(200,400,text = "SOUND"
                                ,font = ("FixedSys",24),fill="yellow")
        self.canvas.create_text(170,420,text = "On"
                                ,font = ("FixedSys",12),fill=onColor)
        self.canvas.create_text(230,420,text = "Off"
                                ,font = ("FixedSys",12),fill=offColor)
        self.drawBackButton(200,500)

    def drawBackButton(self,x,y):
        #creates a back button to the main menu, used by many functions
        backColor = ("yellow","red")[self.backHover]
        self.canvas.create_text(x,y,text = "Main Menu",font =
                                ("FixedSys",20),fill=backColor)

    def drawHelp(self):
        #displays the help graphic and a back button
        self.canvas.create_image(200,300,image=self.canvas.data.helpScreen)
        self.drawBackButton(305,567)

##############GAME OVER DISPLAY PROGRAMMING BELOW #####################

    def drawGameOver(self):
        #draws the game over screen
        self.drawMenuBackground()
        colors = ("yellow","red")
        yesColor = colors[self.yesHover]
        noColor = colors[self.noHover]
        playTime = int(round(self.deathTime -self.timeStart))
        self.canvas.create_text(200,100,text = "GAME OVER"
                                ,font=("FixedSys",36),fill="yellow")
        self.canvas.create_text(160,200,text = "SCORE "
                                ,font=("FixedSys",24),fill="yellow")
        self.canvas.create_text(270,200,text = str(self.score)
                                ,font=("FixedSys",24),fill="yellow")

        self.canvas.create_text(160,230,text = "CONTINUES"
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(270,230,text = str(self.continues)
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(160,260,text = "SHOTS FIRED"
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(270,260,text = str(self.projectiles)
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(160,290,text = "DIFFICULTY"
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(270,290,text = str(self.mode)
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(160,320,text = "PLAY TIME"
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(270,320,text = str(playTime)
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(160,350,text = "kills"
                                ,font=("FixedSys",12),fill="yellow")
        self.canvas.create_text(270,350,text = str(self.kills)
                                ,font=("FixedSys",12),fill="yellow")
        
        self.canvas.create_text(200,400,text = "CONTINUE?"
                                ,font=("FixedSys",24),fill="yellow")
        self.canvas.create_text(200,450,text = "YES"
                                ,font=("FixedSys",24),fill=yesColor)
        self.canvas.create_text(200,500,text = "NO"
                                ,font=("FixedSys",24),fill=noColor)
        self.canvas.create_text(100,570,text = "Thank you for playing."
                                ,font= ("FixedSys",8),fill="blue")
        self.canvas.create_text(100,590,text = "Created by Glenn Philen"
                                ,font = ("FixedSys",8),fill="blue")
    

########################################################################
################## CONTROL PROGRAMMING BELOW  ##########################
########################################################################

    def mouseControlls(self):
        #calls the mouse controll functions depending on the mosue bools
        if self.Button1:
            self.shootPlayerWeapon()
        if self.Button3:
            self.changePlayerAffinity()
        self.moveToMouse()

    def moveToMouse(self):
        #moves the player ship to the mouse at the same speed as
        #the arrow keys can move the player
        (x,y) = self.player.position
        (mx,my) = self.mousePosition
        if mx > x:
            dx = 2
        elif mx < x:
            dx = -2
        else:
            dx = 0
        if my> y:
            dy = 2
        elif my<y:
            dy = -1
        else:
            dy = 0
        if mx -6 < x < mx+6 and my-6 < y < my+6:
            dy = 0
            dx = 0
        self.movePlayer(dx,dy)

    
    def mouse1Pressed(self,event):
        #sets mouse1 presed to true
        self.Button1 = True
        if self.inMenu:
            (x,y) = (event.x,event.y)
            

    def mouse3Pressed(self,event):
        #sets mouse3 to true
        self.Button3 = True
        
    def mouseMotion(self,event):
        #tells the menus where the mouse is hovering to highlight links
        self.mousePosition = (event.x,event.y)
        (x,y) = self.mousePosition
        if self.inMenu and not(self.inSettings or self.inHelp):
            self.mainMenuMouseOver(x,y)
        if self.inMenu and self.inSettings:
            self.settingsMenuMouseOver(x,y)
        if self.inMenu and self.inHelp:
            self.helpMenuMouseOver(x,y)
        if self.gameOver:
            self.gameOverMouseOver(x,y)

    def mainMenuMouseOver(self,x,y):
        #link highlighting for the mainmenu
            if 120<=x<=280 and 285<=y<=315:
                self.playGameHover = True
            else:
                self.playGameHover = False
            if 140<=x<=260 and 335<=y<=365:
                self.settingsHover = True
            else:
                self.settingsHover = False
            if 150<=x<=250 and 385<=y<=415:
                self.helpHover = True
            else:
                self.helpHover = False
            if 155<=x<=245  and 435<=y<=465:
                self.quitHover = True
            else:
                self.quitHover = False

    def settingsMenuMouseOver(self,x,y):
        #link highlighting for the settings menu
            if 140<=x<=160 and 315<=y<=325:
                self.easyHover = True
            else:
                self.easyHover = False
            if 185<=x<=215 and 315<=y<=325:
                self.mediumHover = True
            else:
                self.mediumHover = False
            if 240<=x<=260 and 315<=y<=325:
                self.hardHover = True
            else:
                self.hardHover = False
            if 165<=x<=175 and 415<=y<=425:
                self.onHover = True
            else:
                self.onHover = False
            if 225<=x<=235 and 415<=y<=425:
                self.offHover = True
            else:
                self.offHover = False
            if 150<=x<=250 and 480<=y<=520:
                self.backHover = True
            else:
                self.backHover = False

    def helpMenuMouseOver(self,x,y):
        #link highlighting for the help menu
        if 255<=x<=355 and 547<=y<=587:
            self.backHover = True
        else:
            self.backHover = False    

    def gameOverMouseOver(self,x,y):
            if 185<=x<=215 and 435<=y<=465:
                self.yesHover = True
            else:
                self.yesHover = False
            if 185<=x<=215 and 485<=y<=515:
                self.noHover = True
            else:
                self.noHover = False


    def mouse1Released(self,event):
        #sets the mouse1 bool to false, calls functions for clickble items
        (x,y) = (event.x,event.y)
        self.Button1 = False
        if self.inMenu and not(self.inSettings and self.inHelp):
            self.inMenuMouse(event)
        if self.inMenu and self.inSettings:
            self.inSettingsMouse(event)
        if self.inMenu and self.inHelp:
            self.inHelpMouse(event)
        if self.gameOver:
            self.inGameOverMouse(event)


    def mouse3Released(self,event):
        #sets the mouse3 bool to false
        self.Button3 = False
        pass

    def keyPressed(self,event):
        #adds the key to the list of keys pressed
        if event not in self.keysPressed and (event.keysym != "p"):
            self.keysPressed.add(event)

            
    def executeKeys(self):
        #goes through the list of pressed keys
        #allows multiple keys to be pressed simultaneously
        for event in self.keysPressed:
            if not(self.paused):
                if event.keysym in ["Up","w"]:
                    self.movePlayer(0,-3)
                elif event.keysym in ["Down","s"]:
                    self.movePlayer(0,2)
                elif event.keysym in ["Right","d"]:
                    self.movePlayer(3,0)
                elif event.keysym in ["Left","a"]:
                    self.movePlayer(-3,0)
                elif event.keysym == "space":     
                     self.shootPlayerWeapon()
                elif event.keysym == "c":
                    self.changePlayerAffinity()

                
        self.redrawAll()

    def pause(self):
        #changes the paused state of the game
        self.paused = not(self.paused)

    def keyReleased(self,event):
        #removes the key from the list of keys pressed, handles "p" for pausing
        t = time.time()
        returnset = set()
        self.keysPressedKS = []
        for item in self.keysPressed:
            self.keysPressedKS += set([item.keysym])
        if event.keysym in self.keysPressedKS:
            for item in self.keysPressed:
                if item.keysym != event.keysym:
                    returnset.add(item)
            self.keysPressed = set(returnset)
        if event.keysym == "p":
            self.pause()

###################### Menu Controlls ######################################

    def inMenuMouse(self,event):
        #clickable itemsfor the main menu
        (x,y) = (event.x,event.y)
        if 120<=x<=280 and 285<=y<=315:
            self.tempMode = self.mode
            self.init()
            self.mode = self.tempMode
            self.inMenu = False
            self.inSettings = False
            self.inHelp = False
            self.inGame = True
            self.difficulty()
        elif 140<=x<=260 and 335<=y<=365:
            self.inSettings = True
            self.inMenu = True
            self.inHelp = False
        elif 150<=x<=250 and 385<=y<=415:
            self.inHelp = True
        elif 155<=x<=245  and 435<=y<=465:
            self.quit()

    def inSettingsMouse(self,event):
        #clickable items for the settings menu
        (x,y) = (event.x,event.y)
        if 140<=x<=160 and 315<=y<=325:
            self.easyMode()
        if 185<=x<=215 and 315<=y<=325:
            self.mediumMode()
        if 240<=x<=260 and 315<=y<=325:
            self.hardMode()
        if 165<=x<=175 and 415<=y<=425:
            self.soundon()
        if 225<=x<=235 and 415<=y<=425:
            self.soundOff()
        if 150<=x<=250 and 480<=y<=520:
            self.inSettings = False
            self.inMenu = True

    def difficulty(self):
        #calls the appropriate difficulty function upon game start, depending
        #on the self.mode var
        mode = self.mode
        if mode == "easy":
            self.easyMode()
        if mode == "medium":
            self.mediumMode()
        if mode == "hard":
            self.hardMode()
    
    def easyMode(self):
        #defines the easyMode
        self.mode = "easy"
        self.player.health = 30
        self.lives = 5
        self.framerate = 50 #fps
        self.inSettings = False
        self.player=Player()
        self.kills = 0
        self.score = 0
        self.defaultHealth = self.player.health
        self.timeSinceDeath = time.time()
        self.stage = 0
        self.continues = 0
        self.projectiles = 0
        self.timeStart = time.time()
        
    def mediumMode(self):
        #defines the medium move
        self.mode = "medium"
        self.player.health = 15
        self.lives = 4
        self.framerate = 60 #fps
        self.inSettings = False
        self.player=Player()
        self.kills = 0
        self.score = 0
        self.defaultHealth = self.player.health
        self.timeSinceDeath = time.time()
        self.stage = 0
        self.continues = 0
        self.projectiles = 0
        self.timeStart = time.time()

    def hardMode(self):
        #defines the hard mode
        self.mode = "hard"
        self.player.health = 10
        self.lives = 2
        self.framerate = 80 #fps
        self.inSettings = False
        self.player=Player()
        self.kills = 0
        self.score = 0
        self.defaultHealth = self.player.health
        self.timeSinceDeath = time.time()
        self.stage = 0
        self.continues = 0
        self.projectiles = 0
        self.timeStart = time.time()
        
    def soundon(self):
        #turns sound on
        self.soundOn = True
        self.inSettings = False

    def soundOff(self):
        #turns sound off
        self.soundOn = False
        self.inSettings = False

    def upgrade(self):
        #upgrades the player ship with a new appearance
        #sets the bool that upgrades the weapons
        self.upgraded = True
        self.canvas.data.playerShip = \
                            [PhotoImage(file="Player Ship Light Upgraded.gif"),
                            PhotoImage(file="Player Ship Dark Upgraded.gif")]
            

    def inHelpMouse(self,event):
        #mouse events for the help menu
        (x,y) = (event.x,event.y)
        if 255<=x<=355 and 547<=y<=587:
            self.inHelp = False
            self.inMenu = True

    def inGameOverMouse(self,event):
        #mouse events for the gameover menu
        (x,y) = (event.x,event.y)
        if 185<=x<=215 and 435<=y<=465:
            self.gameOver = False
            self.lives = 1
            self.yesHover = False
            self.inGame = True
            self.timeSinceDeath = time.time()
            self.continues += 1
        if 185<=x<=215 and 485<=y<=515:
            self.gameOver = False
            self.inMenu = True
            self.showStats = True

    def quit(self):
        #quits the game
            self.root.destroy() 

Game()

