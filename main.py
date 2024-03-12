from utils.callgpt import API_KEYS
from utils.callgpt import call_gpt
import random
import json
import re

now_role = '''你是一个专业的医疗助手'''

prompt_list = '''以上是一段医学相关的文本资料，请你根据上述资料的内容，给出针对文本中知识的三对问答，提问和回答请用换行分开，不要有多余输出'''

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
    key =  random.choice(API_KEYS.split('\n'))
    # role = random.choice(now_role.split('\n')
    # 获得随机prompt和keys
    rt = call_gpt(now_role, prompt, key)
    # 再根据问答处理以下
    tmp = split_response(rt)
    print(tmp)
    # 写入这三组问答
    qa_list[tmp[0]] = tmp[1]
    qa_list[tmp[2]] = tmp[3]
    qa_list[tmp[4]] = tmp[5]

def work():
    # 先读入input.txt
    f = open('input.txt', encoding='utf-8')
    txt = []
    for line in f:
        txt.append(line.strip())
    qa_list = {}
    for t in txt:
        process(qa_list, t)
    with open("./qa_list.json", "w", encoding="utf-8") as f:
        json.dump(qa_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    work()