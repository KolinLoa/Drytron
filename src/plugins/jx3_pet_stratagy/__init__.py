import time
from enum import Enum
import requests
import re
from typing import NoReturn

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.params import Depends, RegexDict

from src.modules.search_record import SearchRecord
from src.params import PluginConfig, user_matcher_group
from src.utils.log import logger
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="剑三宠物奇缘查询", description="剑三宠物奇缘查询，数据源使用jx3box", usage="参考“帮助”", config=PluginConfig()
)

class REGEX(Enum):
    """匹配宠物奇缘查询"""
    宠物奇缘攻略 = r"^宠物 (?P<value1>[\S]+)$|^(?P<value2>[\S]+)宠物$"

#====================Matcher====================
pet_stratagy_query = user_matcher_group.on_regex(pattern=REGEX.宠物奇缘攻略.value)

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

#====================爬取参数===================

url = 'https://node.jx3box.com/serendipities?type=pet&page=4&per=4'
response = requests.get(url) # get the page with the links to all the serendipity commences.

dwIDs = re.findall(r'"dwID":(\d+)', response.text)
szNames = re.findall(r'"szName":"(.*?)"', response.text)
list_str4 = szNames
list_num4 = dwIDs
list_new4 = {key: value for key, value in zip(list_str4, list_num4)}

url = 'https://node.jx3box.com/serendipities?type=pet&page=3&per=20'
response = requests.get(url)
dwIDs = re.findall(r'"dwID":(\d+)', response.text)
szNames = re.findall(r'"szName":"(.*?)"', response.text)
list_str3 = szNames
list_num3 = dwIDs
list_new3 = {key: value for key, value in zip(list_str3, list_num3)}

url = 'https://node.jx3box.com/serendipities?type=pet&page=2&per=20'
response = requests.get(url)
dwIDs = re.findall(r'"dwID":(\d+)', response.text)
szNames = re.findall(r'"szName":"(.*?)"', response.text)
list_str2 = szNames
list_num2 = dwIDs
list_new2 = {key: value for key, value in zip(list_str2, list_num2)}

url = 'https://node.jx3box.com/serendipities?type=pet&page=1&per=20'
response = requests.get(url)
dwIDs = re.findall(r'"dwID":(\d+)', response.text)
szNames = re.findall(r'"szName":"(.*?)"', response.text)
list_str1 = szNames
list_num1 = dwIDs
list_new1 = {key: value for key, value in zip(list_str1, list_num1)}

# ==============handler===============
@pet_stratagy_query.handle(parameterless=[cold_down(name="宠物奇缘查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = get_value()) -> NoReturn:
    """宠物奇缘查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 宠物奇缘查询 | 请求：{name}")
    key = name
    list_num1 = list_new1.get(key)
    list_num2 = list_new2.get(key)
    list_num3 = list_new3.get(key)
    list_num4 = list_new4.get(key)
    url = 'https://jx3box.com/adventure/'
    if list_num1 is not None:
        result_url = url + list_num1
        msg = (result_url)
    elif list_num2 is not None:
        result_url = url + list_num2
        msg = (result_url)
    elif list_num3 is not None:
        result_url = url + list_num3
        msg = (result_url)
    elif list_num4 is not None:
        result_url = url + list_num4
        msg = (result_url)
    else:
        print('尼玛根本没有这个宠物奇缘，逗我呢！')


    await pet_stratagy_query.finish(msg)