# -------- 使得python脚本在当前目录下运行 --------
import os, sys
from collections import deque
os.chdir(os.path.dirname(sys.argv[0]))
# --------------------------------------------
"""
为此，一个自动关卡生成器
通常由三部分组成：
1. 关卡生成器：采用随机或者过程化的方式增量式地生成关卡。
2. 关卡求解器：输入关卡生成器生成的一个关卡，判断其是否有解。
3. 关卡过滤器：输入一个生成好且有解的关卡，判断其解状态空间与最小求解步数是否满足需求。
三个部分的相互作用如下图所示：
关卡生成器的三个部分及它们的关系下面我们详细阐述一下关卡生成器、
求解器与过滤器的具体实现。关卡生成器关卡生成器采用增量式随机生成关卡的策略：
关卡求解器我们采用广度优先搜索的算法来求解推箱子谜题。
理由是：
1. 广度优先可以计算出游戏从初始状态到解谜成功状态的最少步骤。
2. 广度优先可以回溯取得解谜过程的状态序列，这些状态序列就是谜题的最短解题步骤。
3. 广度优先搜索的过程中会获得一棵解法树，这棵树的深度与广度可以衡量所生成关卡的解状态空间复杂度。
由于游戏中可变的单位只有箱子和小人的位置，所以状态节点只需要记录箱子与小人的位置即可。
需要注意的是，在用广度优先搜索的过程中，会发生状态空间爆炸的情况，必须对每一个状态节点进行剪枝，否则求解一次非常慢。
可以考虑从以下几点进行剪枝：去重：将每个状态节点散列到一个Hash临接表上，每次生成新的状态都判断之前是否有同样的游戏状态，
如果有，则不添加该状态。判断死锁：比如以下情况中有箱子没有办法被推动，
如果此时箱子没有位于目标点上，则说明该状态之后不可能达到胜利状态，不添加该状态。
死锁情况一： ## ## 
死锁情况二：--▩▩ 

"""


import os
import random
from collections import deque
from IPLA import Pool

# 定义地图元素
WALL_CHAR = "!"
TARGET_CHAR = "x"
PLAYER_CHAR = "p"
BOX_CHAR = "#"
EMPTY_CHAR = "."

# 定义地图文件路径
map_dir = "/workspaces/pythonTutorial/题库/push_box/maps"

# 确保地图文件夹存在
map_dir = "/workspaces/pythonTutorial/题库/push_box/maps"

# 确保地图文件夹存在
os.makedirs(map_dir, exist_ok=True)

# def random_walk_walls(MAP, width, height, num_walls):
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#     for _ in range(num_walls):
#         x = random.randint(1, width - 2)
#         y = random.randint(1, height - 2)
#         MAP[y][x] = WALL_CHAR
#         for _ in range(random.randint(1, 5)):  # 增加墙壁的长度
#             dx, dy = random.choice(directions)
#             nx, ny = x + dx, y + dy
#             if 1 <= nx < width - 1 and 1 <= ny < height - 1:
#                 MAP[ny][nx] = WALL_CHAR
#                 x, y = nx, ny

def creator(width, height, diff: int):
    MAP = []
    for _ in range(height):
        MAP.append([EMPTY_CHAR for _ in range(width)])
    
    box_pool = Pool(diff, diff // 4, 1e-3)
    
    # 随机生成墙壁
    # random_walk_walls(MAP, width, height, diff // 2)
    
    # 随机生成箱子和目标点
    for _ in range(diff):
        if random.random() < 0.7:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if MAP[y][x] == EMPTY_CHAR:
                MAP[y][x] = WALL_CHAR
        
        if box_pool.draw():
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                tx = random.randint(0, width - 1)
                ty = random.randint(0, height - 1)
                
                if tx != x and ty != y and MAP[y][x] == EMPTY_CHAR and MAP[ty][tx] == EMPTY_CHAR:
                    break
            MAP[y][x] = BOX_CHAR
            MAP[ty][tx] = TARGET_CHAR
    
    # 随机放置玩家
    while True:
        px, py = random.randint(1, width - 2), random.randint(1, height - 2)
        if MAP[py][px] == EMPTY_CHAR:
            MAP[py][px] = PLAYER_CHAR
            break
    
    return MAP

def resolve(game_map):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def is_valid_pos(x, y):
        return 0 <= x < len(game_map[0]) and 0 <= y < len(game_map) and game_map[y][x] != WALL_CHAR
    
    def is_deadlock(box_positions):
        for bx, by in box_positions:
            if game_map[by][bx] == TARGET_CHAR:
                continue
            if ((by > 0 and game_map[by-1][bx] == WALL_CHAR or by < len(game_map) - 1 and game_map[by+1][bx] == WALL_CHAR) and
                (bx > 0 and game_map[by][bx-1] == WALL_CHAR or bx < len(game_map[0]) - 1 and game_map[by][bx+1] == WALL_CHAR)):
                return True
        return False
    
    def bfs(start, targets, boxes):
        queue = deque([start])
        visited = set()
        visited.add(start)
        
        i = 0
        while queue:
            if i > 500000:
                break
            i += 1
            
            player_pos, box_positions = queue.popleft()
            
            if all(pos in targets for pos in box_positions):
                return True
            
            for dx, dy in directions:
                new_player_pos = (player_pos[0] + dx, player_pos[1] + dy)
                
                if is_valid_pos(new_player_pos[0], new_player_pos[1]):
                    new_box_positions = set(box_positions)
                    if new_player_pos in box_positions:
                        new_box_pos = (new_player_pos[0] + dx, new_player_pos[1] + dy)
                        if is_valid_pos(new_box_pos[0], new_box_pos[1]) and new_box_pos not in box_positions:
                            new_box_positions.remove(new_player_pos)
                            new_box_positions.add(new_box_pos)
                        else:
                            continue
                    
                    new_state = (new_player_pos, frozenset(new_box_positions))
                    if new_state not in visited and not is_deadlock(new_box_positions):
                        visited.add(new_state)
                        queue.append(new_state)
        
        return False
    
    player_pos = None
    targets = set()
    boxes = set()
    
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if char == PLAYER_CHAR:
                player_pos = (x, y)
            elif char == TARGET_CHAR:
                targets.add((x, y))
            elif char == BOX_CHAR:
                boxes.add((x, y))
    
    if not player_pos or not targets or not boxes:
        return False
    
    return bfs((player_pos, frozenset(boxes)), targets, boxes)


# 生成并保存地图
for i in range(1, 2):
    game_map = creator(10, 5, 30)
    while not resolve(game_map):
        print("生成的地图无解，正在重新生成...")
        game_map = creator(10, 5, 30)
        
        
    print(f"地图{i}生成成功。")
    with open(os.path.join(map_dir, f"level{i}.map"), "w") as file:
        content = "\n".join(["".join(row) for row in game_map])
        file.write(content)
    print(f"地图{i}文件已生成。")