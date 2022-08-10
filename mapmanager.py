# напиши здесь код создания и управления картой
from panda3d.core import LVecBase4f
import random
import pickle

class Mapmanager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'
        # self.color = LVecBase4f(0.4, 0.8, 0,3)
        self.colors = [(0.3, 0.3, 0.3, 1), (0.7, 0.7, 0.7, 1)]
        self.startNew()

    def startNew(self):
        self.ground = render.attachNewNode('Land')

    def addBlock(self, pos):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(pos)
        self.color = self.getColor(int(pos[2]))
        self.block.setColor(self.color)

        self.block.setTag('at', str(pos))
        self.block.reparentTo(self.ground)
    
    def getColor(self, z):
        print(self.colors)
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def clear(self):
        self.ground.removeNode()
        self.startNew()
    
    
    def change(self):
        if self.glitch == 1 or self.glitch == 50:
            id = 5
        elif self.glitch == 49:
            id = random.randint(6, 7)
        else:
            id = random.randint(1,4)
        if id == 1:
            self.texture = 'block.png'
        elif id == 2:
            self.texture = 'stone.png'
        elif id == 3:
            self.texture = 'wood.png'
        elif id == 4:
            self.texture = 'kyrpich.png'
        elif id == 5:
            self.texture = 'matrix1.jpg'
        elif id == 6:
            self.texture = 'j.png'
        elif id == 7:
            self.texture = 'dio.png'

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0 
                line.split(' ')
                for z in line:
                    if z != ' ' and z != '\n':
                        for z0 in range(int(z)+1):
                            self.glitch = 3
                            self.change()
                            block = self.addBlock((x, y, z0))
                        x += 1
                y += 1
        return x,y

    def findBlocks(self, pos):
        return self.ground.findAllMatches('=at=' + str(pos))
    
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        if self.glitch != 1:
            self.glitch = 4
        self.change()
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z +1:
            self.addBlock(new)

    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        blocks = self.ground.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            self.glitch = random.randint(1, 50)
            # self.glitch = 49 #test JoJo reference
            for i in range(length):
                self.change()
                pos = pickle.load(fin)

                self.addBlock(pos)