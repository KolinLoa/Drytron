import time
from enum import Enum
from typing import NoReturn

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Depends, RegexDict

from src.modules.search_record import SearchRecord
from src.params import PluginConfig, user_matcher_group
from src.utils.log import logger
from nonebot.plugin import PluginMetadata
import  os
__plugin_meta__ = PluginMetadata(
    name="剑三奇遇攻略查询", description="剑三奇遇攻略查询，数据源使用jx3box", usage="参考“帮助”", config=PluginConfig()
)

class REGEX(Enum):
    """匹配奇遇攻略查询"""
    奇遇攻略 = r"^攻略 (?P<value1>[\S]+)$|^(?P<value2>[\S]+)攻略$"

#====================Matcher====================
stratagy_query = user_matcher_group.on_regex(pattern=REGEX.奇遇攻略.value)

#   Dependency，用来获取相关参数及冷却实现

def get_value() -> str:
    """
    说明:
        Dependency，获取匹配字符串中的value字段
    """

    async def dependency(regex_dict: dict = RegexDict()) -> str:

        value = regex_dict.get("value1")
        return value if value else regex_dict.get("value2")

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


@stratagy_query.handle(parameterless=[cold_down(name="奇遇攻略查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = get_value()) -> NoReturn:
    """奇遇攻略查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 奇遇攻略查询 | 请求：{name}")
    file_name = f"{name}.png"
    file_path = os.path.join(os.getcwd(), "img", file_name)
    pic = MessageSegment.image('file:///' + file_path)
    if not os.path.exists(file_path):
        pic = f'你奶奶的，逗我呢！'

    await stratagy_query.finish(pic)