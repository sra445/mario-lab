add_library('minim')
import os, random
path = os.getcwd() + "/"
player = Minim(this)

class Creature:
    def __init__(self, x, y, r, g, img, w, h, F):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.img = loadImage(path + "images/"+img)
        self.w = w
        self.h = h
        self.f = 0
        self.F = F
        self.direction = 1
        self.vx = 0
        self.vy = 0
    
    def gravity(self):
        if self.y+self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.4
            if self.y + self.r + self.vy > self.g:
                 self.vy = self.g - (self.y+self.r)
        
        for p in g.platforms:
            if self.y + self.r <= p.y and self.x+self.r >= p.x and self.x-self.r <= p.x+p.w:
                self.g = p.y
                break
            self.g = g.g
    
    def update(self):
        self.gravity()
    
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        stroke(255,0,0)
        
        if self.direction == 1:
            image(self.img,self.x-self.w//2 - g.x , self.y -self.h//2, self.w, self.h, int(self.f) * self.w, 0, (int(self.f) +1)* self.w, self.h )
        elif self.direction == -1:
            image(self.img,self.x-self.w//2 - g.x, self.y -self.h//2, self.w, self.h, (int(self.f) +1) * self.w, 0,  int(self.f) * self.w, self.h )
        
        if self.vx != 0:
            self.f = (self.f + .2) % self.F
            
class Mario(Creature):
    def __init__(self, x, y, r, g, img, w, h, F):
        Creature.__init__(self,x, y, r, g, img, w, h, F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}
        self.jumpSound = player.loadFile(path + "sounds/jump.mp3")
        self.killSound = player.loadFile(path + "sounds/kill.mp3")
        self.starSound = player.loadFile(path + "sounds/coin.mp3")
        self.starCnt = 0
        
    def update(self):
        self.gravity()
        
        if self.keyHandler[LEFT]:
            self.vx = -5
            self.direction = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 8
            self.direction = 1
        else:
            self.vx = 0
            
        if self.keyHandler[UP] and self.y + self.r == self.g:
            self.jumpSound.rewind()
            self.jumpSound.play()
            self.vy = -15
            
        if self.x - self.r < 0:
            self.x = self.r 
        
        self.x += self.vx
        self.y += self.vy
        
        if self.x >= g.w//2:
            g.x += self.vx

        for s in g.stars:
            if self.distance(s) <= self.r + s.r:
                g.stars.remove(s)
                self.starSound.rewind()
                self.starSound.play()
                self.starCnt += 1
                

        for e in g.enemies:
            if self.distance(e) <= self.r + e.r:
                if self.vy > 0:
                    g.enemies.remove(e)
                    del e
                    self.killSound.rewind()
                    self.killSound.play()
                    self.vy = -8
                else:
                    g.bgSound.pause()
                    g.__init__(1280,720,585)
                
    def distance(self, target):
        return ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5
        
        
class Gomba(Creature):
    def __init__(self, x, y, r, g, img, w, h, F, xL, xR):
        Creature.__init__(self,x, y, r, g, img, w, h, F)
        self.xL = xL
        self.xR = xR
        self.vx = random.randint(1,5)
        
    def update(self):
        self.gravity()
    
        if self.x > self.xR:
            self.vx *= -1
            self.direction = -1
        elif self.x < self.xL:
            self.vx *= -1
            self.direction = 1
        
        self.x += self.vx
        self.y += self.vy
    
class Platform:
    def __init__(self,x,y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path+"images/"+img)
    
    def display(self):
        image(self.img, self.x - g.x, self.y, self.w, self.h)

class Star(Creature):
    def __init__(self, x, y, r, g, img, w, h, F, theta, r1):
        Creature.__init__(self,x, y, r, g, img, w, h, F)
        self.theta = theta
        self.cx = x
        self.cy = y
        self.r1 = r1
    
    def update(self):
        self.f = (self.f + .2) % self.F
        
        self.theta += 0.01
        self.x = self.cx + self.r1*cos(self.theta)
        self.y = self.cy + self.r1*sin(self.theta)
        
                                                         
class Game:
    def __init__(self, w, h, g):
        self.x = 0
        self.w = w
        self.h = h
        self.g = g
        self.time = 0
        self.pause = False
        self.pauseSound = player.loadFile(path + "sounds/pause.mp3")
        self.bgSound = player.loadFile(path + "sounds/background.mp3")
        self.bgSound.play()
        self.bgSound.loop()
        
        self.enemies = []
        self.platforms = []
        inputFile = open(path+"level1.csv","r")

    # self.mario = Mario(50,50, 35, self.g, "mario.png", 100, 70, 11)
        
        self.bgImgs = []
        for i in range(5,0,-1):
            self.bgImgs.append(loadImage(path+"images/layer_0" + str(i) + ".png"))
        
        # self.enemies = []
        # for i in range(5):
        #     self.enemies.append(Gomba(random.randint(200, 500), 0, 35, self.g, "gomba.png", 70, 70, 5, 200, 800))
        
        # self.platforms = []
        # for i in range(3):
        #     self.platforms.append(Platform(250+i*300, 500-i*150, 200, 50, "platform.png"))
        
        # for i in range(3):
        #     self.platforms.append(Platform(1500+i*300, 500-i*150, 200, 50, "platform.png"))
    
    
        for line in inputFile:
            line = line.strip().split(",")
            if line[0] == "mario":
                self.mario = Mario(int(line[1]),int(line[2]), int(line[3]), int(line[4]), line[5], int(line[6]), int(line[7]), int(line[8]))
            elif line[0] == "platform":
                self.platforms.append(Platform(int(line[1]),int(line[2]), int(line[3]), int(line[4]), line[5]))
            elif line[0] == "gomba":
                self.enemies.append(Gomba(int(line[1]),int(line[2]), int(line[3]), int(line[4]), line[5], int(line[6]), int(line[7]), int(line[8]), int(line[9]), int(line[10])))
            elif line[0] == "ground":
                self.g = int(line[2])
    
    
        self.stars = []
        for i in range(7):
            self.stars.append(Star(300,300,20, self.g, "star.png", 40,40,6, i*0.9, 100))
        
        self.stars.append(Star(600,300,20, self.g, "star.png", 40,40,6, 0, 0))
        
    def display(self):
        self.time += 1
        cnt = 0
        x = 0
        for b in self.bgImgs:
            if cnt == 1:
                x = self.x//4
            if cnt == 2:
                x = self.x//3
            if cnt == 3:
                x = self.x//2
            if cnt == 4 and cnt == 5:
                x = self.x
            cnt += 1
            
            image(b,0,0, self.w - x%self.w, self.h, x%self.w, 0, self.w, self.h)
            image(b,self.w -x%self.w, 0, x%self.w, self.h, 0, 0, x%self.w, self.h)
        
        for p in self.platforms:
            p.display()
        
        for e in self.enemies:
            e.display()
            
        for s in self.stars:
            s.display()
            
        self.mario.display()
        
        
        textSize(30)
        text(self.mario.starCnt, self.w - 50, 50)
        text(self.time//60, self.w - 50, 100)
        
    

g = Game(1280,720,585)

def setup():
    size(g.w, g.h)
    background(255)
    
def draw():
    if not g.pause:
        background(255)
        g.display()

def keyPressed():
    if keyCode == LEFT:
        g.mario.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.mario.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.mario.keyHandler[UP] = True
    elif keyCode == 80:
        if g.pause:
            g.pause = False
            g.bgSound.play()
        else:
            g.pause = True
            g.bgSound.pause()
        g.pauseSound.rewind()
        g.pauseSound.play()
        
def keyReleased():
    if keyCode == LEFT:
        g.mario.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.mario.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.mario.keyHandler[UP] = False
