# -------- 使得python脚本在当前目录下运行 --------
import os, sys
os.chdir(os.path.dirname(sys.argv[0]))
# --------------------------------------------

# 导入所需库
import random
"""
random库介绍
库名称: random
库功能: 用于生成随机数
random库可以通过randint()函数生成指定范围内的随机整数
random.random()生成0-1之间的随机浮点数
"""

# 创建英雄类
class Role:
    # 初始化英雄属性
    def __init__(self, name, hp, atk, defense):
        self.name = name
        self.health = hp
        self.attack = atk
        self.defense = defense
    
    # 英雄受伤接口
    def hurt(self, damage):
        # 计算实际伤害 = 伤害 - 防御 / 2
        # 如果实际伤害小于1, 实际伤害为1
        hurt = max(1, damage - self.defense / 2)
        # 英雄生命值减去实际伤害
        self.health -= hurt
        # 如果英雄生命值小于0
        if self.health < 0:
            # 英雄生命值为0
            self.health = 0
        # 返回实际伤害
        return hurt
    
    # 英雄攻击接口
    def skill1(self):
        # 造成 攻击力 * (1 + 随机浮点0.0-1) 伤害
        damage = self.attack * (1 + random.random())
        # 返回伤害
        return int(damage)
    

# 创建英雄对象
p1 = Role("玩家", 100, 10, 5)
p2 = Role("敌人", 100, 10, 5)

# 游戏循环
while True:
    # 玩家攻击
    damage = p1.skill1()
    print(f"{p1.name}对{p2.name}造成了{damage:}点伤害")
    # 敌人受伤
    hurt = p2.hurt(damage)
    print(f"{p2.name}受到了{hurt}点伤害, 剩余生命值{p2.health}")
    # 如果敌人生命值为0
    if p2.health == 0:
        # 玩家胜利
        print(f"{p1.name}胜利")
        break
    # 敌人攻击
    damage = p2.skill1()
    print(f"{p2.name}对{p1.name}造成了{damage}点伤害")
    # 玩家受伤
    hurt = p1.hurt(damage)
    print(f"{p1.name}受到了{hurt}点伤害, 剩余生命值{p1.health}")
    # 如果玩家生命值为0
    if p1.health == 0:
        # 敌人胜利
        print(f"{p2.name}胜利")
        break
