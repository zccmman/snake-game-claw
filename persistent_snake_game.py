#!/usr/bin/env python3
"""
🐍 Discord贪吃蛇游戏 - 状态保持版
专为Discord环境优化的文字版贪吃蛇，支持状态保持
"""

import random

class PersistentSnakeGame:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态"""
        self.width = 20
        self.height = 15
        self.snake = [(self.width//2, self.height//2)]
        self.direction = (1, 0)  # 初始向右
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.emojis = {
            'snake_head': '🐍',
            'snake_body': '🟢', 
            'food': '🍎',
            'wall': '⬛',
            'empty': '⬜'
        }
    
    def generate_food(self):
        """生成食物位置"""
        while True:
            food = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """移动蛇"""
        if self.game_over:
            return
            
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # 检查边界
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # 检查自身碰撞
        if new_head in self.snake:
            self.game_over = True
            return
        
        # 移动蛇
        self.snake.insert(0, new_head)
        
        # 检查食物
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """改变方向（防止反向）"""
        direction_map = {
            '右': (1, 0), 'd': (1, 0), '→': (1, 0),
            '左': (-1, 0), 'a': (-1, 0), '←': (-1, 0),
            '下': (0, 1), 's': (0, 1), '↓': (0, 1),
            '上': (0, -1), 'w': (0, -1), '↑': (0, -1)
        }
        
        if new_direction in direction_map:
            new_dir = direction_map[new_direction]
            # 防止反向移动
            current_dir = self.direction
            if (new_dir[0] != -current_dir[0] or new_dir[1] != -current_dir[1]):
                self.direction = new_dir
    
    def render_board(self):
        """渲染游戏棋盘"""
        board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    row.append(self.emojis['snake_head'])
                elif (x, y) in self.snake:
                    row.append(self.emojis['snake_body'])
                elif (x, y) == self.food:
                    row.append(self.emojis['food'])
                else:
                    row.append(self.emojis['empty'])
            board.append(''.join(row))
        
        # 添加边框
        wall = self.emojis['wall']
        bordered = [wall * (self.width + 2)]
        for row in board:
            bordered.append(wall + row + wall)
        bordered.append(wall * (self.width + 2))
        
        return '\n'.join(bordered)
    
    def get_status(self):
        """获取游戏状态"""
        direction_names = {(1, 0): '右', (-1, 0): '左', (0, 1): '下', (0, -1): '上'}
        
        status = f"🐍 **贪吃蛇 - 小爪特别版**\n\n"
        status += f"📊 **分数**: {self.score}\n"
        status += f"🐍 **蛇长度**: {len(self.snake)}\n"
        status += f"🎯 **方向**: {direction_names.get(self.direction, '未知')}\n"
        
        if self.game_over:
            status += f"💀 **游戏结束!**\n"
            status += f"🔄 输入\"重新开始\"再来一局\n"
        else:
            status += f"🍎 **食物位置**: {self.food}\n"
            status += f"🎮 **状态**: 游戏中\n"
        
        return status
    
    def play_step(self, action=None):
        """执行游戏步骤"""
        if action:
            self.change_direction(action)
        
        if not self.game_over:
            self.move_snake()
        
        return self.get_game_state()
    
    def get_game_state(self):
        """获取完整游戏状态"""
        return {
            'board': self.render_board(),
            'status': self.get_status(),
            'score': self.score,
            'game_over': self.game_over,
            'snake_length': len(self.snake),
            'food_position': self.food
        }

# 全局游戏实例
game = PersistentSnakeGame()

def play_discord_snake(command):
    """Discord贪吃蛇游戏主函数"""
    command = command.lower().strip()
    
    if command in ['开始游戏', 'start', '开始', 'play', '新游戏']:
        game.reset_game()
        state = game.get_game_state()
        return f"{state['board']}\n\n{state['status']}"
    
    elif command in ['重新开始', 'restart', '重开', 'reset']:
        game.reset_game()
        state = game.get_game_state()
        return f"🔄 **重新开始！**\n\n{state['board']}\n\n{state['status']}"
    
    elif command in ['上', '下', '左', '右', 'w', 'a', 's', 'd', '↑', '↓', '←', '→']:
        if game.game_over:
            return "💀 游戏已结束！输入\"重新开始\"再来一局"
        
        state = game.play_step(command)
        
        result = f"{state['board']}\n\n{state['status']}"
        
        if state['game_over']:
            result += f"\n\n💀 **游戏结束！** 最终分数: {state['score']}"
            result += f"\n🔄 输入\"重新开始\"再玩一局"
        
        return result
    
    elif command in ['帮助', 'help', '说明', 'h']:
        return "🐍 **贪吃蛇游戏帮助**\n\n" \
               "🎮 **控制方式**:\n" \
               "• 上 / w / ↑ - 向上移动\n" \
               "• 下 / s / ↓ - 向下移动\n" \
               "• 左 / a / ← - 向左移动\n" \
               "• 右 / d / → - 向右移动\n\n" \
               "🎯 **游戏目标**: 收集🍎食物，避免撞墙和撞到自己\n" \
               "📊 **得分**: 每吃一个食物得10分\n\n" \
               "🔄 **其他命令**:\n" \
               "• 开始游戏 - 开始新游戏\n" \
               "• 重新开始 - 重置游戏\n" \
               "• 帮助 - 显示帮助信息\n\n" \
               "🐾 **祝你游戏愉快！**"
    
    elif command in ['状态', 'status', '游戏状态']:
        state = game.get_game_state()
        return f"{state['status']}"
    
    else:
        return "🐍 **贪吃蛇游戏**\n\n" \
               "💡 输入\"开始游戏\"开始新游戏\n" \
               "🎮 输入方向(上/下/左/右)控制移动\n" \
               "❓ 输入\"帮助\"查看详细说明\n\n" \
               "🐾 **示例**: 输入\"开始游戏\"然后输入\"右\"移动"