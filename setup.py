import setuptools
import ast
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

def get_version() -> str:
    black_py = CURRENT_DIR / "linkedin_slack_bot/__init__.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(black_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setuptools.setup(
    name="linkedin_slack_bot",
    version=get_version(),
    author="Haseeb Ahmed",
    description="Python Linkedin Slack Bot",
    packages=setuptools.find_packages(),
    install_requires=["requests", "beautifulsoup4", "lxml" , "demoji" , "slackclient" , "slack"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)