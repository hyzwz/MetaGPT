#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/5 23:00
@Author  : alexanderwu
@File    : base_chatbot.py
"""
from abc import ABC, abstractmethod  # 引入抽象基类和抽象方法装饰器
from dataclasses import dataclass  # 引入数据类装饰器


@dataclass
class BaseChatbot(ABC):
    """定义一个抽象的聊天机器人类"""
    mode: str = "API"  # 定义一个模式字段，初始值为"API"

    @abstractmethod
    def ask(self, msg: str) -> str:
        """定义一个抽象方法，用于向聊天机器人提问并获取答案"""

    @abstractmethod
    def ask_batch(self, msgs: list) -> str:
        """定义一个抽象方法，用于向聊天机器人提出一系列问题并获取一系列答案"""

    @abstractmethod
    def ask_code(self, msgs: list) -> str:
        """定义一个抽象方法，用于向聊天机器人提出一系列问题并获取一段代码"""