# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 11:24:26 2024

@author: jakubziom
"""
import sys
from direct.showbase.ShowBase import ShowBase
import simplepbr
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, PointLight, DirectionalLight, LightAttrib
from direct.filter.CommonFilters import *
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerQueue, CollisionNode, BitMask32
from panda3d.core import CollisionRay
from panda3d.core import GeomNode
import random
from time import sleep

#      0a 1b 2c

Board0=['','','',''] 
Board1=['','','','']
Board2=['','','','']
Board3=['','','','']

BoardList=[Board0,Board1,Board2,Board3]

class MyApp(ShowBase):

    def __init__(self):
        super().__init__()
        
        #enable pbr and materials    
        pbr = simplepbr.init() 
        pbr.use_hardware_skinning = True
        pbr.msaa_samples = 8
        pbr.enable_shadows = True
        pbr.use_330 = True # export MESA_GL_VERSION_OVERRIDE="3.00 ES"
        pbr.use_normal_maps = True
        pbr.use_emission_maps = True
        pbr.use_occlusion_maps = True
        pbr.enable_fog = True
          
        
        self.isMaximizing=False
        
        #board
        self.BoardSize=1
             
        #values for checking win
        self.D1x=0
        self.D2x=0
        self.D1o=0
        self.D2o=0
        self.D1={'x':self.D1x,'o':self.D1o}
        self.D2={'x':self.D2x,'o':self.D2o}
        
        #values for checking draw
        #is x in diagonal line 1?
        self.D1Drawx=False
        #is o in diagonal line 1?
        self.D1Drawo=False
        #is x in diagonal line 2?
        self.D2Drawx=False
        #is o in diagonal line 2?
        self.D2Drawo=False
        #putting it together
        self.D1Draw={'x':self.D1Drawx,'o':self.D1Drawo}
        self.D2Draw={'x':self.D2Drawx,'o':self.D2Drawo}   
        self.HDrawCount=0
        self.VDrawCount=0
        
        
        self.D1Cx=0
        self.D1Co=0
        self.D1C={'x':self.D1Cx,'o':self.D1Co}
        
        self.D2Cx=0
        self.D2Co=0
        self.D2C={'x':self.D2Cx,'o':self.D2Co}
        
        #values for counting computer wins and loses
        self.D1DrawCx=False
        #is o in diagonal line 1?
        self.D1DrawCo=False
        #is x in diagonal line 2?
        self.D2DrawCx=False
        #is o in diagonal line 2?
        self.D2DrawCo=False
        #putting it together
        self.D1DrawC={'x':self.D1DrawCx,'o':self.D1DrawCo}
        self.D2DrawC={'x':self.D2DrawCx,'o':self.D2DrawCo}
        
        self.VCx=[0,0,0,0]
        self.VCo=[0,0,0,0]
        #putting it together
        self.VC={'x':self.VCx,'o':self.VCo}        
        
        self.VC1x=[0,0,0,0]
        self.VC1o=[0,0,0,0]
        #putting it together
        self.VC1={'x':self.VC1x,'o':self.VC1o}
             
        #coordinates for appearing marks in 3d
        self.col={'a':0,'b':1,'c':2,'d':3}
        self.row={'1':0,'2':-1,'3':-2,'4':-3}
        
        #coordinates for selecting existing marks
        self.col2={0:'a',1:'b',2:'c',3:'d'}
        self.row2={0:'1',1:'2',2:'3',3:'4'}        
        
        #which turn is now?
        self.TurnX=True
        #does the player won?
        self.win=False
        
        #number of marks in vertical lines (after player input)
        self.Vx=[0,0,0,0]
        self.Vo=[0,0,0,0]
        #putting it together
        self.V={'x':self.Vx,'o':self.Vo}
        
        #assigning each board piece a different value
        self.board3d={}
        
        #
        self.boardLoaded=False
        self.boardSelected=False 
        self.buttonsLoaded=False
            
        #assigning each X 3d or O 3d a different value
        self.mark3d={}
        
        #player input
        self.input1=''
        self.input2=''
        self.PlayerInput=[self.input1,self.input2]
        
        #mouse control script        
        pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        pickerRay = CollisionRay()
        pickerNode.addSolid(pickerRay)
        pickerNP.show()
        rayQueue = CollisionHandlerQueue()
        base.cTrav = CollisionTraverser()
        base.cTrav.addCollider(pickerNP, rayQueue)

        def pickObject():
            
            mpos = base.mouseWatcherNode.getMouse()
            pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            base.cTrav.traverse(render)
                
            if rayQueue.getNumEntries() > 0:
                rayQueue.sortEntries()
                entry = rayQueue.getEntry(0)
                pickedNP = entry.getIntoNodePath()
                if self.boardLoaded==False and self.boardSelected==False:
                    #detection of 3x3 button
                    if pickedNP.hasNetTag('bs3'):
                        self.BoardSize=3
                        base.camera.setPos(1.5,-1.5,8)
                        self.plnp0.setPos(1.5, 0.5, 1)
                        self.plnp1.setPos(1.5, -3.5, 1)
                        plight.setAttenuation(0.04)                        
                        self.boardSelected=True
                        
                        #for i in range(0,self.BoardSize):
                            #BoardList[i].insert(0,'')
                        #filling the lists to make vertical mark counters
                            #self.Vx.insert(0,0)
                            #self.Vo.insert(0,0)
                        
                        
                    #detection of 4x4 button
                    if pickedNP.hasNetTag('bs4'):
                        self.BoardSize=4  
                        base.camera.setPos(2,-2,10)
                        self.plnp0.setPos(2, 0.5, 1)        
                        self.plnp1.setPos(2, -4.5, 1)
                        plight.setAttenuation(0.03)
                        self.boardSelected=True
                        
                        #for i in range(0,self.BoardSize):
                            #BoardList[i].insert(0,'')
                        #filling the lists to make vertical mark counters
                            #self.Vx.insert(0,0)
                            #self.Vo.insert(0,0)
                        
                #detection of a board piece                                   
                for i in range(0,self.BoardSize):
                    for n in range(0,self.BoardSize):  
                        if pickedNP.hasNetTag(str([self.col2[i]]+[self.row2[n]])):
                            self.input1=str(self.col2[i])
                            self.input2=str(self.row2[n])

                self.diagonalWinMinus('x')
                self.diagonalWinMinus('o')  

                self.verticalWinMinus('x')
                self.verticalWinMinus('o')

                #inserting the marks
                if self.TurnX==True:
                    self.player(True, 'x')
                
            
                self.horizontalWin('x')
                self.horizontalWin('o')           
                self.diagonalWinPlus('x')              
                self.diagonalWinPlus('o')   
                            
                #this is for testing 
                print('D1',self.D1)
                print('D2',self.D2)
                      
                #vertical win
                self.verticalWinPlus('x')
                self.verticalWinPlus('o')
                self.draw('x')
                self.draw('o') 
                
                self.drawConditions()
                
                self.diagonalWinMinus('x')
                self.diagonalWinMinus('o')  

                self.verticalWinMinus('x')
                self.verticalWinMinus('o')
                
                
                #self.PlayerWinsMinusVC('o')
                #self.PlayerWinsMinusVC('x')
                #self.PlayerWinsMinusDC('o')
                #self.PlayerWinsMinusDC('x')
                    
                if self.BoardSize==3 and self.TurnX==False and self.boardLoaded==True:
                    self.computer(35)
                if self.BoardSize==4 and self.TurnX==False and self.boardLoaded==True:
                    self.computer(2)
 
                
                self.horizontalWin('x')
                self.horizontalWin('o')           
                self.diagonalWinPlus('x')              
                self.diagonalWinPlus('o')   
                            
                #this is for testing 
                print('D1',self.D1)
                print('D2',self.D2)
                      
                #vertical win
                self.verticalWinPlus('x')
                self.verticalWinPlus('o')
                self.draw('x')
                self.draw('o') 
                
                self.drawConditions()
                #this is for testing
                print('Vx',self.V['x'])
                print('Vo',self.V['o'])

                #this is for testing            
                print(Board0)
                print(Board1)
                print(Board2)
                print(Board3)
                                                                     
        #click event                                                                                                                   
        base.accept('mouse1', pickObject)
             
        #camera from the top
        
        base.camera.setPos(2,-1.5,8)
        base.camera.setHpr(0,-90,0)
        self.disableMouse()
        self.setBackgroundColor(0.75,0.54,0.4,1)
                     
        #lights
        plight = PointLight('plight')
        plight.setColor((0.55,0.33,0.22,1))
        plight.setAttenuation(0.03)
        
        self.plnp0 = render.attachNewNode(plight)

        self.plnp0.setPos(0.8, 0.5, 1)
        render.setLight(self.plnp0)
        
        plight = PointLight('plight')
        plight.setColor((0.55,0.33,0.22,1))
        plight.setAttenuation(0.03)
        self.plnp1 = render.attachNewNode(plight)
     
        self.plnp1.setPos(3.2, -4.5, 1)
        render.setLight(self.plnp1)
       
        alight = AmbientLight('alight')
        alight.setColor((0.1,0.07,0.05,1))
        plnp = render.attachNewNode(alight)
        plnp.setPos(0, 0, 0)
        render.setLight(plnp)
        
        #loads the background
        self.bg = loader.loadModel("models/bg.glb")
        self.bg.reparentTo(render)
        self.bg.setScale(1,1,1)
        self.bg.setPos(0,0,0)
        
        '''                    
        #enable Text with the mark coords (not in use now)
    def inputTextF(self):
        self.inputText = OnscreenText(text=(str(self.input1)+str(self.input2)),
                                      style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                      pos=(-0.8, -0.95), scale = .07)
        '''
        #inserting the marks  
    def player(self,turn,mark):
        if (not self.input1=='' and not self.input2=='' and self.TurnX==True
            #preventing from putting mark again in same place
            and BoardList[-self.row[self.input2]][self.col[self.input1]]=='' and self.win==False and self.boardLoaded==True):
            #adding mark 3d models
            #each have it's index in mark3d dictionary
            self.mark3d[str([self.input1]+[self.input2])+str(mark)]= loader.loadModel("models/"+ mark+".glb")
            self.mark3d[str([self.input1]+[self.input2])+str(mark)].reparentTo(render)
            self.mark3d[str([self.input1]+[self.input2])+str(mark)].setScale(1,1,1)
            self.mark3d[str([self.input1]+[self.input2])+str(mark)].setPos(self.col[self.input1],self.row[self.input2],0)
            #adding mark to the list
            BoardList[-self.row[self.input2]].pop(self.col[self.input1])
            BoardList[-self.row[self.input2]].insert(self.col[self.input1],str(mark))
            
            print(self.input1,self.input2)              
            self.input1=''
            self.input2='' 
            self.TurnX=False
            
            print(Board0)
            print(Board1)
            print(Board2)
            print(Board3)
            print(self.mark3d)

            print(self.TurnX)
            #creating the board in 3d
        if self.boardLoaded==False and self.boardSelected==True:

            self.bs3.removeNode()
            self.bs4.removeNode()
            for i in range(0,self.BoardSize):
                for n in range(0,self.BoardSize):
                    #loading the 3d model of a board piece
                    
                    self.board3d[str([self.col2[i]]+[self.row2[n]])]= loader.loadModel("models/boardPiece.glb")
                    self.board3d[str([self.col2[i]]+[self.row2[n]])].reparentTo(render)
                    self.board3d[str([self.col2[i]]+[self.row2[n]])].setScale(1,1,1)
                    self.board3d[str([self.col2[i]]+[self.row2[n]])].setPos(self.col[self.col2[i]],self.row[self.row2[n]],0)
                    #adding different tag for each piece to be recognizable by mouse ray
                    self.board3d[str([self.col2[i]]+[self.row2[n]])].setTag(str([self.col2[i]]+[self.row2[n]]),'')
            self.boardLoaded=True
            print(self.board3d)    
        
        #cleaning the lists after player won
        if self.win==True:  
            for i in range(0,self.BoardSize):
                for n in range(0,self.BoardSize):
                    if self.BoardSize==3:
                        self.plnp0.setPos(1.5, 0.5, 1)
                        self.plnp1.setPos(1.5, -3.5, 1)     
                    if self.BoardSize==4:
                        self.plnp0.setPos(2, 0.5, 1)
                        self.plnp1.setPos(2, -4.5, 1)       
                    #self.winText2.clearText()
                    BoardList[n][i]=''
                    self.board3d[str([self.col2[i]]+[self.row2[n]])].removeNode()
                    self.boardLoaded=False
                    try:                     
                        self.mark3d[str([self.col2[i]]+[self.row2[n]])+str('x')].removeNode()
                    except:
                        pass
                    try:
                        self.mark3d[str([self.col2[i]]+[self.row2[n]])+str('o')].removeNode()               
                    except:
                        pass
            self.TurnX=True
            self.win=False   
            self.boardSelected=False
            self.buttonsLoaded=False
            #loading the menu
        if self.boardSelected==False and self.buttonsLoaded==False:
                       
            base.camera.setPos(2,-1.5,8)
            self.plnp0.setPos(0.8, 0, 1)           
            self.plnp1.setPos(3.2, 0, 1)
            
            self.bs3 = loader.loadModel("models/bs3.glb")
            self.bs3.reparentTo(render)
            self.bs3.setScale(1,1,1)
            self.bs3.setPos(0,-1,0)
            self.bs3.setTag('bs3','')
                    
            self.bs4 = loader.loadModel("models/bs4.glb")
            self.bs4.reparentTo(render)
            self.bs4.setScale(1,1,1)
            self.bs4.setPos(2.4,-1,0)
            self.bs4.setTag('bs4','')            
            
            self.buttonsLoaded=True          
        else:
            print(self.TurnX)
            print('no input')
        return 
        
    def HorizontalWinC(self,mark):
        for i in range(0,self.BoardSize):
            #print(BoardList[i].count(mark))
            #checking horizontal win
            if BoardList[i].count(mark)==self.BoardSize:
                return True
            
    def PlayerWinsVC(self,mark):
        for i in range(0,self.BoardSize):
            self.VC[mark][i]=0
            
        for i in range(0,self.BoardSize):
            #counting marks x or o in vertical lines
            for n in range(0,self.BoardSize):
                if BoardList[n][i]==mark:
                    self.VC[mark][i]+=1
                    #print('VC'+str(self.VC))
                    if self.VC[mark][i]==self.BoardSize:
                        return True
            
    def PlayerWinsD1C(self,mark):
        self.D1C[mark]=0  
        for i in range(0,self.BoardSize):
            if BoardList[i][i]==mark:
                self.D1C[mark]+=1 
                #print('D1C'+str(self.D1C))
                if self.D1C[mark]==self.BoardSize:
                    return True
        
    def PlayerWinsD2C(self,mark):    
        self.D2C[mark]=0   
        
        for i in range(0,self.BoardSize):
            if BoardList[self.BoardSize-1-i][i]==mark:
                self.D2C[mark]+=1 
                #print('D2C'+str(self.D2C)) 
                if self.D2C[mark]==self.BoardSize:
                    return True 
    
    def DrawC(self):
        self.D1DrawC['o']=False
        self.D1DrawC['x']=False
        self.D2DrawC['o']=False        
        self.D2DrawC['x']=False
 
        for i in range(0,self.BoardSize):
            if BoardList[i][i]=='o':
                self.D1DrawC['o']=True  
                #print('D1DrawC',self.D1DrawC)
                
        for i in range(0,self.BoardSize):
            if BoardList[i][i]=='x':
                self.D1DrawC['x']=True  
                #print('D1DrawC',self.D1DrawC)
        #this is for testing 
        
        #diagonal draw 2
        for i in range(0,self.BoardSize):
            if BoardList[self.BoardSize-1-i][i]=='o':
                self.D2DrawC['o']=True 
                #print('D2DrawC',self.D2DrawC)
                
        for i in range(0,self.BoardSize):
            if BoardList[self.BoardSize-1-i][i]=='x':
                self.D2DrawC['x']=True 
                #print('D2DrawC',self.D2DrawC)
        #this is for testing
        
        for i in range(0,self.BoardSize):
            self.VC1['o'][i]=0
            self.VC1['x'][i]=0
        for i in range(0,self.BoardSize):
            #counting marks x or o in vertical lines
            for n in range(0,self.BoardSize):
                if BoardList[n][i]=='o':
                    self.VC1['o'][i]+=1   
                    
        for i in range(0,self.BoardSize):
            #counting marks x or o in vertical lines
            for n in range(0,self.BoardSize):
                if BoardList[n][i]=='x':
                    self.VC1['x'][i]+=1 
                
        self.VDrawCountC=0
        self.HDrawCountC=0
        #vertical draw
        for i in range(0,self.BoardSize):
            if self.VC1['x'][i]>=1 and self.VC1['o'][i]>=1:
                self.VDrawCountC+=1
                #print('VDrawCountC',self.VDrawCountC)
        #horizonal draw

        for i in range(0,self.BoardSize):
            if BoardList[i].count('x')>=1 and BoardList[i].count('o')>=1:
                self.HDrawCountC+=1
                #print('HDrawCountC',self.HDrawCountC)
        #this is for testing
        
        if (self.D1DrawC['x']==True and self.D1DrawC['o']==True
            and self.D2DrawC['x']==True and self.D2DrawC['o']==True
            and self.VDrawCountC==self.BoardSize
            and self.HDrawCountC==self.BoardSize):      
            return True          
        
    def insertLetter(self,mark,n,i):
        if self.boardLoaded==True and self.win==False:
         
            if not (BoardList[n][i]=='x' or BoardList[n][i]=='o'):    
                self.mark3d[str([self.col2[i]]+[self.row2[n]])+str(mark)]= loader.loadModel("models/"+ mark+".glb")
                self.mark3d[str([self.col2[i]]+[self.row2[n]])+str(mark)].reparentTo(render)
                self.mark3d[str([self.col2[i]]+[self.row2[n]])+str(mark)].setScale(1,1,1)
                self.mark3d[str([self.col2[i]]+[self.row2[n]])+str(mark)].setPos(self.col[self.col2[i]],self.row[self.row2[n]],0)
                #adding mark to the list
                BoardList[n].pop(i)
                BoardList[n].insert(i, mark)
            else:
                exit()
                
        self.TurnX=True           
        #if self.win==True:
            #self.winText2.clearText()   
        return
      
    def computer(self, max_depth):
        a=random.randint(0,1)
        b=random.randint(0,1)
        self.max_score1=-10000
        self.best_moveR = 0
        self.best_moveC = 0
        self.random_moveR = random.randint(0, self.BoardSize-1) 
        self.random_moveC = random.randint(0, self.BoardSize-1) 
        
        for i in range(0,self.BoardSize):
            for n in range(0,self.BoardSize):
                if BoardList[n][i]=='':
                    
                    BoardList[n][i]='o'
                    self.score1 = self.minimax(0,False,max_depth)
                 
                    BoardList[n][i]=''
                    if self.score1 > self.max_score1:
                        self.max_score1 = self.score1
                        self.best_moveR = n
                        self.best_moveC = i
                        print(self.best_moveR)
                        print(self.best_moveC)
   
        '''
        try: 
            self.insertLetter('o', self.random_moveR,self.random_moveC)
        except:
            try:
                self.insertLetter('o', self.random_moveR,self.random_moveR) 
            except:
                self.insertLetter('o', self.best_moveR,self.best_moveC)
        '''   
        '''
        self.insertLetter('o', self.best_moveR,self.best_moveC)
        '''
        if a==0:
            try: 
                self.insertLetter('o', self.random_moveR,self.random_moveC)
            except:
                self.insertLetter('o', self.best_moveR,self.best_moveC)
        if a==1:
            if b==0:
                try:
                    self.insertLetter('o', 1, 1)
                except:
                    self.insertLetter('o', self.best_moveR,self.best_moveC)   
            if b==1 :
                try:
                    self.insertLetter('o', 1, 2)
                except:
                    self.insertLetter('o', self.best_moveR,self.best_moveC)
             
        return self.best_moveR,self.best_moveC
  
    
    def minimax(self, depth, isMaximizing,max_depth):
         
        if self.HorizontalWinC('o') or self.PlayerWinsVC('o') or self.PlayerWinsD1C('o') or self.PlayerWinsD2C('o'):
            return 1
             
        if self.HorizontalWinC('x') or self.PlayerWinsVC('x') or self.PlayerWinsD1C('x') or self.PlayerWinsD2C('x'): 
            return -1
        
        if self.DrawC() or depth==max_depth:
            return 0
               
        if isMaximizing:
            self.max_score2 = -10000
            
            for n in range(0,self.BoardSize):
                for i in range(0,self.BoardSize):
                    if BoardList[n][i]=='':                
                        BoardList[n][i]='o'
                        self.score2 = self.minimax(depth+1,False,max_depth)          
                        BoardList[n][i]=''
                        if self.score2 > self.max_score2:
                            self.max_score2 = self.score2
            return self.max_score2
            
        else:
            self.max_score3 = 8000
            for n in range(0,self.BoardSize):
                for i in range(0,self.BoardSize):
                    if BoardList[n][i]=='':       
                        BoardList[n][i]='x'
                        self.score3 = self.minimax(depth+1,True,max_depth)
                        BoardList[n][i]=''
                        if self.score3 < self.max_score3:
                            self.max_score3 = self.score3
            return self.max_score3  
    
    #moves the lights up after the player won
    def lightsWin(self):
        
        if self.BoardSize==3:
            
            self.plnp0.setPos(1.5, 0.5, 4)
            self.plnp1.setPos(1.5, -3.5, 4)        
        
        if self.BoardSize==4:
     
            self.plnp0.setPos(2, 0.5, 4)
            self.plnp1.setPos(2, -4.5, 4)
        return
    
    def diagonalWinMinus(self,mark):
        #diagonal win 1
        for i in range(0,self.BoardSize):
            if BoardList[i][i]==mark:
                self.D1[mark]+=-1 
        #diagonal win 2
        for i in range(0,self.BoardSize):
            if BoardList[self.BoardSize-1-i][i]==mark:
                self.D2[mark]+=-1
        return
  
    def verticalWinMinus(self,mark):
        #vertical win
        #X
        for i in range(0,self.BoardSize):
            #counting marks x or o in vertical lines
            for n in range(0,self.BoardSize):
                if BoardList[n][i]==mark:
                    self.V[mark][i]+=-1
        return

    def winText(self,mark,text):                
        #self.winText2 = OnscreenText(text=mark + text,
                    #style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                    #pos=(0, 0), scale = .2)  
        return
        
    def horizontalWin(self,mark):
        for i in range(0,self.BoardSize):
            #checking horizontal win
            if (BoardList[i].count(mark)==self.BoardSize):
                #moving marks up, trying each line horizontally
                try:
                    for i in range(0,self.BoardSize): 
                        self.mark3dWin(i, 0, mark,0.8)
                except:
                    for i in range(0,self.BoardSize):
                        for n in range(0,self.BoardSize):
                            try:
                                self.mark3dWin(n, i, mark,0)
                            except:
                                pass
                    try:
                        for i in range(0,self.BoardSize):
                            self.mark3dWin(i, 1, mark,0.8)
                    except:
                        for i in range(0,self.BoardSize):
                            for n in range(0,self.BoardSize):
                                try:
                                    self.mark3dWin(n, i, mark,0)
                                except:
                                    pass
                        try:
                            for i in range(0,self.BoardSize):
                                self.mark3dWin(i, 2, mark,0.8) 
                        except:
                            for i in range(0,self.BoardSize):
                                for n in range(0,self.BoardSize):
                                    try:
                                        self.mark3dWin(n, i, mark,0)
                                    except:
                                        pass
                            for i in range(0,self.BoardSize): 
                                self.mark3dWin(i, 3, mark,0.8)
                #win                    
                self.lightsWin()
                self.winText(mark,' wins!')
                print(mark+' wins!')
                self.win=True
        return
    
    def diagonalWinPlus(self,mark):
        for i in range(0,self.BoardSize):
            if BoardList[i][i]==mark:
                self.D1[mark]+=1 
                
        if self.D1[mark]==self.BoardSize and self.win==False:
            #win
            self.winText(mark,' wins!')
            self.win=True
            self.lightsWin()
            #moving marks up
            for i in range(0,self.BoardSize):
                self.mark3dWin(i, i, mark,0.8)
    
        #diagonal win 2    
        for i in range(0,self.BoardSize):
            if BoardList[self.BoardSize-1-i][i]==mark:
                self.D2[mark]+=1
                
        if self.D2[mark]==self.BoardSize and self.win==False:
            #win
            self.winText(mark,' wins!')
            self.win=True
            self.lightsWin()
            #moving marks up
            for i in range(0,self.BoardSize):
                self.mark3dWin(self.BoardSize-1-i, i,mark,0.8)                          
        return

    def verticalWinPlus(self,mark):
        for i in range(0,self.BoardSize):
            #counting marks x or o in vertical lines
            for n in range(0,self.BoardSize):
                if BoardList[n][i]==mark:
                    self.V[mark][i]+=1
        for i in range(0,self.BoardSize):
            if self.V[mark][i]==self.BoardSize and self.win==False:
                #moving the marks up, trying each line vertically
                try:
                    for i in range(0,self.BoardSize):
                        self.mark3dWin(0, i, mark,0.8)
                except:
                    for i in range(0,self.BoardSize):
                        for n in range(0,self.BoardSize):
                            try:
                                self.mark3dWin(n, i, mark,0)
                            except:
                                pass             
                    try:
                        for i in range(0,self.BoardSize):
                            self.mark3dWin(1, i, mark,0.8)
                    except:
                        for i in range(0,self.BoardSize):
                            for n in range(0,self.BoardSize):
                                try:
                                    self.mark3dWin(n, i, mark,0)
                                except:
                                    pass
                        try:
                            for i in range(0,self.BoardSize):
                                self.mark3dWin(2, i, mark,0.8)
                        except:
                            for i in range(0,self.BoardSize):
                                for n in range(0,self.BoardSize):
                                    try:
                                        self.mark3dWin(n, i, mark,0)
                                    except:
                                        pass 
                            for i in range(0,self.BoardSize):
                                self.mark3dWin(3, i, mark,0.8)
                #win
                self.lightsWin()
                self.winText(mark,' wins!')
                self.win=True
        return

        #moves the marks after player won (zCoord)
    def mark3dWin(self,col,row,mark,zCoord):
        
        self.mark3d[str([self.col2[col]]+[self.row2[row]])+str(mark)].setPos(self.col[self.col2[col]],self.row[self.row2[row]],zCoord)
        self.board3d[str([self.col2[col]]+[self.row2[row]])].setPos(self.col[self.col2[col]],self.row[self.row2[row]],zCoord)
        return

    def draw(self,mark):
        #diagonal draw 1
        self.D1Draw[mark]=False
        self.D2Draw[mark]=False
        for i in range(0,self.BoardSize):
            if BoardList[i][i]==mark:
                self.D1Draw[mark]=True   
        #this is for testing 
        
        print('D1Draw',self.D1Draw)
        
        #diagonal draw 2
        for i in range(0,self.BoardSize):
            if BoardList[self.BoardSize-1-i][i]==mark:
                self.D2Draw[mark]=True 
        #this is for testing
        
        print('D2Draw',self.D2Draw)
        
        self.VDrawCount=0
        self.HDrawCount=0
        #vertical draw
        for i in range(0,self.BoardSize):
            if self.V['x'][i]>=1 and self.V['o'][i]>=1:
                self.VDrawCount+=1
        #horizonal draw
        for i in range(0,self.BoardSize):
            if BoardList[i].count('x')>=1 and BoardList[i].count('o')>=1:
                self.HDrawCount+=1
        #this is for testing
           
        print('VDrawCount',self.VDrawCount)
        print('HDrawCount',self.HDrawCount)        
        return
        
    def drawConditions(self):
        #draw conditions
        if (self.D1Draw['x']==True and self.D1Draw['o']==True
            and self.D2Draw['x']==True and self.D2Draw['o']==True
            and self.VDrawCount==self.BoardSize
            and self.HDrawCount==self.BoardSize):      
            self.win=True
            self.winText('','draw!')          
        return
            
app = MyApp()
app.run()