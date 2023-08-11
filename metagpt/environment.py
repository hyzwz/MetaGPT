#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 22:12
@Author  : alexanderwu
@File    : environment.py
"""
import asyncio  # 引入异步I/O库
from typing import Iterable  # 引入Iterable类型

from pydantic import BaseModel, Field  # 引入pydantic库的BaseModel和Field类

from metagpt.memory import Memory  # 引入Memory类
from metagpt.roles import Role  # 引入Role类
from metagpt.schema import Message  # 引入Message类


class Environment(BaseModel):
    """环境，承载一批角色，角色可以向环境发布消息，可以被其他角色观察到"""

    roles: dict[str, Role] = Field(default_factory=dict)  # 角色字段，用于存储环境中的所有角色
    memory: Memory = Field(default_factory=Memory)  # 内存字段，用于存储环境的内存
    history: str = Field(default='')  # 历史字段，用于存储环境的历史记录

    class Config:
        arbitrary_types_allowed = True  # 允许任意类型

    def add_role(self, role: Role):
        """增加一个在当前环境的Role"""
        role.set_env(self)  # 设置角色的环境为当前环境
        self.roles[role.profile] = role  # 将角色添加到环境中

    def add_roles(self, roles: Iterable[Role]):
        """增加一批在当前环境的Role"""
        for role in roles:  # 对于每一个角色
            self.add_role(role)  # 添加角色到环境中

    def publish_message(self, message: Message):
        """向当前环境发布信息"""
        self.memory.add(message)  # 将消息添加到内存中
        self.history += f"\n{message}"  # 将消息添加到历史记录中

    async def run(self, k=1):
        """处理一次所有Role的运行"""
        for _ in range(k):  # 对于每一轮
            futures = []  # 创建一个空的未来列表
            for role in self.roles.values():  # 对于每一个角色
                future = role.run()  # 运行角色
                futures.append(future)  # 将未来添加到未来列表中

            await asyncio.gather(*futures)  # 等待所有未来完成

    def get_roles(self) -> dict[str, Role]:
        """获得环境内的所有Role"""
        return self.roles  # 返回环境中的所有角色

    def get_role(self, name: str) -> Role:
        """获得环境内的指定Role"""
        return self.roles.get(name, None)  # 返回环境中的指定角色，如果不存在，则返回None