"""
[████████████████████]      第 2 回合      [████████████████████]
张山 HP: 8000/8000                             院士 HP: 5000/4000
1. 重击                                                   1. 雾锁
2. 蓄力             张山使用了重击，对院士造成 600 点         2. 烈火
3. 烙锁                                                   3. 磁月 
4. 飞鸿                                                 4. 航行天
5. 天行剑 <--                                           5. 非恒基
"""
import math
import curses
import shutil
import wcwidth
from base_hero import BaseHero, Attributes

class Drawer:
    def __init__(self) -> None:
        self.health_char = "█"
        self.shield_char = "▓"
        self.round = 1
        self.choice = 0
        self.message = []
        self.history = []
        self.buffer = []
        self.__color__ = {}
        self.__pair__ = {}
        self.__using__ = 0
        self.__color_index = 8
        self.__pair_index = 1
        self.auto_off = True
        self.cols, self.lines = shutil.get_terminal_size()
        self.CD_Chars = ["○", "◔", "◑", "◕", "●"]
    
    def push_message(self, message: str) -> None:
        self.history.append(message)
        self.message = self.history[-5:]
    
    def init(self) -> None:
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        self.stdscr.keypad(True)
    
    def render(self, hero1: BaseHero, hero2: BaseHero) -> None:
        try:
            self.draw_health(hero1, hero2)
            self.draw_hero_status(hero1, hero2)
            self.draw_skill(hero1, hero2)            
        finally:
            self.close()
        
    def draw_skill(self, hero1: BaseHero, hero2: BaseHero) -> None:
        skill1 = hero1.skills
        skill2 = hero2.skills
        line_index = 3
        
        for i in range(max(len(skill1), len(skill2), len(self.message))):
            if i < len(skill1):
                if skill1[i].is_ready():
                    skill1_text = f"{i + 1}. {skill1[i].name}"
                    self.draw(0, i + line_index, skill1_text)
                    if self.choice == i:
                        self.color("#0DFFE0")
                        self.draw(wcwidth.wcswidth(skill1_text) + 1, i + line_index, "<<<")
                else:
                    tiptxt = f"{i + 1}. "
                    self.draw(0, i + line_index, tiptxt)
                    self.color("#959595")
                    self.draw(len(tiptxt), i + line_index, skill1[i].name)
                    self.color("#F3DD6F")
                    ratio = skill1[i].CD / skill1[i].DCD
                    index = min(int(math.floor(ratio * len(self.CD_Chars))), len(self.CD_Chars) - 1)
                    self.draw(len(tiptxt) + wcwidth.wcswidth(skill1[i].name) + 1, i + line_index, self.CD_Chars[index])
                
            if i < len(skill2):
                if skill2[i].is_ready():
                    skill2_text = f"{i + 1}. {skill2[i].name}"
                    self.draw(self.cols - wcwidth.wcswidth(skill2_text), i + line_index, skill2_text)
                else:
                    skill2_text = f"{i + 1}. "
                    skill2_text_width = wcwidth.wcswidth(skill2_text) + wcwidth.wcswidth(skill2[i].name)
                    self.draw(self.cols - skill2_text_width, i + line_index, skill2_text)
                    self.color("#959595")
                    self.draw(self.cols - wcwidth.wcswidth(skill2[i].name), i + line_index, skill2[i].name)
                    self.color("#F3DD6F")
                    ratio = skill2[i].CD / skill2[i].DCD
                    index = min(int(math.floor(ratio * len(self.CD_Chars))), len(self.CD_Chars) - 1)
                    self.draw(self.cols - skill2_text_width - 2, i + line_index, self.CD_Chars[index])
                    
            if i < len(self.message):
                self.draw(self.cols // 2 - wcwidth.wcswidth(self.message[i]) // 2, i + 2, self.message[i])
        
    def draw_hero_status(self, hero1: BaseHero, hero2: BaseHero) -> None:
        hero1_width = wcwidth.wcswidth(hero1.name)
        hero2_width = wcwidth.wcswidth(hero2.name)
        
        health_text = f"{hero1.health}/{hero1.max_health}"
        self.draw(0, 1, hero1.name)
        color = "#22FF00" if hero1.health > hero1.max_health * 0.5 else "#FF0000"
        self.color(color)
        self.draw(hero1_width + 1, 1, str(hero1.health))
        self.draw(hero1_width + 1 + wcwidth.wcswidth(str(hero1.health)), 1, "/")
        self.color("#22FF00")
        self.draw(hero1_width + 1 + wcwidth.wcswidth(str(hero1.health)) + 1, 1, str(hero1.max_health))
        total_width = hero1_width + 1 + wcwidth.wcswidth(health_text)
        
        self.color("#00D5FF")
        self.draw(total_width + 1, 1, str(hero1.shield) + "🛡️")
        # 绘制 buff 状态
        # 红焉 {CD_Chars[index]}
        padding = wcwidth.wcswidth(str(hero1.shield)) + 4
        for buff in hero1.attrs.buff:
            if not buff.visible: continue
            
            ratio = buff.duration / buff.default_duration
            index = min(int(math.floor(ratio * len(self.CD_Chars))), len(self.CD_Chars) - 1)
            buff_width = wcwidth.wcswidth(buff.name + self.CD_Chars[index])
            self.color(buff.color)
            self.draw(total_width + padding, 1, buff.name)
            self.color("#F3DD6F")
            self.draw(total_width + padding + wcwidth.wcswidth(buff.name), 1, self.CD_Chars[index])
            padding += buff_width + 1
            
        self.draw(self.cols - hero2_width, 1, hero2.name)
        color = "#22FF00" if hero2.health > hero2.max_health * 0.5 else "#FF0000"
        self.color(color)
        self.draw(self.cols - hero2_width - wcwidth.wcswidth(str(hero2.health)) - 1, 1, str(hero2.health))
        self.draw(self.cols - hero2_width - wcwidth.wcswidth(str(hero2.health)) - 2, 1, "/")
        self.color("#22FF00")
        self.draw(self.cols - hero2_width - wcwidth.wcswidth(str(hero2.health)) - len(str(hero2.max_health)) - 2, 1, str(hero2.max_health))
        # self.color("#00D5FF")
        # self.draw(self.cols - hero2_width - wcwidth.wcswidth(str(hero2.shield)) - 1, 1, str(hero2.shield) + "🛡️")
        
    
    def draw_health(self, hero1: BaseHero, hero2: BaseHero) -> None:
        block1, shield1, empty1 = self.clac_health(hero1)
        block2, shield2, empty2 = self.clac_health(hero2)
        
        self.draw(0, 0, f"[")
        self.color("#22FF00")
        self.draw(1, 0, f"{self.health_char * block1}")
        self.color("#00D5FF")
        self.draw(1 + block1, 0, f"{self.shield_char * shield1}")
        self.color_off()
        self.color("#606262")
        self.draw(1 + block1 + shield1, 0, f"{self.health_char * empty1}")
        self.draw(1 + block1 + shield1 + empty1, 0, f"]")
        
        round_text = f"第 {self.round} 回合"
        round_width = wcwidth.wcswidth(round_text)
        self.draw(self.cols // 2 - round_width // 2, 0, round_text)
        
        self.draw(self.cols - 1, 0, f"]")
        self.color("#22FF00")
        self.draw(self.cols - 1 - block2, 0, f"{self.health_char * block2}")
        self.color("#00D5FF")
        self.draw(self.cols - 1 - block2 - shield2, 0, f"{self.shield_char * shield2}")
        self.color("#606262")
        self.draw(self.cols - 1 - block2 - shield2 - empty2, 0, f"{self.health_char * empty2}")
        self.draw(self.cols - 1 - block2 - shield2 - empty2 - 1, 0, f"[")    
    
    def clac_health(self, hero: BaseHero) -> list[int]:
        base_length = int(self.cols * 0.33)
        health = hero.health
        max_health = hero.max_health
        default_health = hero.default_attrs.health
        shield = hero.shield
        
        # 基础长度 * (最大生命值 / 默认生命值)
        # 最大生命长度
        ratio = int(min(base_length * (max_health / default_health), self.cols * .45))
        # 血量长度
        block = int(health / max_health * ratio)
        
        # 护盾/最大生命 * 最大生命长度 * 0.5
        shield_block = min(ratio, int(shield / max_health * ratio * 0.5))
        if shield_block > ratio - block:
            block = max(0, block - shield_block - (ratio - block))
        
        empty_block = ratio - block - shield_block
        return [block, shield_block, empty_block]
        
    def cursor_up(self, hero: BaseHero) -> None:
        self.choice = self.choice - 1
        if self.choice < 0:
            self.choice = len(hero.skills) - 1
        
        if not hero.skills[self.choice].is_ready():
            self.cursor_up(hero)
    
    def cursor_down(self, hero: BaseHero) -> None:
        self.choice = self.choice + 1
        if self.choice == len(hero.skills):
            self.choice = 0
        
        if not hero.skills[self.choice].is_ready():
            self.cursor_down(hero)
    
    def close(self) -> None:
        curses.endwin()
    
    def color(self, hexfg: str, hexbg: str = "#000000") -> None:
        hexfg = hexfg.upper().strip("#")
        hexbg = hexbg.upper().strip("#")
        
        # 转化为 RGB
        fg = [int(hexfg[i:i + 2], 16) for i in range(0, 6, 2)]
        bg = [int(hexbg[i:i + 2], 16) for i in range(0, 6, 2)]
        
        # 转化为 1000 级别
        fg = [int(1000 * i / 255) for i in fg]
        bg = [int(1000 * i / 255) for i in bg]
        
        if hexfg not in self.__color__:
            curses.init_color(self.__color_index, *fg)
            self.__color__[hexfg] = self.__color_index
            self.__color_index += 1
        if hexbg not in self.__color__:
            curses.init_color(self.__color_index, *bg)
            self.__color__[hexbg] = self.__color_index
            self.__color_index += 1
        
        if (hexfg, hexbg) not in self.__pair__:
            curses.init_pair(self.__pair_index, self.__color__[hexfg], self.__color__[hexbg])
            self.__pair__[hexfg, hexbg] = self.__pair_index
            self.__pair_index += 1
        
        self.__using__ = self.__pair__[hexfg, hexbg]
        self.stdscr.attron(curses.color_pair(self.__pair__[hexfg, hexbg]))
    
    def color_off(self) -> None:
        self.stdscr.attroff(curses.color_pair(self.__using__))
    
    def draw(self, x: int, y: int, string: str, flush=False, color: str = None) -> None:
        self.stdscr.addstr(y, x, string)
        flush and self.stdscr.refresh()
        self.auto_off and self.color_off()
    
    
    def clear(self) -> None:
        self.stdscr.clear()
        

if __name__ == "__main__":
    from heroes import HeroZhangshan
    
    role1 = HeroZhangshan()
    role2 = HeroZhangshan()
    
    role2.max_health = 300000
    role2.recover(300000)
    role2.shield = 100000
    role1.attack = 1145
    
    drawer = Drawer()
    drawer.init()
    drawer.render(role1, role2)
    # drawer.stdscr.getch()
    while not role1.is_death() and not role2.is_death():
        char = drawer.stdscr.getch()
        drawer.clear()
        if char == curses.KEY_UP:
            drawer.cursor_up(role1)
        elif char == curses.KEY_DOWN:
            drawer.cursor_down(role1)
        elif char == ord("\n"):
            skill = role1.skills[drawer.choice]
            if skill.is_ready():
                skill(role2)
                skill.CD = skill.DCD
                
                drawer.round += 1
                
                role1.health = int(role1.health * 0.8)
                role1.settle()
        
        drawer.render(role1, role2)
