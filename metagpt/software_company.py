#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/12 00:30
@Author  : alexanderwu
@File    : software_company.py
"""
from pydantic import BaseModel, Field  # 引入pydantic库的BaseModel和Field类

from metagpt.actions import BossRequirement  # 引入BossRequirement类
from metagpt.config import CONFIG  # 引入全局配置
from metagpt.environment import Environment  # 引入Environment类
from metagpt.logs import logger  # 引入日志库
from metagpt.roles import Role  # 引入Role类
from metagpt.schema import Message  # 引入Message类
from metagpt.utils.common import NoMoneyException  # 引入NoMoneyException类


class SoftwareCompany(BaseModel):
    """
    软件公司：拥有一个团队、标准操作程序（SOP）和即时通讯平台，致力于编写可执行代码。
    """
    environment: Environment = Field(default_factory=Environment)  # 环境字段，用于存储公司的环境
    investment: float = Field(default=10.0)  # 投资字段，用于存储公司的投资金额
    idea: str = Field(default="")  # 想法字段，用于存储公司的项目想法

    class Config:
        arbitrary_types_allowed = True  # 允许任意类型

    def hire(self, roles: list[Role]):
        """雇佣角色以进行合作"""
        self.environment.add_roles(roles)  # 在环境中添加角色

    def invest(self, investment: float):
        """投资公司。当超过最大预算时，抛出NoMoneyException。"""
        self.investment = investment  # 设置投资金额
        CONFIG.max_budget = investment  # 设置最大预算
        logger.info(f'Investment: ${investment}.')  # 记录投资信息

    def _check_balance(self):
        """检查余额。当总成本超过最大预算时，抛出NoMoneyException。"""
        if CONFIG.total_cost > CONFIG.max_budget:  # 如果总成本超过最大预算
            raise NoMoneyException(CONFIG.total_cost, f'Insufficient funds: {CONFIG.max_budget}')  # 抛出NoMoneyException

    def start_project(self, idea):
        """从发布老板需求开始一个项目。"""
        self.idea = idea  # 设置项目想法
        self.environment.publish_message(Message(role="BOSS", content=idea, cause_by=BossRequirement))  # 发布消息

    def _save(self):
        """保存公司信息。"""
        logger.info(self.json())  # 记录公司信息

    async def run(self, n_round=3):
        """运行公司，直到达到目标轮数或没有钱"""
        while n_round > 0:  # 当还有剩余轮数时
            # self._save()  # 保存公司信息
            n_round -= 1  # 轮数减一
            logger.debug(f"{n_round=}")  # 记录剩余轮数
            self._check_balance()  # 检查余额
            await self.environment.run()  # 运行环境
        return self.environment.history  # 返回环境历史