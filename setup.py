"""wutils: handy tools
"""
import subprocess   # 引入子进程库
from codecs import open  # 引入编解码库
from os import path   # 引入操作系统路径库

from setuptools import Command, find_packages, setup  # 引入setuptools库


class InstallMermaidCLI(Command):
    """一个自定义命令，通过子进程运行 `npm install -g @mermaid-js/mermaid-cli` via a subprocess."""

    description = "install mermaid-cli"  # 命令描述
    user_options = []  # 用户选项

    def run(self):
        try:
            subprocess.check_call(["npm", "install", "-g", "@mermaid-js/mermaid-cli"])
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e.output}")


here = path.abspath(path.dirname(__file__))  # 获取当前文件的绝对路径

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()  # 读取文件内容

with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line]  # 读取文件内容

setup(
    name="metagpt",   # 项目名称
    version="0.1",    # 项目版本
    description="The Multi-Role Meta Programming Framework", # 项目描述
    long_description=long_description,  # 项目长描述
    long_description_content_type="text/markdown",  # 长描述内容类型
    url="https://gitlab.deepwisdomai.com/pub/metagpt",  # 项目URL
    author="Alexander Wu",   # 作者
    author_email="alexanderwu@fuzhi.ai",  # 作者邮箱
    license="Apache 2.0",  # 许可证
    keywords="metagpt multi-role multi-agent programming gpt llm",    # 关键词
    packages=find_packages(exclude=["contrib", "docs", "examples"]),  # 包含的包
    python_requires=">=3.9",   # Python版本要求
    install_requires=requirements,  # 安装要求
    extras_require={   # 额外要求
        "playwright": ["playwright>=1.26", "beautifulsoup4"],
        "selenium": ["selenium>4", "webdriver_manager<3.9", "beautifulsoup4"],
    },
    cmdclass={  # 自定义命令
        "install_mermaid": InstallMermaidCLI,
    },
)
