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
    with open(file_path, "r") as file:
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
    pass

# 检测碰撞
def check_collision(x: int, y: int, dx: int, dy: int) -> bool:
    """检测碰撞函数"""
    pass

# 移动箱子
def move_box(x: int, y: int, dx: int, dy: int) -> bool:
    """移动箱子函数"""
    pass

# 移动玩家
def move_player(x: int, y: int, dx: int, dy) -> None:
    """移动玩家函数"""
    pass

# 检查游戏是否胜利
def is_win() -> bool:
    """检查游戏是否胜利"""
    pass

def load_target_pos() -> list:
    """加载目标点位置"""
    pass

# ------------- 逻辑代码 -------------

curlevel = 1
"""当前关卡"""
game_map = load_map(f"level{curlevel}.map")
"""游戏地图"""
target_pos = load_target_pos()
"""目标点的位置"""

# 游戏循环