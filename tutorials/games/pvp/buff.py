import inspect
from base_hero import BaseHero

# ----------------- BUFF 定义 START ----------------
def red_flame(self: BaseHero, level: int = 1) -> None:
    """ 攻击力提升 20% """
    self.attack *= 1.2 + (level - 1 * 0.1)

def no_sense(self: BaseHero, level: int = 1) -> None:
    """ 期间血量每减少 3% 获得 1 个'力', 攻击力提升 5% """
    if "_no_sense" not in self.attrs.special:
        self.attrs.special["_no_sense"] = {
            "before": self.health,
            "added_attack": 0,
            "power": 0
        }
    
    before_percent = self.attrs.special["_no_sense"]["before"] / self.max_attrs.health
    missing_percent = self.percentage - before_percent
    power = missing_percent // 0.03
    if power > self.attrs.special["_no_sense"]["power"]:
        self.attrs.special["力"] += power - self.attrs.special["_no_sense"]["power"]
        self.attrs.special["_no_sense"]["power"] = power
        # 每次获得 1 个'力' 时, 攻击力提升 5%
        self.attack *= 1.05 + (level - 1 * 0.05)

def sky_sword(self: BaseHero, level: int = 1) -> None:
    """ 全属性提升 50%, 期间'力'最低不低于 3 个 """
    if self.attrs.special.get("_sky_sword", False):
        buff = self.find_buff("天行")
        if buff.duration == 1:
            # 恢复属性
            gain_attrs = self.attrs.special["_sky_sword"]
            # self.max_health -= gain_attrs[0]
            self.attack -= gain_attrs[1]
            self.defense -= gain_attrs[2]
            self.speed -= gain_attrs[3]
            self.critical -= gain_attrs[4]
            self.critical_multiplier -= gain_attrs[5]
            self.armor_break -= gain_attrs[6]
            self.recover_multiplier -= gain_attrs[7]    
            self.attrs.special.pop("_sky_sword")
            return
        self.attrs.special["力"] = max(self.attrs.special["力"], 3)
    else:
        gain_attrs = [
            self.max_health * .15,
            self.attack * .25,
            self.defense * .05,
            self.speed * .15,
            self.critical * .1,
            self.critical_multiplier * .15,
            self.armor_break * .1,
            self.recover_multiplier * .45
        ]
        self.attrs.special["_sky_sword"] = gain_attrs
        self.max_health += gain_attrs[0]
        self.attack += gain_attrs[1]
        self.defense += gain_attrs[2]
        self.speed += gain_attrs[3]
        self.critical += gain_attrs[4]
        self.critical_multiplier += gain_attrs[5]
        self.armor_break += gain_attrs[6]
        self.recover_multiplier += gain_attrs[7]

# ----------------- BUFF 定义 END ----------------

__effects__ = {
    "红焉": {
        "name": "红焉",
        "type": "trigger", # trigger, continued
        "effect": red_flame,
        "desc": inspect.getdoc(red_flame),
        "visible": True,
        "color": "#E81717"
    },
    "无感": {
        "name": "无感",
        "type": "continued",
        "effect": no_sense,
        "desc": inspect.getdoc(no_sense),
        "visible": True,
        "color": "#FFFFFF"
    },
    "天行": {
        "name": "天行",
        "type": "continued",
        "effect": sky_sword,
        "desc": inspect.getdoc(sky_sword),
        "visible": True,
        "color": "#FFFFFF"
    }
}

def getter(name: str) -> dict:
    return __effects__[name]