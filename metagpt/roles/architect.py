#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : architect.py
"""

from metagpt.actions import WriteDesign, WritePRD  # 引入WriteDesign和WritePRD类
from metagpt.roles import Role  # 引入Role类


class Architect(Role):
    """架构师：负责听取PRD，设计API，设计代码文件"""
    def __init__(self, name="Bob", profile="Architect", goal="Design a concise, usable, complete python system",
                 constraints="Try to specify good open source tools as much as possible"):
        super().__init__(name, profile, goal, constraints)  # 调用父类的
        