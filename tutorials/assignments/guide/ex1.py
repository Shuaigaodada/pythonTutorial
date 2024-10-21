# -*- coding: utf-8 -*-
# # 猜数字游戏
import random

# number = random.randint(1, 100)
# print("猜猜我心里想的是哪个数字？")

# userGuess = -1
# guessCount = 0

# while userGuess != number:
#     userGuess = int(input("请输入你猜的数字："))
    
#     if userGuess > number:
#         print("太大了")
#         guessCount += 1
#     if userGuess < number:
#         print("太小了")
#         guessCount += 1
        
# print(f"wow! 你猜对了！只用了{guessCount}次哦！")

import jionlp
import china_idiom as idiom
import time
import os
os.system("cls||clear")
time.sleep(1)

emotionText = {
    "happy": ["o(〃'▽'〃)o", "ʕ•̀ω•́ʔ✧","(๑˃̵ᴗ˂̵)و","٩(๑˃́ꇴ˂̀๑)۶","٩(๑˃̵ᴗ˂̵๑)۶","٩(๑❛ᴗ❛๑)۶","(´◒`)","(｡╹ω╹｡)"],
    "okay": ["(๑•̀ㅂ•́)و","(๑•́ ₃ •̀๑)ｴｰ", "(ง •̀_•́)ง‼","٩(๑`^´๑)۶","( つ•̀ω•́)つ","σ(o’ω’o)","(๑•̀ㅂ•́)و✧",],
    "sad": ["(๑•̀д•́๑)","꒰ ๑͒ óｪò๑͒꒱","(* Ŏ∀Ŏ)","( ͡° ᴥ ͡°ʋ)","(‘-’*)","(´ω｀*)"],
}
idiomDict = jionlp.chinese_idiom_loader()

print("我们来玩成语接龙叭!")
print("我先来" + random.choice(emotionText["happy"]) + ":")
AiIdiom = idiom.sample()
print(AiIdiom)
chance = 3
while True:
    print("-" * 50)
    userIdiom = input("到你咯：")
    if not idiom.is_idiom(userIdiom) and userIdiom not in idiomDict:        
        print("这不是成语哦！", end="")
        if chance == 3:
            print("你还有3次机会哦！加油!")
        elif chance == 2:
            print("又错嘞(つ´ω`)つ 还剩2次机会 小心哟")
        elif chance == 1:
            print("最后一次机会啦！థ౪థ")
        else:
            print("机会用完了哦！我赢啦!(ﾉ>ω<)ﾉ")
            break
        chance -= 1
    else:
        answerprob = random.randint(1, 100)
        
        answerList = idiom.next_idioms_solitaire(userIdiom, 10)
        answer = ""
        while len(answer) != 4:
            answer = random.choice(answerList)
        
        if answerprob < 10:
            print("emmmm...我想想.....")
            time.sleep(random.randint(4, 7))
            print("啊啊啊啊啊.." + random.choice(emotionText["sad"]))
            time.sleep(random.randint(5, 9))
            print("呜呜 想不出来了(´;ω;`)")
            print("我认输了！你赢咯٩(ŏ﹏ŏ、)۶")
            break
        elif answerprob < 30:
            print("emmmm...我想想.....")
            time.sleep(random.randint(2, 4))
            print("啊啊啊...." + random.choice(emotionText["sad"]))
            time.sleep(random.randint(4, 7))
            print("哼哼!有啦! σ`∀´)σ")
            time.sleep(1)
            for c in answer:
                print(c, end="", flush=True)
                time.sleep(.75)
            print("!")
        
        elif answerprob < 60:
            print("emmmm...")
            time.sleep(random.randint(2, 4))
            print("再让我想想" + random.choice(emotionText["okay"]))
            time.sleep(random.randint(1, 4))
            print("有啦" + random.choice(emotionText["happy"]))
            time.sleep(1)
            print(answer)
        else:
            print("哼哼简单" + random.choice(emotionText["happy"]))
            time.sleep(1)
            print(answer)
        AiIdiom = answer
            