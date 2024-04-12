from utils.callgpt import API_KEYS
from utils.callgpt import call_gpt
import random
import json
import re

now_role = '''你是一个专业的医疗助手'''

prompt_list = '''以上是一段医学相关的文本资料，请你根据上述资料的内容，给出针对文本中知识的三对问答，提问和回答请用换行分开，不要有多余输出'''

WINDOW_SIZE = 3 # 设置滑动窗口的大小

def split_response(original):
    questions = original.split('\n')
    result = []
    for question in questions:
        question = re.sub(r':\s*', '', question) # 匹配冒号后的内容
        if len(question) > 5:# 要大于一定长度才保留，这里主要是为了防止多余空行
            result.append(question)
    return result

def process(qa_list,prompt): # 处理单条对话
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
    # 写入这三组问答
    qa_list[tmp[0]] = tmp[1]
    qa_list[tmp[2]] = tmp[3]
    qa_list[tmp[4]] = tmp[5]

def work():
    # 先读入input.txt
    f = open('input.txt', encoding='utf-8')
    txt = []
    for line in f: # 读取txt
        txt.append(line.strip())
    qa_list = {} # 这里使用字典，避免了重复问题

    # 这里开始询问了
    dl_num = len(txt) # 段落数量
    for i in range(dl_num - WINDOW_SIZE + 1): # 这里开始用大小为WINDOW_SIZE的窗口开始滑动
        print(f"[开始处理第{i}段]")
        prompt = ''.join(txt[i:i + WINDOW_SIZE])
        process(qa_list,prompt)

    # 写到json里
    with open("./qa_list.json", "w", encoding="utf-8") as f:
        json.dump(qa_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    work()