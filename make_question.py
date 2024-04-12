from utils.callgpt import API_KEYS
from utils.callgpt import call_gpt
import random
import json
import re

now_role = '''你是一个专业的农业助手'''

prompt_list = '''以上是一段农业相关的文本资料，请你根据上述资料的内容，提出两个相关的问题，和两个与文本无关的假问题，用换行隔开。 '''

WINDOW_SIZE = 10 # 设置滑动窗口的大小
STRIDE = 3

def split_response(original):
    questions = original.split('\n')
    result = []
    for question in questions:
        question = re.sub(r':\s*', '', question) # 匹配冒号后的内容
        if len(question) > 7:# 要大于一定长度才保留，这里主要是为了防止多余空行
            # 而且有些时候会有“相关问题：”这样的一行，所以也要去除
            result.append(question)
    return result

def process(context,prompt): # 处理单条对话
    prompt = prompt + '\n' + random.choice(prompt_list.split('\n'))
    print(prompt)
    # role = random.choice(now_role.split('\n')
    while True: # 因为openai限制API一定时间内的询问次数，也有可能是这个KEY余额不够，就会出现报错
        # 所以这里要一直try
        try:
            # 获得随机keys
            key = random.choice(API_KEYS.split('\n'))
            rt = call_gpt(now_role, prompt, key)
            break
        except Exception as e:
            print(f'报错：{e}')
    # 再根据问答处理以下
    tmp = split_response(rt)
    print(tmp) # 打印输出

    for i in range(len(tmp)):
        pattern = r'^\d+[\.、.]\s*'
        # 去除开头的编号
        tmp[i] = re.sub(pattern, '', tmp[i], count=1).strip() # 并且去除空格

    dct = {}
    dct['query'] = ''.join(context) # 这里叫query，实际上是context，我也不知道为什么bge微调格式里面context要放在dict的query里
    dct['pos'] = [tmp[0],tmp[1]]
    dct['neg'] = [tmp[1],tmp[2]]
    with open('agritext.jsonl', 'a', encoding="utf-8") as f: # 用w会覆盖，a就不会
        f.write(json.dumps(dct,ensure_ascii=False) + '\n') # 如果不加ensure_ascii=false的话，会输出的是编码不是中文

def work():
    # 先读入input.txt
    f = open('text_out.txt', encoding='utf-8')
    txt = []
    for line in f: # 读取txt
        txt.append(line.strip())

    # 这里开始询问了
    dl_num = len(txt) # 段落数量
    for i in range(0, dl_num - WINDOW_SIZE + 1, STRIDE): # 这里开始用大小为WINDOW_SIZE的窗口开始滑动
        print(f"[开始处理第{i}段]")
        prompt = ''.join(txt[i:i + WINDOW_SIZE])
        process(txt[i:i + WINDOW_SIZE],prompt)

if __name__ == "__main__":
    work()

'''BGE微调格式如下
{"query": "Five women walk along a beach wearing flip-flops.", "pos": ["Some women with flip-flops on, are walking along the beach"], "neg": ["The 4 women are sitting on the beach.", "There was a reform in 1996.", "She's not going to court to clear her record.", "The man is talking about hawaii.", "A woman is standing outside.", "The battle was over. ", "A group of people plays volleyball."]}
{"query": "A woman standing on a high cliff on one leg looking over a river.", "pos": ["A woman is standing on a cliff."], "neg": ["A woman sits on a chair.", "George Bush told the Republicans there was no way he would let them even consider this foolish idea, against his top advisors advice.", "The family was falling apart.", "no one showed up to the meeting", "A boy is sitting outside playing in the sand.", "Ended as soon as I received the wire.", "A child is reading in her bedroom."]}
{"query": "Two woman are playing instruments; one a clarinet, the other a violin.", "pos": ["Some people are playing a tune."], "neg": ["Two women are playing a guitar and drums.", "A man is skiing down a mountain.", "The fatal dose was not taken when the murderer thought it would be.", "Person on bike", "The girl is standing, leaning against the archway.", "A group of women watch soap operas.", "No matter how old people get they never forget. "]}
{"query": "A girl with a blue tank top sitting watching three dogs.", "pos": ["A girl is wearing blue."], "neg": ["A girl is with three cats.", "The people are watching a funeral procession.", "The child is wearing black.", "Financing is an issue for us in public schools.", "Kids at a pool.", "It is calming to be assaulted.", "I face a serious problem at eighteen years old. "]}
{"query": "A yellow dog running along a forest path.", "pos": ["a dog is running"], "neg": ["a cat is running", "Steele did not keep her original story.", "The rule discourages people to pay their child support.", "A man in a vest sits in a car.", "Person in black clothing, with white bandanna and sunglasses waits at a bus stop.", "Neither the Globe or Mail had comments on the current state of Canada's road system. ", "The Spring Creek facility is old and outdated."]}
{"query": "It sets out essential activities in each phase along with critical factors related to those activities.", "pos": ["Critical factors for essential activities are set out."], "neg": ["It lays out critical activities but makes no provision for critical factors related to those activities.", "People are assembled in protest.", "The state would prefer for you to do that.", "A girl sits beside a boy.", "Two males are performing.", "Nobody is jumping", "Conrad was being plotted against, to be hit on the head."]}
{"query": "A man giving a speech in a restaurant.", "pos": ["A person gives a speech."], "neg": ["The man sits at the table and eats food.", "This is definitely not an endorsement.", "They sold their home because they were retiring and not because of the loan.", "The seal of Missouri is perfect.", "Someone is raising their hand.", "An athlete is competing in the 1500 meter swimming competition.", "Two men watching a magic show."]}
{"query": "Indians having a gathering with coats and food and drinks.", "pos": ["A group of Indians are having a gathering with food and drinks"], "neg": ["A group of Indians are having a funeral", "It is only staged on Winter afternoons in Palma's large bullring.", "Right information can empower the legal service practices and the justice system. ", "Meanwhile, the mainland was empty of population.", "Two children is sleeping.", "a fisherman is trying to catch a monkey", "the people are in a train"]}
{"query": "A woman with violet hair rides her bicycle outside.", "pos": ["A woman is riding her bike."], "neg": ["A woman is jogging in the park.", "The street was lined with white-painted houses.", "A group watches a movie inside.", "man at picnics cut steak", "Several chefs are sitting down and talking about food.", "The Commission notes that no significant alternatives were considered.", "We ran out of firewood and had to use pine needles for the fire."]}
{"query": "A man pulls two women down a city street in a rickshaw.", "pos": ["A man is in a city."], "neg": ["A man is a pilot of an airplane.", "It is boring and mundane.", "The morning sunlight was shining brightly and it was warm. ", "Two people jumped off the dock.", "People watching a spaceship launch.", "Mother Teresa is an easy choice.", "It's worth being able to go at a pace you prefer."]}
'''