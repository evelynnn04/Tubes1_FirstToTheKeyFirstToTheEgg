from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
import time 
from ..util import get_direction


class botFed(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
    def goHome(self,board_bot: GameObject, board: Board):
        goal = board_bot.properties.base
        current_position = board_bot.position
        teleporter = self.teleporter(board)
        stepToBase = abs(current_position.x - goal.x) + abs(current_position.y - goal.y)
        stepToTeleporter = abs(teleporter[0].position.x - current_position.x) + abs(teleporter[0].position.y - current_position.y) + abs(teleporter[1].position.x - goal.x) + abs(teleporter[1].position.y - goal.y)
        stepToTeleporter2 = abs(teleporter[1].position.x - current_position.x) + abs(teleporter[1].position.y - current_position.y) + abs(teleporter[0].position.x - goal.x) + abs(teleporter[0].position.y - goal.y)
        stepToTele = min(stepToTeleporter,stepToTeleporter2)
        if stepToTele < stepToBase and stepToTele == stepToTeleporter:
            goal = teleporter[0].position
        elif stepToTele < stepToBase and stepToTele == stepToTeleporter2:
            goal = teleporter[1].position
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            goal.x,
            goal.y
        )
        return delta_x, delta_y
    
    def shortestDiamondToBot(self,board_bot: GameObject,board: Board):
        # Sebelumnya harus divalidasi dulu kalau jumlah diamond pada board > 0
        if board_bot.properties.diamonds == 4:
            min_step = 99
            x = 99
            y = 99
            for diamond in board.diamonds:
                if diamond.properties.points == 1:
                    temp_step = abs(diamond.position.y-board_bot.position.y) + abs(diamond.position.x-board_bot.position.x)
                    if temp_step < min_step:
                        x = diamond.position.x
                        y = diamond.position.y
                        min_step = temp_step
            coor = Position(y,x)
        else:
            min_step = abs(board.diamonds[0].position.y-board_bot.position.y) + abs(board.diamonds[0].position.x-board_bot.position.x)
            x = board.diamonds[0].position.x
            y = board.diamonds[0].position.y
            for diamond in board.diamonds:
                temp_step = abs(diamond.position.y-board_bot.position.y) + abs(diamond.position.x-board_bot.position.x)
                if temp_step < min_step:
                    x = diamond.position.x
                    y = diamond.position.y
                    min_step = temp_step
            coor = Position(y,x)
        return (coor, min_step)
    
    def teleporter(self, board: Board):
        teleporter = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        return teleporter

    def shortestDiamondToBase(self, board_bot: GameObject, board: Board):
        min_step = abs(board.diamonds[0].position.y-board_bot.properties.base.y) + abs(board.diamonds[0].position.x-board_bot.properties.base.x)
        x = board.diamonds[0].position.x
        y = board.diamonds[0].position.y
        for diamond in board.diamonds:
            temp_step = abs(diamond.position.y-board_bot.properties.base.y) + abs(diamond.position.x-board_bot.properties.base.x)
            if temp_step < min_step:
                x = diamond.position.x
                y = diamond.position.y
                min_step = temp_step
        coor = Position(y,x)
        return (coor, min_step)
    
    def goTo(self,board_bot: GameObject, target: Position):
        current = board_bot.position
        return get_direction(current.x, current.y, target.x, target.y)
    
    def shortestDiamondAndBaseMove(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        minStepBaseToDiamond = self.shortestDiamondToBase(board_bot,board)[1] # step dari base ke diamond
        minStepBase = abs(board_bot.properties.base.y-board_bot.position.y) + abs(board_bot.properties.base.x-board_bot.position.x) # step ke base
        minStepDiamondToBot = self.shortestDiamondToBot(board_bot, board)[1] # step ke diamond terdekat dari bot
        # Analyze new state
        if props.diamonds == 5:
            delta_x, delta_y =  self.goHome(board_bot, board)
        elif props.diamonds > 0 and (min(minStepBase,minStepBaseToDiamond) <= minStepDiamondToBot):
            if minStepBase < minStepBaseToDiamond:
                delta_x, delta_y = self.goHome(board_bot, board)
            else:
                delta_x, delta_y = self.goTo(board_bot, self.shortestDiamondToBase(board_bot, board)[0])
        else:
            delta_x, delta_y =  self.goTo(board_bot,self.shortestDiamondToBot(board_bot,board)[0])
        return delta_x, delta_y
    
    def timeLeftMove(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        if props.diamonds >= 3:
            delta_x, delta_y = self.goHome(board_bot, board)
        elif board_bot.properties.milliseconds_left <= 10000:
            if props.diamonds >= 1:
                delta_x, delta_y = self.goHome(board_bot, board)
            else:
                delta_x, delta_y = self.goTo(board_bot,self.shortestDiamondToBase(board_bot, board)[0])
        else:
            delta_x, delta_y = self.goTo(board_bot,self.shortestDiamondToBase(board_bot,board)[0])
        return delta_x, delta_y

    def next_move(self, board_bot: GameObject, board: Board):
        start = time.time()
        timeLeft = board_bot.properties.milliseconds_left
        if timeLeft > 15*1000:
            direction = self.shortestDiamondAndBaseMove(board_bot, board) 
            finish = time.time()
            print(finish - start)
            return direction
        else:
            direction = self.timeLeftMove(board_bot, board)
            finish = time.time()
            print(finish - start)
            return direction
        