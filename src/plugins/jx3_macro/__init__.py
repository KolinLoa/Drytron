import time
from enum import Enum
from typing import NoReturn

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.params import Depends, RegexDict

from src.modules.search_record import SearchRecord
from src.params import PluginConfig, user_matcher_group
from src.utils.log import logger
from nonebot.plugin import PluginMetadata

from .config import JX3PROFESSION

__plugin_meta__ = PluginMetadata(
    name="剑三宏查询", description="剑三宏查询，数据源使用jx3box", usage="参考“帮助”", config=PluginConfig()
)
class REGEX(Enum):
    查宏命令 = r"^宏 (?P<value1>[\S]+)$|^(?P<value2>[\S]+)宏$"

# ======matcher=========
macro_query = user_matcher_group.on_regex(pattern=REGEX.查宏命令.value)

# =======获取相关参数=======
def get_value() -> str:
    """
    说明:
        Dependency，获取匹配字符串中的value字段
    """

    async def dependency(regex_dict: dict = RegexDict()) -> str:

        value = regex_dict.get("value1")
        return value if value else regex_dict.get("value2")

    return Depends(dependency)


def get_profession() -> str:
    """
    说明:
        Dependency，通过别名获取职业名称
    """

    async def dependency(matcher: Matcher, name: str = get_value()) -> str:

        profession = JX3PROFESSION.get_profession(name)
        if profession:
            return profession

        # 未找到职业
        msg = f"未找到职业[{name}]，请检查参数。"
        await matcher.finish(msg)

    return Depends(dependency)


def cold_down(name: str, cd_time: int) -> None:
    """
    说明:
        Dependency，增加命令冷却，同时会在数据库中记录一次查询

    参数:
        * `name`：app名称，相同名称会使用同一组cd
        * `cd_time`：冷却时间

    用法:
    ```
        @matcher.handle(parameterless=[cold_down(name="app", cd_time=0)])
        async def _():
            pass
    ```
    """

    async def dependency(matcher: Matcher, event: GroupMessageEvent):
        time_last = await SearchRecord.get_search_time(event.group_id, name)
        time_now = int(time.time())
        over_time = over_time = time_now - time_last
        if over_time > cd_time:
            await SearchRecord.use_search(event.group_id, name)
            return
        else:
            left_cd = cd_time - over_time
            await matcher.finish(f"[{name}]冷却中 ({left_cd})")

    return Depends(dependency)

@macro_query.handle(parameterless=[cold_down(name="宏查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = get_profession()) -> NoReturn:
    """宏查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 宏查询 | 请求：{name}")
    if name == '冰心诀':
        msg = (f"https://www.jx3box.com/macro/?subtype=%E5%86%B0%E5%BF%83%E8%AF%80")
    elif name == '云裳心经':
        msg = (f"https://www.jx3box.com/macro/?subtype=%E4%BA%91%E8%A3%B3%E5%BF%83%E7%BB%8F")
    elif name == '花间游':
        msg = (f"花椒油侠士有福了，你的一键宏来了。https://www.jx3box.com/macro/?subtype=%E8%8A%B1%E9%97%B4%E6%B8%B8")
    elif name == '离经易道':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E8%8A%B1%E9%97%B4%E6%B8%B8')
    elif name == '毒经':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E6%AF%92%E7%BB%8F')
    elif name == '补天诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E8%A1%A5%E5%A4%A9%E8%AF%80')
    elif name == '莫问':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E8%8E%AB%E9%97%AE')
    elif name == '相知':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E7%9B%B8%E7%9F%A5')
    elif name == '无方':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E6%97%A0%E6%96%B9')
    elif name == '灵素':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E7%81%B5%E7%B4%A0')
    elif name == '傲血战意':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%82%B2%E8%A1%80%E6%88%98%E6%84%8F')
    elif name == '铁牢律':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E9%93%81%E7%89%A2%E5%BE%8B')
    elif name == '易筋经':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E6%98%93%E7%AD%8B%E7%BB%8F')
    elif name == '洗髓经':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E6%B4%97%E9%AB%93%E7%BB%8F')
    elif name == '焚影圣诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E7%84%9A%E5%BD%B1%E5%9C%A3%E8%AF%80')
    elif name == '明尊琉璃体':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E6%98%8E%E5%B0%8A%E7%90%89%E7%92%83%E4%BD%93')
    elif name == '分山劲':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%88%86%E5%B1%B1%E5%8A%B2')
    elif name == '铁骨衣':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E9%93%81%E9%AA%A8%E8%A1%A3')
    elif name == '紫霞功':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E7%B4%AB%E9%9C%9E%E5%8A%9F')
    elif name == '太虚剑意':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%A4%AA%E8%99%9A%E5%89%91%E6%84%8F')
    elif name == '天罗诡道':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%A4%A9%E7%BD%97%E8%AF%A1%E9%81%93')
    elif name == '惊羽诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E6%83%8A%E7%BE%BD%E8%AF%80')
    elif name == '问水诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E9%97%AE%E6%B0%B4%E8%AF%80')
    elif name == '笑尘决':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E7%AC%91%E5%B0%98%E8%AF%80')
    elif name == '北傲决':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%8C%97%E5%82%B2%E8%AF%80')
    elif name == '凌海诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%87%8C%E6%B5%B7%E8%AF%80')
    elif name == '隐龙诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E9%9A%90%E9%BE%99%E8%AF%80')
    elif name == '太玄经':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%A4%AA%E7%8E%84%E7%BB%8F')
    elif name == '孤锋诀':
        msg = (f'https://www.jx3box.com/macro/?subtype=%E5%AD%A4%E9%94%8B%E8%AF%80')


    await macro_query.finish(msg)