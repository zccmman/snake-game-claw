#!/usr/bin/env python3
"""
🐍 Discord贪吃蛇游戏 - 小爪特别版
专为Discord环境优化的文字版贪吃蛇

游戏规则：
- 使用方向键控制蛇的移动
- 收集食物(*)获得分数
- 避免撞墙和撞到自己
- 游戏结束后可以重新开始
"""

import random
import time
import os

class DiscordSnake:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.snake = [(width//2, height//2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.emojis = {
            'snake_head': '🐍',
            'snake_body': '🟢',
            'food': '🍎',
            'wall': '⬛',
            'empty': '⬜',
            'game_over': '💀'
        }
    
    def generate_food(self):
        while True:
            food = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if food not in self.snake:
                return food
    
    def move_snake(self):
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
    
    def change_direction(self, direction):
        # 防止反向移动
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction
    
    def render_game(self):
        """渲染游戏状态为文本格式"""
        game_map = []
        
        # 创建游戏地图
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
            game_map.append(''.join(row))
        
        # 添加边界
        top_bottom = self.emojis['wall'] * (self.width + 2)
        bordered_map = [top_bottom]
        for row in game_map:
            bordered_map.append(self.emojis['wall'] + row + self.emojis['wall'])
        bordered_map.append(top_bottom)
        
        return '\n'.join(bordered_map)
    
    def get_status(self):
        """获取游戏状态信息"""
        status = f"🐍 贪吃蛇 - 小爪特别版\n"
        status += f"📊 分数: {self.score}\n"
        status += f"🐍 蛇长度: {len(self.snake)}\n"
        status += f"🎯 食物位置: {self.food}\n"
        
        if self.game_over:
            status += f"💀 游戏结束!\n"
            status += f"🔄 输入 \"重新开始\" 再来一局\n"
        else:
            status += f"🎮 方向: {self.get_direction_name()}\n"
            status += f"🍎 去吃苹果吧!\n"
        
        return status
    
    def get_direction_name(self):
        directions = {
            (1, 0): "右",
            (-1, 0): "左", 
            (0, 1): "下",
            (0, -1): "上"
        }
        return directions.get(self.direction, "未知")
    
    def game_step(self, action=None):
        """执行游戏步骤"""
        if action and not self.game_over:
            self.process_action(action)
        
        if not self.game_over:
            self.move_snake()
        
        return self.get_game_state()
    
    def process_action(self, action):
        """处理玩家动作"""
        action_map = {
            '上': (0, -1),
            '下': (0, 1),
            '左': (-1, 0),
            '右': (1, 0),
            'w': (0, -1),
            's': (0, 1),
            'a': (-1, 0),
            'd': (1, 0),
            '↑': (0, -1),
            '↓': (0, 1),
            '←': (-1, 0),
            '→': (1, 0)
        }
        
        if action in action_map:
            self.change_direction(action_map[action])
    
    def get_game_state(self):
        """获取完整的游戏状态"""
        return {
            'board': self.render_game(),
            'status': self.get_status(),
            'score': self.score,
            'game_over': self.game_over,
            'snake_length': len(self.snake),
            'food_position': self.food
        }
    
    def reset(self):
        """重置游戏"""
        self.__init__(self.width, self.height)

class DiscordSnakeGame:
    def __init__(self):
        self.game = None
        self.game_active = False
    
    def start_game(self):
        """开始新游戏"""
        self.game = DiscordSnake()
        self.game_active = True
        return self.get_game_display()
    
    def make_move(self, direction):
        """执行移动"""
        if not self.game_active or not self.game:
            return "🐍 游戏尚未开始，输入\"开始游戏\"来启动"
        
        state = self.game.game_step(direction)
        
        if self.game.game_over:
            self.game_active = False
            
        return self.format_game_display(state)
    
    def get_game_display(self):
        """获取游戏显示"""
        if not self.game:
            return "🐍 游戏尚未开始，输入\"开始游戏\"来启动"
        
        state = self.game.get_game_state()
        return self.format_game_display(state)
    
    def format_game_display(self, state):
        """格式化游戏显示"""
        display = f"```\n"
        display += f"{state['board']}\n"
        display += f"```\n\n"
        display += f"{state['status']}\n"
        
        if state['game_over']:
            display += f"\n💀 **游戏结束！** 最终分数: {state['score']}\n"
            display += f"🔄 输入 \"重新开始\" 再玩一局\n"
        else:
            display += f"\n🎮 **控制方式**: 输入方向 (上/下/左/右 或 w/a/s/d)\n"
            display += f"🎯 **目标**: 收集🍎，避免撞墙和撞到自己\n"
        
        return display
    
    def restart(self):
        """重新开始游戏"""
        return self.start_game()

# 全局游戏实例
game_instance = DiscordSnakeGame()

def play_snake_game(command):
    """主游戏函数"""
    command = command.lower().strip()
    
    if command in ['开始游戏', 'start', '开始', 'play']:
        return game_instance.start_game()
    elif command in ['重新开始', 'restart', '重开']:
        return game_instance.restart()
    elif command in ['上', '下', '左', '右', 'w', 'a', 's', 'd', '↑', '↓', '←', '→']:
        return game_instance.make_move(command)
    elif command in ['状态', 'status', '游戏状态']:
        return game_instance.get_game_display()
    else:
        return f"🐍 **贪吃蛇游戏控制**\n\n" \
               f"🎮 **可用命令**: \n" \
               f"• 开始游戏 / start - 开始新游戏\n" \
               f"• 上 / w / ↑ - 向上移动\n" \
               f"• 下 / s / ↓ - 向下移动\n" \
               f"• 左 / a / ← - 向左移动\n" \
               f"• 右 / d / → - 向右移动\n" \
               f"• 重新开始 / restart - 重新开始游戏\n" \
               f"• 状态 / status - 查看游戏状态\n\n" \
               f"💡 **提示**: 输入\"开始游戏\"来启动！\n\n" \
               f"🐾 **示例**: 输入\"开始游戏\"然后输入\"右\"来向右移动"

if __name__ == "__main__":
    print("🐍 Discord贪吃蛇游戏 - 小爪特别版")
    print("=" * 40)
    print("输入\"开始游戏\"来启动游戏！")
    print("=" * 40)
    
    while True:
        user_input = input("\n🐍 请输入命令: ").strip()
        if user_input.lower() in ['退出', 'exit', 'quit']:
            break
        
        result = play_snake_game(user_input)
        print(f"\n{result}")