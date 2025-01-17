import sys
import buff
import skills
import inspect
from base_hero import BaseHero

        

class HeroZhangshan(BaseHero):
    def __init__(self):
        super().__init__()
        self.name = "张山"
        self.default_attrs.health = 8000
        self.default_attrs.attack = 300
        self.default_attrs.defense = 100
        self.default_attrs.speed = 0.6
        self.default_attrs.critical = 0.35
        self.default_attrs.critical_multiplier = 215
        self.default_attrs.armor_break = 0.15
        self.default_attrs.special = { "力": 0 }
        self.default_attrs.recover_multiplier = 100
        self.skills = [0, 1, 2, 3, 4]
        self.init(skills.getter, buff.getter)
        


def heroes():
    return [cls for name, cls in inspect.getmembers(sys.modules[__name__]) if inspect.isclass(cls) and name.startswith("Hero")]


if __name__ == "__main__":
    role1 = HeroZhangshan()
    print(role1.skills[0](HeroZhangshan()))
    
    
