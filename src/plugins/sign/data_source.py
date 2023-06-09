import random
from datetime import date

from httpx import AsyncClient
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent

from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo
from src.utils.browser import browser
from src.utils.log import logger

from .config import FRIENDLY_ADD, GOLD_BASE, LUCKY_GOLD, LUCKY_MAX, LUCKY_MIN

client = AsyncClient()
"""异步请求客户端"""

async def get_nickname(
    event: GroupMessageEvent
):
    if event.sender.card:
        nickname = event.sender.card
    else:
        nickname = event.sender.nickname
    return nickname



async def get_sign_in(event: GroupMessageEvent, user_id: int, group_id: int) -> Message:
    """
    :说明
        用户签到

    :参数
        * user_id：用户QQ
        * group_id：QQ群号

    :返回
        * Message：机器人返回消息
    """
    msg = MessageSegment.at(user_id)
    # 获取上次签到日期
    last_sign = await UserInfo.get_last_sign(user_id, group_id)
    # 判断是否已签到
    today = date.today()
    if today == last_sign:
        logger.debug(f"<y>群{group_id}</y> | <g>{user_id}</g> | 签到失败")
        msg += MessageSegment.text("\n你今天已经签到了，不要贪心噢。")
        return msg

    nickname = await get_nickname(event)





    # 头像
    qq_head = await _get_qq_img(user_id)
    msg_head = MessageSegment.image(qq_head)

    # 签到名次
    sign_num = await GroupInfo.group_sign_in(group_id)

    # 设置签到
    data = await UserInfo.sign_in(
        user_id=user_id,
        group_id=group_id,
        lucky_min=LUCKY_MIN,
        lucky_max=LUCKY_MAX,
        friendly_add=FRIENDLY_ADD,
        gold_base=GOLD_BASE,
        lucky_gold=LUCKY_GOLD,
    )


    pagename = "签到.html"
    today_lucky = data.get("today_lucky")
    today_gold = data.get("today_gold")
    all_gold = data.get("all_gold")
    all_friendly = data.get("all_friendly")
    sign_times = data.get("sign_times")

    img = await browser.template_to_image(
        pagename=pagename,
        sign_num=sign_num,
        today_lucky=today_lucky,
        today_gold=today_gold,
        all_gold=all_gold,
        all_friendly=all_friendly,
        sign_times=sign_times,
        nickname=nickname,
        id=user_id,
    )
    msg = MessageSegment.image(img)

    logger.debug(f"<y>群{group_id}</y> | <g>{user_id}</g> | 签到成功")
    return msg


async def _get_qq_img(user_id: int) -> bytes:
    """
    :说明
        获取QQ头像

    :参数
        * user_id：用户QQ

    :返回
        * bytes：头像数据
    """
    num = random.randrange(1, 4)
    url = f"http://q{num}.qlogo.cn/g"
    params = {"b": "qq", "nk": user_id, "s": 100}
    resp = await client.get(url, params=params)
    return resp.content
