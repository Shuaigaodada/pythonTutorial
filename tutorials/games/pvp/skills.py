import sys
import inspect
from typing import Dict, Callable
from base_hero import BaseHero, Attributes

# ----------------- 前置依赖 START ----------------
def skill(name: str, CD: int) -> Callable:
    """
    技能装饰器
    
    Args:
        name: 技能名称
        CD: 冷却时间
    Returns:
        Callable: 技能函数
    """
    def decorator(function: Callable) -> Callable:
        global __skills__
        __skills__[len(__skills__)] = {
            "name": name,
            "description": inspect.getdoc(function),
            "function": function,
            "CD": CD,
            "DCD": CD
        }
        return function
    return decorator

__skills__: Dict[int, Dict[str, str | Callable | int]] = { }
""" 技能字典 """
# ----------------- 前置依赖 END ------------------

# ----------------- 技能定义 START ----------------
@skill(name="重击", CD=2)
def heavy(self: BaseHero, target: BaseHero) -> int:
    """
    重击: 消耗所有'力'对敌方造成 200% 攻击力的伤害, 每一个'力'增加 50% 伤害, 获得造成伤害的 30% 的护盾
    类型: 物理攻击
    冷却时间 (CD): 2
    """
    damage = self.attack * 2
    for _ in range(self.attrs.special["力"]):
        damage += self.attack * 0.5
    self.attrs.special["力"] = 0
    
    real_damage = target.hurt(damage)
    self.shield += real_damage * 0.3
    return real_damage

@skill(name="三角锁", CD=5)
def triangle_lock(self: BaseHero, target: BaseHero) -> int:
    """
    三角锁: 对敌方造成 80% 攻击力的伤害, 75% 概率眩晕敌方 1 回合, 获得 1 个'力'
    类型: 眩晕
    冷却时间 (CD): 5
    """
    damage = self.attack * 0.8
    target.register_stun(75, 1)
    self.attrs.special["力"] += 1
    return target.hurt(damage)
    
@skill(name="红焉拳", CD=2)
def red_flame_fist(self: BaseHero, target: BaseHero) -> int:
    """
    红焉拳: 造成 75% 攻击力的伤害, 自身攻击力提升 20%, 恢复造成伤害 50% 的生命值, 获得 1 个'力'
    类型: 恢复 & 攻击
    冷却时间 (CD): 2
    """
    damage = self.attack * 0.75
    self.register_buff("红焉", 2)
    return target.hurt(damage)

@skill(name="无感功", CD=7)
def no_sense(self: BaseHero, target: BaseHero) -> int:
    """
    无感功: 眩晕 2 回合, 获得 2 个'力', 此期间血量每减少 3% 获得 1 个'力', 攻击力提升 5%
    类型: 蓄力
    冷却时间 (CD): 7
    """
    self.register_stun(1000, 2)
    self.attrs.special["力"] += 2
    self.register_buff("无感", 7)
    return 0
    
# ----------------- 技能定义END -------------------

def getter(skill_id: int) -> Dict[str, str | Callable | int] | None:
    """ 获取技能 """
    return __skills__.get(skill_id, None).copy()

if __name__ == "__main__":
    print(__skills__)
    damage = getter(0)["function"](BaseHero(), BaseHero())
    print(damage)