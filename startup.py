#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio   # 引入异步I/O库

import fire  # 引入命令行参数处理库

from metagpt.roles import Architect, Engineer, ProductManager, ProjectManager  # 引入各种角色
from metagpt.software_company import SoftwareCompany   # 引入软件公司类


async def startup(idea: str, investment: float = 3.0, n_round: int = 5, code_review: bool = False):
    """运行一个创业公司。做老板。"""
    company = SoftwareCompany()   # 创建一个软件公司
    # 雇佣产品经理、架构师、项目经理和工程师
    company.hire([ProductManager(),
                  Architect(),
                  ProjectManager(),
                  Engineer(n_borg=5, use_code_review=code_review)])
    company.invest(investment)   # 投资
    company.start_project(idea)   # 开始项目
    await company.run(n_round=n_round)  # 运行公司


def main(idea: str, investment: float = 3.0, n_round: int = 5, code_review: bool = False):
    """
    我们是一个由AI组成的软件创业公司。投资我们，你就是在赋能一个充满无限可能的未来。
    :param idea: 你的创新想法，比如"创建一个贪吃蛇游戏"。
    :param investment: 作为投资者，你有机会向这个AI公司投入一定的资金。
    :param n_round: 运行的轮数。
    :param code_review: 是否使用代码审查。
    :return: 无返回值
    """
    asyncio.run(startup(idea, investment, n_round, code_review))


if __name__ == '__main__':
    fire.Fire(main)  # 使用fire库处理命令行参数，并运行main函数
