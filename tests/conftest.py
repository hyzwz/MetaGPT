#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/1 12:10
@Author  : alexanderwu
@File    : conftest.py
"""

from unittest.mock import Mock # 引入mock库

import pytest  # 引入pytest库

from metagpt.logs import logger  # 引入日志库
from metagpt.provider.openai_api import OpenAIGPTAPI as GPTAPI # 引入GPTAPI
import asyncio  # 引入异步I/O库
import re       # 引入正则表达式库


class Context:
    """定义一个上下文类，包含一个GPTAPI实例。"""
    def __init__(self):
        self._llm_ui = None
        self._llm_api = GPTAPI()

    @property
    def llm_api(self):
        return self._llm_api


@pytest.fixture(scope="package")
def llm_api():
    """定义一个package级别的fixture，返回一个GPTAPI实例。"""
    logger.info("Setting up the test")
    _context = Context()

    yield _context.llm_api

    logger.info("Tearing down the test")


@pytest.fixture(scope="function")
def mock_llm():
    """定义一个function级别的fixture，返回一个mock对象。"""
    return Mock()


@pytest.fixture(scope="session")
def proxy():
    """定义一个session级别的fixture，返回一个代理服务器的地址。"""
    pattern = re.compile(
        rb"(?P<method>[a-zA-Z]+) (?P<uri>(\w+://)?(?P<host>[^\s\'\"<>\[\]{}|/:]+)(:(?P<port>\d+))?[^\s\'\"<>\[\]{}|]*) "
    )

    async def pipe(reader, writer):
        """定义一个异步函数，用于读取和写入数据。"""
        while not reader.at_eof():
            writer.write(await reader.read(2048))
        writer.close()

    async def handle_client(reader, writer):
        """定义一个异步函数，用于处理客户端的请求。"""
        data = await reader.readuntil(b"\r\n\r\n")
        print(f"Proxy: {data}")  # checking with capfd fixture
        infos = pattern.match(data)
        host, port = infos.group("host"), infos.group("port")
        port = int(port) if port else 80
        remote_reader, remote_writer = await asyncio.open_connection(host, port)
        if data.startswith(b"CONNECT"):
            writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        else:
            remote_writer.write(data)
        await asyncio.gather(pipe(reader, remote_writer), pipe(remote_reader, writer))

    server = asyncio.get_event_loop().run_until_complete(asyncio.start_server(handle_client, "127.0.0.1", 0))
    return "http://{}:{}".format(*server.sockets[0].getsockname())
