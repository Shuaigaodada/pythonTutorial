# -------- 使得python脚本在当前目录下运行 --------
import os, sys
import getch
os.chdir(os.path.dirname(sys.argv[0]))
# --------------------------------------------

TARGET_CHAR = "□"
"""目标点的字符"""
WALL_CHAR = "▒"
"""墙壁的字符"""
PLAYER_CHAR = "■"
"""玩家的字符"""
BOX_CHAR = "#"
"""箱子的字符"""
BORDER_CHAR = ["┌", "┐", "└", "┘", "─", "│"]
"""地图边界的字符"""

def clear() -> None:
    """清屏函数"""
    # 清屏
    print("\033[2J", end="")
    # 光标移动到左上角
    print("\033[0;0H", end="")
    return None

def draw_map(map: list) -> None:
    """绘制地图函数"""
    clear()
    # 绘制边框
    print(BORDER_CHAR[0] + BORDER_CHAR[4] * len(map[0]) + BORDER_CHAR[1])
    # 绘制地图
    for row in map:
        print(BORDER_CHAR[5], end="")
        for char in row:
            if char == PLAYER_CHAR:
                print("\033[92m" + char + "\033[0m", end="")
            elif char == TARGET_CHAR:
                print("\033[93m" + char + "\033[0m", end="")
            elif char == BOX_CHAR:
                print("\033[94m" + char + "\033[0m", end="")
            else:
                print(char, end="")
        print(BORDER_CHAR[5])
    # 绘制边框
    print(BORDER_CHAR[2] + BORDER_CHAR[4] * len(map[0]) + BORDER_CHAR[3])
    
    for pos in target_pos:
        if game_map[pos[1]][pos[0]] == " ":
            game_map[pos[1]][pos[0]] = TARGET_CHAR
    return None

def load_map(file_path: str) -> list:
    """加载地图函数"""
    # 读取地图文件
    with open("maps/" + file_path, "r") as file:
        raw_map = file.read().split("\n")
    
    fmap = []
    # 处理地图
    for line in raw_map:
        map_line = line.replace(".", " ") \
                        .replace("p", PLAYER_CHAR) \
                        .replace("!", WALL_CHAR) \
                        .replace("#", BOX_CHAR) \
                        .replace("x", TARGET_CHAR)
        fmap.append(list(map_line))
    return fmap

def getkey() -> str:
    """获取用户输入"""
    return getch.getch()

# ------------- 逻辑代码 -------------
# 查询玩家位置
def find_player() -> tuple:
    """查询玩家位置函数"""
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if char == PLAYER_CHAR:
                return x, y
    return None

# 检测碰撞
def check_collision(x: int, y: int, dx: int, dy: int) -> bool:
    """检测碰撞函数"""
    if y + dy < 0 or y + dy >= len(game_map):
        return True
    if x + dx < 0 or x + dx >= len(game_map[y]):
        return True
    
    if game_map[y + dy][x + dx] == WALL_CHAR:
        return True
    
    if game_map[y + dy][x + dx] == BOX_CHAR:
        return move_box(x + dx, y + dy, dx, dy)
    return False

# 移动箱子
def move_box(x: int, y: int, dx: int, dy: int) -> bool:
    """移动箱子函数"""
    if y + dy < 0 or y + dy >= len(game_map):
        return True
    if x + dx < 0 or x + dx >= len(game_map[y]):
        return True
        
    if game_map[y + dy] == WALL_CHAR or game_map[y + dy][x + dx] == WALL_CHAR:
        return True
    # 移动箱子
    game_map[y + dy][x + dx] = " "
    game_map[y + dy][x + dx] = BOX_CHAR
    return False

# 移动玩家
def move_player(x: int, y: int, dx: int, dy) -> None:
    """移动玩家函数"""
    game_map[y][x] = " "
    game_map[y + dy][x + dx] = PLAYER_CHAR
    draw_map(game_map)
    return None

# 检查游戏是否胜利
def is_win() -> bool:
    """检查游戏是否胜利"""
    for x, y in target_pos:
        if game_map[y][x] != BOX_CHAR:
            return False
    return True

def load_target_pos() -> list:
    """加载目标点位置"""
    target_pos = []
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if char == TARGET_CHAR:
                target_pos.append((x, y))
    return target_pos

# ------------- 逻辑代码 -------------

curlevel = 1
"""当前关卡"""
game_map = load_map(f"level{curlevel}.map")
"""游戏地图"""
target_pos = load_target_pos()
"""目标点的位置"""
# 游戏循环
while True:
    draw_map(game_map)
    key = getkey()
    if key == "w":
        pos = find_player()
        not check_collision(pos[0], pos[1], 0, -1) and move_player(*pos, 0, -1)
    elif key == "s":
        pos = find_player()
        not check_collision(pos[0], pos[1], 0, 1) and move_player(*pos, 0, 1)
    elif key == "a":
        pos = find_player()
        not check_collision(pos[0], pos[1], -1, 0) and move_player(*pos, -1, 0)
    elif key == "d":
        pos = find_player()
        not check_collision(pos[0], pos[1], 1, 0) and move_player(*pos, 1, 0)
    elif key == "r":
        game_map = load_map(f"level{curlevel}.map")
        
    if is_win():
        curlevel += 1
        game_map = load_map(f"level{curlevel}.map")
        target_pos = load_target_pos()