#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : action.py
"""
from abc import ABC
from typing import Optional

from tenacity import retry, stop_after_attempt, wait_fixed

from metagpt.actions.action_output import ActionOutput
from metagpt.llm import LLM
from metagpt.utils.common import OutputParser
from metagpt.logs import logger

class Action(ABC):
    def __init__(self, name: str = '', context=None, llm: LLM = None):
        # 初始化方法，设置动作的名称，上下文和LLM对象
        self.name: str = name
        if llm is None:
            llm = LLM()
        self.llm = llm
        self.context = context
        self.prefix = ""
        self.profile = ""
        self.desc = ""
        self.content = ""
        self.instruct_content = None

    def set_prefix(self, prefix, profile):
        """设置前缀和配置文件，这些信息可能会在后续的操作中使用"""
        self.prefix = prefix
        self.profile = profile

    def __str__(self):
        # 返回类的名称作为字符串表示
        return self.__class__.__name__

    def __repr__(self):
        # 返回类的名称作为类的官方字符串表示
        return self.__str__()

    async def _aask(self, prompt: str, system_msgs: Optional[list[str]] = None) -> str:
        """异步方法，添加默认前缀并调用LLM的aask方法"""
        if not system_msgs:
            system_msgs = []
        system_msgs.append(self.prefix)
        return await self.llm.aask(prompt, system_msgs)

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    async def _aask_v1(self, prompt: str, output_class_name: str,
                       output_data_mapping: dict,
                       system_msgs: Optional[list[str]] = None) -> ActionOutput:
        """Append default prefix"""
        if not system_msgs:
            system_msgs = []
        system_msgs.append(self.prefix)
        content = await self.llm.aask(prompt, system_msgs)
        logger.debug(content)
        output_class = ActionOutput.create_model_class(output_class_name, output_data_mapping)
        parsed_data = OutputParser.parse_data_with_mapping(content, output_data_mapping)
        logger.debug(parsed_data)
        instruct_content = output_class(**parsed_data)
        return ActionOutput(content, instruct_content)

    async def run(self, *args, **kwargs):
        """Run action"""
        raise NotImplementedError("The run method should be implemented in a subclass.")
