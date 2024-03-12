from callgpt import API_KEYS
from callgpt import call_gpt
import random
import json

now_role = '''你是一个专业的医疗助手'''

prompt_list = '''以上是一段医学相关的文本资料，请你根据上述资料的内容，给出针对文本中知识的一问一答，提问和回答请用换行分开，不要有多余输出'''

def process(qa_list,prompt): # 处理单条对话
    prompt = prompt + '\n' + random.choice(prompt_list.split('\n'))
    key =  random.choice(API_KEYS.split('\n'))
    # role = random.choice(now_role.split('\n')
    # 获得随机prompt和keys
    rt = call_gpt(now_role, prompt, key)
    # 再根据问答处理以下
    tmp = rt.split('\n')
    print(tmp)
    qa_list[tmp[0]] = tmp[1] # 写入问答

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