#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/7/21 11:15
@Author  : Leo Xiao
@File    : anthropic_api.py
"""

import requests  # 引入requests库
# import anthropic  # 引入anthropic库
# from anthropic import Anthropic  # 从anthropic库中引入Anthropic类
import anthropic
from metagpt.config import CONFIG  # 引入全局配置
import uuid  # 引入uuid库
import re  # 引入正则表达式库
import json  # 引入json库
import aiohttp  # 引入aiohttp库


class Claude2:
    """定义一个Claude2类，用于与Anthropic的Claude-2模型进行交互。"""
    def __init__(self):
        """初始化Claude2类，从全局配置中获取organization_uuid和cookie。"""
        self.cookie = CONFIG.cookie
        self.organization_uuid = CONFIG.organization_uuid
        self.conversation_uuid = CONFIG.conversation_uuid
        self.headers = {
            "Cookie": CONFIG.cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79",
            "Referer": f"https://claude.ai/chat/{CONFIG.conversation_uuid}",
        }

        # 创建对话
        url = f"https://claude.ai/api/organizations/{self.organization_uuid}/chat_conversations"
        uuid4 = str(uuid.uuid4()) if self.conversation_uuid == "" else self.conversation_uuid
        payload = {
            "name": '',  # 这个name我不知道该写什么，先这么写吧
            "uuid": uuid4
        }
        print(url, payload)
        response = requests.request('POST', url, json=payload, headers=self.headers)
        if response.status_code == 201:
            self.conversation_uuid = uuid4


    def ask(self, prompt):
        """向Claude-2模型发送一个同步的请求，并返回结果。"""
        # 发送消息并接收消息
        url = f"https://claude.ai/api/append_message"
        payload = {
            "completion": {
                "prompt": prompt,
                "timezone": "Asia/Shanghai",
                "model": "claude-2"
            },
            "organization_uuid": self.organization_uuid,
            "conversation_uuid": self.conversation_uuid,
            "text": prompt,
        }
        response = requests.request("POST", url, json=payload, headers=self.headers)
        response.encoding = 'utf-8'
        if response.status_code in [200, 201]:
            pattern = re.compile(r'data: (.*?)"type":"within_limit"}}', re.DOTALL)
            match = re.findall(pattern, response.text)
            if len(match) > 0:
                text = match[-1] + '"type":"within_limit"}}'
                text = json.loads(text.strip())["completion"]
                # print(text)
                print("发送消息成功", text)
                return text
        else:
            return False
    
        # res = client.completions.create(
        #     model="claude-2",  # 指定模型为Claude-2
        #     prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",  # 设置提示
        #     max_tokens_to_sample=1000,  # 设置最大令牌数为1000
        # )
        # return res.completion  # 返回结果

    async def aask(self, prompt):
        """异步向Claude-2模型发送一个请求，并返回结果。"""
        # 发送消息并接收消息
        url = f"https://claude.ai/api/append_message"
        payload = {
            "completion": {
                "prompt": prompt,
                "timezone": "Asia/Shanghai",
                "model": "claude-2"
            },
            "organization_uuid": self.organization_uuid,
            "conversation_uuid": self.conversation_uuid,
            "text": prompt,
        }
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200 or response.status == 201:
                    text = await response.text()

                    # 使用正则表达式匹配响应文本中的数据
                    pattern = re.compile(r'data: (.*?)"type":"within_limit"}}', re.DOTALL)
                    match = re.findall(pattern, text)
                    completions = []
                    if len(match) > 0:
                        for item in match:
                            item=item + '"type":"within_limit"}}'
                            item_json = json.loads(item)
                            completion = item_json.get("completion", "")
                            completions.append(completion)
                            
                        text = "".join(completions)
                        print("发送消息成功", text)
                        return text
                else:
                    return False