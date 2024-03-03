from game.logic.base import BaseLogic
from game.models import Board, GameObject
import math, time
class FirstToTheKeyFirstToTheEggBot(BaseLogic):
    
    targetX = 99
    targetY = 99
    tele1_step = 99
    tele1_X = 99
    tele1_Y = 99
    tele2_step = 99
    tele2_X = 99
    tele2_Y = 99
    
    def __init__(self):
        self.targetX = 99
        self.targetY = 99
        self.tele1_step = 99
        self.tele1_X = 99
        self.tele1_Y = 99
        self.tele2_step = 99
        self.tele2_X = 99
        self.tele2_Y = 99
        
    def getObjectsPosition(self,board_bot:GameObject,board:Board):
        start = time.time()
        target_X = 99
        target_Y = 99
        
        currX = board_bot.position.x
        currY = board_bot.position.y
        
        diamond_min_step = 99
        shortest_diamond_X = 99
        shortest_diamond_Y = 99
        n_diamond = 0
        
        isTackle = False
        other_bot_to_target_diamond_step = 99
        # shortest_bot_X = 99
        # shortest_bot_Y = 99
        
        button_step = 99
        button_X = 99
        button_Y = 99
        button_radar = 3
        diamond_in_button_radar = 0
        
        isTele1 = True
        # self.tele1_step = 99
        # self.tele1_X = 99
        # self.tele1_Y = 99
        
        # self.tele2_step = 99
        # self.tele2_X = 99
        # self.tele2_Y = 99
        print(board.game_objects)
        for object in board.game_objects:
            
            if object.type == "DiamondGameObject":
                n_diamond+=1
                if abs(object.position.x-button_X)+abs(object.position.y-button_Y) <= button_radar:
                    diamond_in_button_radar+=1
                # Teleporter
                step_in_tele1 = (abs(currX-self.tele1_X)+abs(currY-self.tele1_Y))+(abs(self.tele2_X-object.position.x)+abs(self.tele2_Y-object.position.y))
                step_in_tele2 = (abs(currX-self.tele2_X)+abs(currY-self.tele2_Y))+(abs(self.tele1_X-object.position.x)+abs(self.tele1_Y-object.position.y))
                # Original
                temp_step = abs(object.position.y-board_bot.position.y) + abs(object.position.x-board_bot.position.x)
                diamond_min_step_temp = min(temp_step,step_in_tele1,step_in_tele2)
                if diamond_min_step_temp < diamond_min_step:
                    diamond_min_step = diamond_min_step_temp
                    if diamond_min_step == step_in_tele1:
                        shortest_diamond_X = self.tele1_X
                        shortest_diamond_Y = self.tele1_Y
                    elif diamond_min_step == step_in_tele2:
                        shortest_diamond_X = self.tele2_X
                        shortest_diamond_Y = self.tele2_Y
                    else:
                        shortest_diamond_X = object.position.x
                        shortest_diamond_Y = object.position.y
                    
            # elif object.type == "BotGameObject" and object.position.x != currX and object.position.y != currY:
            #     try:
            #         if object.properties.diamonds > 0:
            #             if abs(object.position.x-currX) == 1 or abs(object.position.y-currY) == 1:
            #                 target_X = object.position.x
            #                 target_Y = object.position.y
            #                 isTackle = True
            #     except:
            #         print("EXCEPTION RAGHHHHHHHHHH")
            #     else:
            #         break
            #         temp_step_to_target_diamond = abs(object.position.x-shortest_diamond_X)+abs(object.position.y-shortest_diamond_Y)
            #         if temp_step_to_target_diamond < other_bot_to_target_diamond_step:
            #             other_bot_to_target_diamond_step = temp_step_to_target_diamond
                    
            elif object.type == "TeleportGameObject":
                if isTele1:
                    self.tele1_X = object.position.x
                    self.tele1_Y = object.position.y
                    self.tele1_step = abs(object.position.x-currX)+abs(object.position.y-currY)
                    isTele1 = False
                else:
                    self.tele2_X = object.position.x
                    self.tele2_Y = object.position.y
                    self.tele2_step = abs(object.position.x-currX)+abs(object.position.y-currY)
                    
            elif object.type == "DiamondButtonGameObject":
                button_X = object.position.x
                button_Y = object.position.y
                button_step = abs(currX-button_X)+abs(currY-button_Y)
        
        
        if not isTackle:
            if n_diamond == 1:
                # if (diamond_min_step < other_bot_to_target_diamond_step):
                #     target_X = shortest_diamond_X
                #     target_Y = shortest_diamond_Y
                # else:
                #     target_X = 7
                #     target_Y = 7
                if board_bot.properties.diamonds == 0:
                    step_to_center = abs(7-currX)+abs(7-currY)
                    step_to_base = abs(board_bot.properties.base.x-currX)+abs(board_bot.properties.base.y-currY)
                    if step_to_base < step_to_center and step_to_base < button_step:
                        target_X = board_bot.properties.base.x
                        target_Y = board_bot.properties.base.y
                    elif step_to_center < button_step:
                        target_X = 7
                        target_Y = 7
                    else:
                        target_X = button_X
                        target_Y = button_Y
                else:
                    target_X = board_bot.properties.base.x
                    target_Y = board_bot.properties.base.y
            else:
                min_step = min(diamond_min_step,button_step)
                print("N BUTTON RADAR", diamond_in_button_radar)
                if min_step == button_step and diamond_in_button_radar == 0:
                    print("CHASE BUTTON")
                    target_X = button_X
                    target_Y = button_Y
                else:
                    print("CHASE DIAMOND")
                    target_X = shortest_diamond_X
                    target_Y = shortest_diamond_Y
                
        end = time.time()
        print("TARGET INIT", target_X,target_Y)
        print("DURASI", (end-start)*1000,"ms")
        return (target_X, target_Y, isTackle)
        
    def tackle(self,board_bot:GameObject,board:Board):
        currX = board_bot.position.x
        currY = board_bot.position.y
        
        isTackle = False
        dx = 0
        dy = 0
        
        for bot in board.bots:
            if bot.properties.diamonds > 2:
                tackleX = bot.position.x-currX
                tackleY = bot.position.y-currY
                if (tackleX == 1 or tackleX == -1) and tackleY==0:
                    dx = tackleX
                    isTackle = True
                    break
                if (tackleY == 1 or tackleY == -1) and tackleX==0:
                    dy = tackleY
                    isTackle = True
                    break
        return (dx,dy,isTackle)
            
    def next_move(self, board_bot: GameObject, board: Board):
        start = time.time()
        if board_bot.properties.diamonds < 2:
            tackle = self.tackle(board_bot,board)
            if tackle[2]:
                return tackle[0], tackle[1]
        tempXY = self.getObjectsPosition(board_bot,board)
        delta_x = 0
        delta_y = 0
        print()
        threshold = 4
        count = 0
        self.targetX = tempXY[0]
        self.targetY = tempXY[1]
        startw = time.time()
        while(delta_x == 0 and delta_y == 0 and count < threshold):
            if tempXY[2]:
                print("TACKLE CUY")
                if(self.targetX!=99):
                    if self.targetX < currX:
                        delta_x = -1
                        break
                    elif self.targetX > currX:
                        delta_x = 1
                        break
                    else:
                        self.targetX = 99
                                    
                if(self.targetY!=99):
                    if self.targetY < currY:
                        delta_y = -1
                        print("LIATT1")
                        break
                    elif self.targetY > currY:
                        print("LIATT2")
                        delta_y = 1
                        break
                    else:
                        self.targetY = 99
            else:           
                currX = board_bot.position.x
                currY = board_bot.position.y
                print("CURR LOC", board_bot.position)
                print("TARGET X",self.targetX)
                print("TARGET Y",self.targetY)
                print("dx", delta_x)
                print("dy", delta_y)
                original_step = abs(board_bot.position.x-board_bot.properties.base.x)+abs(board_bot.position.y-board_bot.properties.base.y)
                tele1_step = (abs(currX-self.tele1_X)+abs(currY-self.tele1_Y))+(abs(board_bot.properties.base.x-self.tele2_X)+abs(board_bot.properties.base.y-self.tele2_Y))
                tele2_step = (abs(currX-self.tele2_X)+abs(currY-self.tele2_Y))+(abs(board_bot.properties.base.x-self.tele1_X)+abs(board_bot.properties.base.y-self.tele1_Y))
                min_target_step = min(original_step,tele1_step,tele2_step)
                if ((((board_bot.properties.milliseconds_left//1000))-min_target_step) <= 2):
                    print("ENDGAME")
                    if min_target_step == tele1_step:
                        self.targetX = self.tele1_X
                        self.targetY = self.tele1_Y
                    elif min_target_step == tele2_step:
                        self.targetX = self.tele2_X
                        self.targetY = self.tele2_Y
                    else:
                        self.targetX = board_bot.properties.base.x
                        self.targetY = board_bot.properties.base.y
                        
                    if(self.targetX!=99):
                        if self.targetX < currX:
                            delta_x = -1
                            break
                        elif self.targetX > currX:
                            delta_x = 1
                            break
                        else:
                            self.targetX = 99
                                        
                    if(self.targetY!=99):
                        if self.targetY < currY:
                            delta_y = -1
                            print("LIATT1")
                            break
                        elif self.targetY > currY:
                            print("LIATT2")
                            delta_y = 1
                            break
                        else:
                            self.targetY = 99
                elif (board_bot.properties.diamonds > 3):
                    print("DIAMONDS > 3")
                    original_step = abs(currX-board_bot.properties.base.x)+abs(currY-board_bot.properties.base.y)
                    tele1_step = (abs(currX-self.tele1_X)+abs(currY-self.tele1_Y))+(abs(board_bot.properties.base.x-self.tele2_X)+abs(board_bot.properties.base.y-self.tele2_Y))
                    tele2_step = (abs(currX-self.tele2_X)+abs(currY-self.tele2_Y))+(abs(board_bot.properties.base.x-self.tele1_X)+abs(board_bot.properties.base.y-self.tele1_Y))
                    min_target_step = min(original_step,tele1_step,tele2_step)
                    if min_target_step == tele1_step:
                        self.targetX = self.tele1_X
                        self.targetY = self.tele1_Y
                    elif min_target_step == tele2_step:
                        self.targetX = self.tele2_X
                        self.targetY = self.tele2_Y
                    else:  
                        self.targetX = board_bot.properties.base.x
                        self.targetY = board_bot.properties.base.y
                    
                    if(self.targetX!=99):
                        if self.targetX < currX:
                            delta_x = -1
                            break
                        elif self.targetX > currX:
                            delta_x = 1
                            break
                        else:
                            self.targetX = 99
                                        
                    if(self.targetY!=99):
                        if self.targetY < currY:
                            delta_y = -1
                            # print("LIATT1")
                            break
                        elif self.targetY > currY:
                            # print("LIATT2")
                            delta_y = 1
                            break
                        else:
                            self.targetY = 99
                elif(board_bot.properties.diamonds > 2):
                    print("DIAMOND > 0")
                    # print("MASOK")
                    # print("CURR LOC", board_bot.position)
                    # print("TARGET X",self.targetX)
                    # print("TARGET Y",self.targetY)
                    # targetXY = tempXY
                    target_step = abs(tempXY[0]-currX)+abs(tempXY[1]-currY)
                    # print("DIAMOND",tempXY[0]+tempXY[1])
                    original_step = abs(currX-board_bot.properties.base.x)+abs(currY-board_bot.properties.base.y)
                    tele1_step = (abs(currX-self.tele1_X)+abs(currY-self.tele1_Y))+(abs(board_bot.properties.base.x-self.tele2_X)+abs(board_bot.properties.base.y-self.tele2_Y))
                    tele2_step = (abs(currX-self.tele2_X)+abs(currY-self.tele2_Y))+(abs(board_bot.properties.base.x-self.tele1_X)+abs(board_bot.properties.base.y-self.tele1_Y))
                    min_target_step = min(original_step,tele1_step,tele2_step,target_step)
                    # print("BASE", base_step)
                    if min_target_step == target_step:
                        print("CHASE TARGET")
                        self.targetX = tempXY[0]
                        self.targetY = tempXY[1]
                        
                    elif min_target_step == tele1_step:
                        print("CHASE TELE1")
                        self.targetX = self.tele1_X
                        self.targetY = self.tele1_Y
                    elif min_target_step == tele2_step:
                        print("CHASE TELE2")
                        self.targetX = self.tele2_X
                        self.targetY = self.tele2_Y
                    else:  
                        print("CHASE BASE")
                        self.targetX = board_bot.properties.base.x
                        self.targetY = board_bot.properties.base.y
                        
                    if(self.targetX!=99):
                        if self.targetX < currX:
                            delta_x = -1
                            break
                        elif self.targetX > currX:
                            delta_x = 1
                            break
                        else:
                            self.targetX = 99
                                        
                    if(self.targetY!=99):
                        if self.targetY < currY:
                            delta_y = -1
                            print("LIATT1")
                            break
                        elif self.targetY > currY:
                            print("LIATT2")
                            delta_y = 1
                            break
                        else:
                            self.targetY = 99
                    
                if(self.targetX!=99):
                    if self.targetX < currX:
                        delta_x = -1
                        break
                    elif self.targetX > currX:
                        delta_x = 1
                        break
                    else:
                        self.targetX = 99
                                    
                if(self.targetY!=99):
                    if self.targetY < currY:
                        delta_y = -1
                        print("LIATT1")
                        break
                    elif self.targetY > currY:
                        print("LIATT2")
                        delta_y = 1
                        break
                    else:
                        self.targetY = 99
                    
                # else:
                #     # n_diamond = len(board.diamonds)
                #     # board_bot : bot kita
                #     # print("POSITION",board_bot.position)
                #     # print("LALALA",board.bots)
                #     # print()
                #     # shortestYfromCurr = self.shortestVertical(board_bot,board)
                #     # shortestXfromCurr = self.shortestHorizontal(board_bot,board)
                    
                #     # if shortestXfromCurr != 99 and shortestYfromCurr != 99:
                #     #     if (abs(shortestXfromCurr[0]) < abs(shortestYfromCurr[0])):
                #     #         self.targetX = shortestXfromCurr[1]
                #     #     else:
                #     #         self.targetY = shortestYfromCurr[1]
                #     # elif shortestXfromCurr!=99:
                #     #     self.targetX = shortestXfromCurr[1]
                        
                #     # if n_diamond > 0:
                #     targetXY = tempXY
                #     self.targetX = targetXY[0]
                #     self.targetY = targetXY[1]
                #     if(self.targetX!=99):
                #         if self.targetX < currX:
                #             delta_x = -1
                #             break
                #             # if(currX-1 == self.targetX):
                #             #     self.targetX = 99
                #         elif self.targetX > currX:
                #             delta_x = 1
                #             break
                #             # if(currX+1 == self.targetX):
                #             #     self.targetX = 99
                #         else:
                #             self.targetX = 99
                            
                #     elif(self.targetY!=99):
                #         if self.targetY < currY:
                #             delta_y = -1
                #             break
                #             # if(currY-1 == self.targetY):
                #             #     self.targetY = 99
                #         elif self.targetY > currY:
                #             delta_y = 1
                #             break
                #             # if(currY+1 == self.targetY):
                #             #     self.targetY = 99
                #         else:
                #             self.targetY = 99
                        
            count+=1    
                # elif (board_bot.position.y == 0):
                #     delta_y = 1
                #     break
                #     # self.isUp = False
                # elif (board_bot.position.y == 14):
                #     delta_y = -1
                #     # self.isUp = True
                # elif (board_bot.position.x == 0):
                #     delta_x = 1
                # elif (board_bot.position.x == 14):
                #     delta_x = -1
                # else:
                #     delta_y = 1
                    
                # elif(board_bot.position.y <= board_bot.properties.base.y and board_bot.properties.diamonds==1):
                #     delta_y = 1
                # elif(board_bot.position.y > board_bot.properties.base.y and board_bot.properties.diamonds==1):
                #     delta_y = -1
                
                # elif(self.isUp):
                #     delta_y = -1
                # else:
                #     delta_y = 1
        endw = time.time()
        print("DUR WHILE", (endw-startw)*1000,"ms")
        print("RETURN1",delta_x,delta_y)
        
        if (delta_x == delta_y):
            if currX == 0:
                delta_x = 1
                delta_y = 0
            elif currX == 14:
                delta_x = -1
                delta_y = 0
            elif currY == 0:
                delta_x = 0
                delta_y = 1
            elif currY == 14:
                delta_x = 0
                delta_y = -1
            else:
                delta_x = 1
                delta_y = 0
                
        end = time.time()
        print("RETURN",delta_x,delta_y)
        print("TOTAL DUR", (end-start)*1000,"ms")
        return delta_x, delta_y
    