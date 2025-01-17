import random
from typing import List, Callable

def skill_wrapper(skill: Callable, hero: "BaseHero") -> Callable:
    """ 技能装饰器 """
    def wrapper(target: "BaseHero") -> None:
        return skill(hero, target)
    return wrapper

class SkillWrapper:
    def __init__(self, skill: dict, hero: "BaseHero") -> None:
        self.name = skill.get("name", "未知技能")
        self.description = skill.get("description", "未知技能")
        self.CD = skill.get("CD", 0)
        self.DCD = skill.get("CD", 0)
        self.function = skill.get("function")
        self.function = skill_wrapper(self.function, hero)
    
    def __call__(self, target: "BaseHero"):
        return self.function(target)

    def is_ready(self) -> bool:
        """ 技能是否就绪 """
        return self.CD <= 0

class Buff:
    TRIGGER = "tirgger"
    CONTINUED = "continued"
    def __init__(self, buff: dict, level: int, duration: int, hero: "BaseHero" = None) -> None:
        self.level = level
        self.duration = duration
        self.default_duration = duration
        self.effect = buff.get("effect", lambda _, __: None)
        self.desc = buff.get("desc", "未知效果")
        self.type = buff.get("type", "ERR")
        self.hero = hero
        self.name = buff.get("name", "未知效果")
        self.visible = buff.get("visible", False)
        self.triggered = False
        self.color = buff.get("color", "#FFFFFF")
        
        if self.type == "ERR":
            raise ValueError("未知的增益效果类型")
    
    def is_finished(self) -> bool:
        """ 是否结束 """
        return self.duration <= 0
    
    def __call__(self, hero: "BaseHero" = None) -> None:
        if hero is None:
            hero = self.hero
        return self.effect(hero)
    
    def __repr__(self) -> str:
        return f"<Buff {self.name} Lv.{self.level} Duration: {self.duration} Effect: {self.desc}>"

class Attributes:
    def __init__(self):
        self.health: int = 0
        """ 英雄血量 """
        self.attack: int = 0
        """ 英雄攻击力 """
        self.defense: int = 0
        """ 英雄防御力 """
        self.speed: float = 0.0
        """ 英雄速度 """
        self.critical: float = 0
        """ 英雄暴击率 """
        self.critical_multiplier: int = 0
        """ 英雄暴击伤害倍率 """
        self.recover_multiplier: int = 100
        """ 英雄回复效果倍率 """
        self.armor_break: float = 0
        """ 英雄穿甲倍率 """
        self.shield: int = 0
        """ 英雄护盾 """
        self.stun: int = 0
        """ 英雄眩晕回合 """
        self.stun_resist: float = 0
        """ 英雄眩晕抗性 """
        self.special = {}
        """ 英雄特殊属性 """
        self.buff: List[Buff] = []
        """ 英雄增益效果 """
        self.debuff: List[Buff] = []
        """ 英雄减益效果 """
    
    def copy(self) -> "Attributes":
        """ 复制属性 """
        attr = Attributes()
        attr.health = self.health
        attr.attack = self.attack
        attr.defense = self.defense
        attr.speed = self.speed
        attr.critical = self.critical
        attr.critical_multiplier = self.critical_multiplier
        attr.recover_multiplier = self.recover_multiplier
        attr.armor_break = self.armor_break
        attr.shield = self.shield
        attr.stun = self.stun
        attr.stun_resist = self.stun_resist
        attr.special = self.special.copy()
        attr.buff = self.buff.copy()
        attr.debuff = self.debuff.copy()
        return attr

class BaseHero:
    def __init__(self):
        self.name: str = "undefined"
        """ 英雄名称 """
        self.default_attrs = Attributes()
        """ 英雄默认属性 """
        self.max_attrs = Attributes()
        """ 英雄最大属性 """
        self.attrs = Attributes()
        """ 英雄属性 """
        self.skills: List[int | SkillWrapper] = []
        """ 英雄技能 """
    
    def init(self, getter: Callable, buff_getter: Callable) -> None:
        """ 初始化英雄 """
        self.max_attrs = self.default_attrs.copy()
        self.attrs = self.default_attrs.copy()
        
        skills = []
        for skill_id in self.skills:
            skill: dict = getter(skill_id)
            if skill:
                skill = skill.copy()
                skill["CD"] = 0
                skill = SkillWrapper(skill, self)
                skills.append(skill)
            else:
                raise ValueError(f"技能 {skill_id} 不存在")

        self.skills = skills
        self.buff_getter = buff_getter
    
    @property
    def percentage(self) -> float:
        """ 血量百分比 """
        return self.attrs.health / self.max_attrs.health
    
    def register_buff(self, name: str, duration: int, /, level: int = 1) -> None:
        """ 注册增益效果 """
        self.attrs.buff.append(Buff(
            buff=self.buff_getter(name),
            level=level,
            duration=duration,
            hero=self
        ))
        
    def register_debuff(self, name: str, duration: int, /, level: int = 1) -> None:
        """ 注册减益效果 """
        self.attrs.debuff.append(Buff(
            buff=self.buff_getter(name),
            level=level,
            duration=duration,
            hero=self
        ))
    
    def register_stun(self, prob: float, duration: int = 1) -> None:
        """
        注册眩晕效果

        Args:
            prob: 眩晕概率
            duration: 眩晕回合
        """
        prob = max(0, prob - self.attrs.stun_resist)
        if random.uniform(0, 100) <= prob:
            self.attrs.stun = duration
    
    def recover(self, value: int) -> None:
        """
        恢复血量
        
        Args:
            value: 恢复值
        """
        self.health = min(self.max_attrs.health, self.attrs.health + (value * self.attrs.recover_multiplier / 100))
    
    def hurt(self, damage: int, callback: None | Callable = None) -> int:
        """
        计算角色受到伤害
        
        Args:
            damage: 伤害值
        Returns:
            int: 实际受到的伤害
        """
        damage = max(0, damage - self.attrs.defense * (1 - self.attrs.armor_break))
        if self.shield >= damage:
            self.shield -= damage
            real_damage = 0
        else:
            real_damage = damage - self.shield
            self.shield = 0
            self.health -= real_damage
        
        callback and callback(damage, real_damage)
        return damage
        
    
    # 结算
    def settle(self) -> None:
        """ 回合结算 """
        for buff in self.attrs.buff:
            if buff.type == buff.CONTINUED:
                buff()
            elif buff.type == buff.TRIGGER and not buff.triggered:
                buff()
                buff.triggered = True
            
            buff.duration = max(0, buff.duration - 1)
            
            # 检查是否结束
            if buff.is_finished():
                self.attrs.buff.remove(buff)
        
        for debuff in self.attrs.debuff:
            if debuff.type == debuff.CONTINUED:
                debuff()
            elif debuff.type == debuff.TRIGGER and not debuff.triggered:
                debuff()
                debuff.triggered = True
            
            debuff.duration = max(0, debuff.duration - 1)
            
        
        for skill in self.skills:
            skill.CD = max(0, skill.CD - 1)
    
    def use(self, index: str | int) -> SkillWrapper:
        """
        使用技能
        
        Args:
            index: 技能名称或索引
        Returns:
            Callable: 技能函数
        """
        if isinstance(index, int):
            index = self.skill_name()[index]
        
        for skill in self.skills:
            if skill.name == index: 
                return skill
        return None
        
    def skill_name(self) -> List[str]:
        """ 技能名称 """
        return [skill.name for skill in self.skills]
    
    def find(self, index: str | int) -> dict:
        """
        查找技能
        
        Args:
            index: 技能名称或索引
        Returns:
            dict: 技能信息
        """
        if isinstance(index, int):
            index = self.skill_name()[index]
        for skill in self.skills:
            if skill.name == index: 
                return skill
        return None
    
    def find_buff(self, name: str) -> Buff:
        """ 查找增益/减益效果 """
        for buff in self.attrs.buff[:] + self.attrs.debuff[:]:
            if buff.name == name:
                return buff
        return None
    
    def is_death(self) -> bool:
        """ 是否死亡 """
        return self.attrs.health <= 0
        
    @property
    def health(self) -> int:
        return self.attrs.health
    @property
    def attack(self) -> int:
        return self.attrs.attack
    @property
    def defense(self) -> int:
        return self.attrs.defense
    @property
    def speed(self) -> float:
        return self.attrs.speed
    @property
    def critical(self) -> float:
        return self.attrs.critical
    @property
    def critical_multiplier(self) -> int:
        return self.attrs.critical_multiplier
    @property
    def armor_break(self) -> float:
        return self.attrs.armor_break
    @property
    def shield(self) -> int:
        return self.attrs.shield
    @property
    def stun(self) -> int:
        return self.attrs.stun
    @property
    def stun_resist(self) -> float:
        return self.attrs.stun_resist
    @property
    def special(self) -> dict:
        return self.attrs.special
    @property
    def recover_multiplier(self) -> int:
        return self.attrs.recover_multiplier
    @property
    def max_health(self) -> int:
        return self.max_attrs.health
    @property
    def max_attack(self) -> int:
        return self.max_attrs.attack
    @property
    def max_defense(self) -> int:
        return self.max_attrs.defense
    @property
    def max_speed(self) -> float:
        return self.max_attrs.speed
    @property
    def max_critical(self) -> float:
        return self.max_attrs.critical
    @property
    def max_critical_multiplier(self) -> int:
        return self.max_attrs.critical_multiplier
    @property
    def max_armor_break(self) -> float:
        return self.max_attrs.armor_break
    @property
    def max_shield(self) -> int:
        return self.max_attrs.shield
    @property
    def max_stun(self) -> int:
        return self.max_attrs.stun
    @property
    def max_stun_resist(self) -> float:
        return self.max_attrs.stun_resist
    @property
    def max_special(self) -> dict:
        return self.max_attrs.special
    @property
    def max_buff(self) -> List[dict]:
        return self.max_attrs.buff
    @property
    def max_debuff(self) -> List[dict]:
        return self.max_attrs.debuff
    @property
    def max_recover_multiplier(self) -> int:
        return self.max_attrs.recover_multiplier
    
    @health.setter
    def health(self, value: int | float) -> None:
        self.attrs.health = int(max(min(value, self.max_health), 0))
    @attack.setter
    def attack(self, value: int | float) -> None:
        self.attrs.attack = int(value)
    @defense.setter
    def defense(self, value: int | float) -> None:
        self.attrs.defense = int(value)
    @speed.setter
    def speed(self, value: int | float) -> None:
        self.attrs.speed = float(value)
    @critical.setter
    def critical(self, value: int | float) -> None:
        self.attrs.critical = float(value)
    @critical_multiplier.setter
    def critical_multiplier(self, value: int | float) -> None:
        self.attrs.critical_multiplier = int(value)
    @armor_break.setter
    def armor_break(self, value: int | float) -> None:
        self.attrs.armor_break = float(value)
    @shield.setter
    def shield(self, value: int | float) -> None:
        self.attrs.shield = int(value)
    @stun.setter
    def stun(self, value: int | float) -> None:
        self.attrs.stun = int(value)
    @stun_resist.setter
    def stun_resist(self, value: int | float) -> None:
        self.attrs.stun_resist = float(value)
    @recover_multiplier.setter
    def recover_multiplier(self, value: int | float) -> None:
        self.attrs.recover_multiplier = int(value)
    @max_health.setter
    def max_health(self, value: int | float) -> None:
        self.max_attrs.health = int(value)
    @max_attack.setter
    def max_attack(self, value: int | float) -> None:
        self.max_attrs.attack = int(value)
    @max_defense.setter
    def max_defense(self, value: int | float) -> None:
        self.max_attrs.defense = int(value)
    @max_speed.setter
    def max_speed(self, value: int | float) -> None:
        self.max_attrs.speed = float(value)
    @max_critical.setter
    def max_critical(self, value: int | float) -> None:
        self.max_attrs.critical = float(value)
    @max_critical_multiplier.setter
    def max_critical_multiplier(self, value: int | float) -> None:
        self.max_attrs.critical_multiplier = int(value)
    @max_armor_break.setter
    def max_armor_break(self, value: int | float) -> None:
        self.max_attrs.armor_break = float(value)
    @max_shield.setter
    def max_shield(self, value: int | float) -> None:
        self.max_attrs.shield = int(value)
    @max_stun.setter
    def max_stun(self, value: int | float) -> None:
        self.max_attrs.stun = int(value)
    @max_stun_resist.setter
    def max_stun_resist(self, value: int | float) -> None:
        self.max_attrs.stun_resist = float(value)
    @max_recover_multiplier.setter
    def max_recover_multiplier(self, value: int | float) -> None:
        self.max_attrs.recover_multiplier = int(value)
