from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata

from src.internal.jx3api import JX3API
from src.modules.group_info import GroupInfo
from src.params import PluginConfig
from src.utils.log import logger

from .model import sand_manager

__plugin_meta__ = PluginMetadata(
    name="剑三沙盘",
    description="查看沙盘数据，数据使用：j3sp.com",
    usage="沙盘 [服务器]",
    config=PluginConfig(),
)

api = JX3API()
"""jx3api接口实例"""


sand_query = on_regex(
    pattern=r"^沙盘$|^沙盘 (?P<server>[\u4e00-\u9fa5]+)$",
    permission=GROUP,
    priority=5,
    block=True,
)


async def get_server(
    matcher: Matcher, event: GroupMessageEvent, regex_dict: dict = RegexDict()
) -> str:
    """
    说明:
        Dependency，获取匹配字符串中的server，如果没有则获取群绑定的默认server
    """
    _server = regex_dict.get("server")
    if _server:
        server = api.app_server(name=_server)
        if not server:
            msg = f"未找到服务器[{_server}]，请验证后查询。"
            await matcher.finish(msg)
    else:
        server = await GroupInfo.get_server(event.group_id)
    return server


@sand_query.handle()
async def _(event: GroupMessageEvent, server: str = Depends(get_server)):
    """沙盘查询"""

    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 沙盘查询 | 请求：{server}"
    )
    sand_data = await sand_manager.get_sand_pic(server)
    if sand_data.code != 1:
        await sand_query.finish(sand_data.msg)

    msg = (
        f"[{server}]沙盘 更新时间：{sand_data.data.sand_data.createTime}"
        + MessageSegment.image(sand_data.data.sand_data.sandImage)
    )
    await sand_query.finish(msg)
