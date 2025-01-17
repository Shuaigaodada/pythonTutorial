import inspect
from base_hero import BaseHero

def red_flame(self: BaseHero, level: int = 1) -> None:
    """ 攻击力提升 20% """
    self.attack *= 1.2 + (level - 1 * 0.1)


__effects__ = {
    "红焉": {
        "name": "红焉",
        "type": "trigger", # trigger, continued
        "effect": red_flame,
        "desc": inspect.getdoc(red_flame),
        "visible": True,
        "color": "#E81717"
    },
}

def getter(name: str) -> dict:
    return __effects__[name]