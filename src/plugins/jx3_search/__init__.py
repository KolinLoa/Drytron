import time
from enum import Enum
from typing import NoReturn, Optional

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata

from src.internal.jx3api import JX3API
from src.modules.group_info import GroupInfo
from src.modules.search_record import SearchRecord
from src.modules.ticket_info import TicketInfo
from src.params import PluginConfig, user_matcher_group
from src.utils.browser import browser
from src.utils.log import logger

from . import data_source as source

__plugin_meta__ = PluginMetadata(
    name="剑三查询", description="剑三游戏查询，数据源使用jx3api", usage="参考“帮助”", config=PluginConfig()
)

api = JX3API()
"""jx3api接口实例"""

BOT = "龙辉巧Drytron"


# ----------------------------------------------------------------
#   正则枚举，已实现的查询功能
# ----------------------------------------------------------------


class REGEX(Enum):
    """正则枚举"""

    日常任务 = r"^日常$|^日常 (?P<server>[\S]+)$"
    开服检查 = r"^开服$|^开服 (?P<server>[\S]+)$"
    金价比例 = r"^金价$|^金价 (?P<server>[\S]+)$"
    推荐小药 = r"^小药 (?P<value1>[\S]+)$|^(?P<value2>[\S]+)小药$"
    推荐装备 = r"^配装 (?P<value1>[\S]+)$|^(?P<value2>[\S]+)配装$"
    阵眼效果 = r"^阵眼 (?P<value1>[\S]+)$|^(?P<value2>[\S]+)阵眼$"
    物品价格 = r"^物价 (?P<value1>[\S]+)$"
    随机骚话 = r"^骚话$"
    更新公告 = r"^更新$|^公告$|^更新公告$"
    奇遇查询 = r"^查询 (?P<value1>[\S]+)$|^查询 (?P<server>[\S]+) (?P<value2>[\S]+)$"
    奇遇统计 = r"^奇遇 (?P<value1>[\S]+)$|^奇遇 (?P<server>[\S]+) (?P<value2>[\S]+)$"
    奇遇汇总 = r"^汇总$|^汇总 (?P<server>[\S]+)$"
    比赛战绩 = r"^战绩 (?P<value1>[\S]+)$|^战绩 (?P<server>[\S]+) (?P<value2>[\S]+)$"
    装备属性 = r"^(?:(?:装备)|(?:属性)) (?P<value1>[\S]+)$|^(?:(?:装备)|(?:属性)) (?P<server>[\S]+) (?P<value2>[\S]+)$"
    烟花记录 = r"^烟花 (?P<value1>[\S]+)$|^烟花 (?P<server>[\S]+) (?P<value2>[\S]+)$"
    招募查询 = r"^招募$|^招募 (?P<server1>[\S]+)$|^招募 (?P<server2>[\S]+) (?P<keyword>[\S]+)$"
    资历榜 = r"^资历榜$|^资历榜 (?P<server1>[\S]+)$|^资历榜 (?P<server2>[\S]+) (?P<keyword>[\S]+)$"
    声望榜 = r"^(?P<type1>声望榜)$|^(?P<type2>声望榜) (?P<server>[\S]+)$"
    老江湖 = r"^(?P<type1>老江湖)$|^(?P<type2>老江湖) (?P<server>[\S]+)$"
    兵甲榜 = r"^(?P<type1>兵甲榜)$|^(?P<type2>兵甲榜) (?P<server>[\S]+)$"
    名师榜 = r"^(?P<type1>名师榜)$|^(?P<type2>名师榜) (?P<server>[\S]+)$"
    战阶榜 = r"^(?P<type1>战阶榜)$|^(?P<type2>战阶榜) (?P<server>[\S]+)$"
    薪火榜 = r"^(?P<type1>薪火榜)$|^(?P<type2>薪火榜) (?P<server>[\S]+)$"
    梓行榜 = r"^(?P<type1>梓行榜)$|^(?P<type2>梓行榜) (?P<server>[\S]+)$"
    爱心榜 = r"^(?P<type1>爱心榜) (?P<value1>[\S]+)$|^(?P<type2>爱心榜) (?P<server>[\S]+) (?P<value2>[\S]+)$"
    神兵榜 = r"^(?P<type1>神兵榜) (?P<value1>[\S]+)$|^(?P<type2>神兵榜) (?P<server>[\S]+) (?P<value2>[\S]+)$"
    试炼榜 = r"^试炼榜 (?P<value1>[\S]+)$|^试炼榜 (?P<server>[\S]+) (?P<value2>[\S]+)$"


# ----------------------------------------------------------------
#   matcher列表，定义查询的mathcer
# ----------------------------------------------------------------
daily_query = user_matcher_group.on_regex(pattern=REGEX.日常任务.value)
server_query = user_matcher_group.on_regex(pattern=REGEX.开服检查.value)
gold_query = user_matcher_group.on_regex(pattern=REGEX.金价比例.value)
medicine_query = user_matcher_group.on_regex(pattern=REGEX.推荐小药.value)
equip_group_query = user_matcher_group.on_regex(pattern=REGEX.推荐装备.value)
zhenyan_query = user_matcher_group.on_regex(pattern=REGEX.阵眼效果.value)
update_query = user_matcher_group.on_regex(pattern=REGEX.更新公告.value)
price_query = user_matcher_group.on_regex(pattern=REGEX.物品价格.value)
serendipity_query = user_matcher_group.on_regex(pattern=REGEX.奇遇查询.value)
serendipity_list_query = user_matcher_group.on_regex(pattern=REGEX.奇遇统计.value)
serendipity_summary_query = user_matcher_group.on_regex(pattern=REGEX.奇遇汇总.value)
saohua_query = user_matcher_group.on_regex(pattern=REGEX.随机骚话.value)
match_query = user_matcher_group.on_regex(pattern=REGEX.比赛战绩.value)
equip_query = user_matcher_group.on_regex(pattern=REGEX.装备属性.value)
firework_query = user_matcher_group.on_regex(pattern=REGEX.烟花记录.value)
recruit_query = user_matcher_group.on_regex(pattern=REGEX.招募查询.value)
zili_query = user_matcher_group.on_regex(pattern=REGEX.资历榜.value)
shengwang_query = user_matcher_group.on_regex(pattern=REGEX.声望榜.value)
laojianghu_query = user_matcher_group.on_regex(pattern=REGEX.老江湖.value)
bingjia_query = user_matcher_group.on_regex(pattern=REGEX.兵甲榜.value)
mingshi_query = user_matcher_group.on_regex(pattern=REGEX.名师榜.value)
zhanjie_query = user_matcher_group.on_regex(pattern=REGEX.战阶榜.value)
xinhuo_query = user_matcher_group.on_regex(pattern=REGEX.薪火榜.value)
zixing_query = user_matcher_group.on_regex(pattern=REGEX.梓行榜.value)
aixin_query = user_matcher_group.on_regex(pattern=REGEX.爱心榜.value)
shenbing_query = user_matcher_group.on_regex(pattern=REGEX.神兵榜.value)
shilian_query = user_matcher_group.on_regex(pattern=REGEX.试炼榜.value)
help = user_matcher_group.on_regex(pattern=r"^帮助$")


# ----------------------------------------------------------------
#   Dependency，用来获取相关参数及冷却实现
# ----------------------------------------------------------------


def get_server() -> str:
    """
    说明:
        Dependency，获取匹配字符串中的server，如果没有则获取群绑定的默认server
    """

    async def dependency(
            matcher: Matcher, event: GroupMessageEvent, regex_dict: dict = RegexDict()
    ) -> str:

        _server = regex_dict.get("server")
        if _server:
            server = api.app_server(name=_server)
            if not server:
                msg = f"未找到服务器[{_server}]，请验证后查询。"
                await matcher.finish(msg)
        else:
            server = await GroupInfo.get_server(event.group_id)
        return server

    return Depends(dependency)


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


def get_server_with_keyword() -> str:
    """
    说明:
        Dependency，获取server，会判断是不是keyword
    """

    async def dependency(
            matcher: Matcher, event: GroupMessageEvent, regex_dict: dict = RegexDict()
    ) -> str:
        _server = regex_dict.get("server2")
        if _server:
            server = api.app_server(name=_server)
            if not server:
                msg = f"未找到服务器[{_server}]，请验证后查询。"
                await matcher.finish(msg)
            else:
                return server
        else:
            _server = regex_dict.get("server1")
            if _server:
                # 判断server是不是keyword
                server = api.app_server(name=_server)
                if not server:
                    server = await GroupInfo.get_server(event.group_id)
            else:
                # 单招募
                server = await GroupInfo.get_server(event.group_id)
            return server

    return Depends(dependency)


def get_keyword() -> str:
    """
    说明:
        Dependency，招募查询-关键字
    """

    async def dependency(regex_dict: dict = RegexDict()) -> Optional[str]:
        if _keyword := regex_dict.get("keyword"):
            return _keyword
        if _keyword := regex_dict.get("server1"):
            if api.app_server(name=_keyword):
                keyword = None
            else:
                keyword = _keyword
        else:
            keyword = None
        return keyword

    return Depends(dependency)


def get_type() -> str:
    """
    说明:
        Dependency，排行榜-获取类型
    """

    def dependency(regex_dict: dict = RegexDict()) -> str:
        _type = regex_dict.get("type2")
        if not _type:
            _type = regex_dict.get("type1")
        match _type:
            case "声望榜":
                return "名士五十强"
            case "老江湖":
                return "老江湖五十强"
            case "兵甲榜":
                return "兵甲藏家五十强"
            case "名师榜":
                return "名师五十强"
            case "战阶榜":
                return "阵营英雄五十强"
            case "薪火榜":
                return "薪火相传五十强"
            case "梓行榜":
                return "庐园广记一百强"
            case "爱心榜":
                return "爱心帮会五十强"
            case "神兵榜":
                return "神兵宝甲五十强"
            case _:
                return ""

    return Depends(dependency)


def get_tittle() -> str:
    """
    说明:
        Dependency，排行榜-获取标题
    """

    def dependency(regex_dict: dict = RegexDict()) -> str:
        _type = regex_dict.get("type2")
        if not _type:
            _type = regex_dict.get("type1")
        match _type:
            case "声望榜":
                return "声望"
            case "老江湖":
                return "资历"
            case "兵甲榜":
                return "装分"
            case "名师榜":
                return "师徒值"
            case "战阶榜":
                return "战阶分数"
            case "薪火榜":
                return "薪火点"
            case "梓行榜":
                return "梓行点"
            case "爱心榜":
                return "爱心值"
            case "神兵榜":
                return "总装分"
            case _:
                return ""

    return Depends(dependency)


def get_camp() -> str:
    """
    说明:
        Dependency，帮会排名-获取阵营
    """

    async def dependency(matcher: Matcher, name: str = get_value()) -> str:
        match name:
            case "浩气" | "浩气盟":
                return "浩气"
            case "恶人" | "恶人谷":
                return "恶人"
            case _:
                await matcher.finish("请输入正确的阵营名！")

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


# ----------------------------------------------------------------
#   handler列表，具体实现回复内容
# ----------------------------------------------------------------

@daily_query.handle(parameterless=[cold_down(name="日常查询", cd_time=0)])
async def _(event: GroupMessageEvent, server: str = get_server()) -> NoReturn:
    """日常查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 日常查询 | 请求：{server}"
    )
    response = await api.view_active_current(server=server, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await daily_query.finish(msg)

    data = response.data
    url = data.get("url")

    await daily_query.finish(MessageSegment.image(url))


@server_query.handle(parameterless=[cold_down(name="开服查询", cd_time=0)])
async def _(event: GroupMessageEvent, server: str = get_server()) -> NoReturn:
    """开服查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 开服查询 | 请求：{server}"
    )
    response = await api.data_server_check(server=server)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await server_query.finish(msg)

    data = response.data
    status = "已开服" if data["status"] == 1 else "维护中"
    msg = f"{server} 当前状态是[{status}]"
    await server_query.finish(msg)


@gold_query.handle(parameterless=[cold_down(name="金价查询", cd_time=0)])
async def _(event: GroupMessageEvent, server: str = get_server()) -> NoReturn:
    """金价查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 金价查询 | 请求：{server}"
    )
    response = await api.view_trade_demon(server=server, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await gold_query.finish(msg)

    data = response.data
    url = data.get("url")
    await gold_query.finish(MessageSegment.image(url))


@zhenyan_query.handle(parameterless=[cold_down(name="阵眼查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = get_profession()) -> NoReturn:
    """阵眼查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 阵眼查询 | 请求：{name}")
    response = await api.data_school_matrix(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await zhenyan_query.finish(msg)

    data = response.data
    msg = f"{name}：【{data.get('skillName')}】\n"
    descs: list[dict] = data.get("descs")
    for i in descs:
        msg += f"{i.get('name')}：{i.get('desc')}\n"
    await zhenyan_query.finish(msg)


@update_query.handle(parameterless=[cold_down(name="更新公告", cd_time=0)])
async def _(event: GroupMessageEvent) -> NoReturn:
    """更新公告"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 更新公告查询")
    url = "https://jx3.xoyo.com/launcher/update/latest.html"
    img = await browser.get_image_from_url(url=url, width=130, height=480)
    msg = MessageSegment.image(img)
    log = f"群{event.group_id} | 查询更新公告"
    logger.info(log)
    await update_query.finish(msg)


@saohua_query.handle(parameterless=[cold_down(name="骚话", cd_time=0)])
async def _(event: GroupMessageEvent) -> NoReturn:
    """骚话"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 骚话 | 请求骚话")
    response = await api.data_saohua_random()
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await saohua_query.finish(msg)

    data = response.data
    await saohua_query.finish(data["text"])


# -------------------------------------------------------------
#   下面是使用模板生成的图片事件
# -------------------------------------------------------------

@price_query.handle(parameterless=[cold_down(name="物价查询", cd_time=10)])
async def _(event: GroupMessageEvent, name: str = get_value()) -> NoReturn:
    """物价查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 物价查询 | 请求：{name}")
    response = await api.view_trade_record(name=name, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await price_query.finish(msg)

    data = response.data
    url = data.get("url")
    await price_query.finish(MessageSegment.image(url))


@serendipity_query.handle(parameterless=[cold_down(name="角色奇遇", cd_time=10)])
async def _(
        event: GroupMessageEvent,
        server: str = get_server(),
        name: str = get_value(),
) -> NoReturn:
    """角色奇遇查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 角色奇遇查询 | 请求：server:{server},name:{name}"
    )

    ticket = await TicketInfo.get_ticket()
    response = await api.view_luck_adventure(server=server, name=name, ticket=ticket, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await serendipity_query.finish(msg)

    data = response.data
    url = data.get("url")

    await serendipity_query.finish(MessageSegment.image(url))

@serendipity_list_query.handle(parameterless=[cold_down(name="奇遇统计", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = get_server(),
    name: str = get_value(),
) -> NoReturn:
    """奇遇统计查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 奇遇统计查询 | 请求：server:{server},serendipity:{name}"
    )
    response = await api.view_luck_statistical(server=server, name=name, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await serendipity_list_query.finish(msg)

    data = response.data
    url = data.get("url")
    await serendipity_list_query.finish(MessageSegment.image(url))

@serendipity_summary_query.handle(parameterless=[cold_down(name="奇遇汇总", cd_time=10)])
async def _(event: GroupMessageEvent, server: str = get_server()) -> NoReturn:
    """奇遇汇总查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 奇遇汇总查询 | 请求：{server}"
    )
    response = await api.view_luck_collect(server=server, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await serendipity_summary_query.finish(msg)

    data = response.data
    url = data.get("url")
    await serendipity_summary_query.finish(MessageSegment.image(url))

@match_query.handle(parameterless=[cold_down(name="战绩查询", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = get_server(),
    name: str = get_value(),
) -> NoReturn:
    """战绩查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 战绩查询 | 请求：server:{server},name:{name}"
    )
    ticket = await TicketInfo.get_ticket()
    response = await api.view_match_recent(server=server, name=name, ticket=ticket, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await match_query.finish(msg)

    data = response.data
    url = data.get("url")
    await match_query.finish(MessageSegment.image(url))

@equip_query.handle(parameterless=[cold_down(name="装备属性", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = get_server(),
    name: str = get_value(),
) -> NoReturn:
    """装备属性查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 装备属性查询 | 请求：server:{server},name:{name}"
    )
    ticket = await TicketInfo.get_ticket()
    response = await api.view_role_attribute(server=server, name=name, ticket=ticket, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await equip_query.finish(msg)

    data = response.data
    url =  data.get("url")
    await equip_query.finish(MessageSegment.image(url))

@recruit_query.handle(parameterless=[cold_down(name="招募查询", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = get_server_with_keyword(),
    keyword: Optional[str] = get_keyword(),
) -> NoReturn:
    """招募查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 招募查询 | 请求：server:{server},keyword:{keyword}"
    )
    response = await api.view_member_recruit(server=server, robot=BOT)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await recruit_query.finish(msg)

    data = response.data
    url =  data.get("url")
    await recruit_query.finish(MessageSegment.image(url))

@zili_query.handle(parameterless=[cold_down(name="资历排行", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = get_server_with_keyword(),
    kungfu: Optional[str] = get_keyword(),
) -> NoReturn:
    """资历榜"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 资历排行 | 请求：server:{server},kunfu:{kungfu}"
    )
    ticket = await TicketInfo.get_ticket()
    if not kungfu:
        kungfu = "ALL"
    response = await api.view_school_excellent(
        server=server, school=kungfu, ticket=ticket, robot=BOT
    )
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await zili_query.finish(msg)

    data = response.data
    url = data.get("url")
    await zili_query.finish(MessageSegment.image(url))