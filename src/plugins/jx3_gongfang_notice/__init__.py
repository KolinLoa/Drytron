from src.utils.log import logger
from nonebot import get_bots
from nonebot_plugin_apscheduler import scheduler
from src.params import PluginConfig
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="攻防排队通知",
    description="提醒大小攻防排队",
    usage="自动发送通知",
    config=PluginConfig(),
)


@scheduler.scheduled_job("cron", hour="12", minute="20", day_of_week="sat,sun", id="weekly_all")
async def weekly_all():
    logger.info(f"<y>攻防通知!</y>")
    bot = list(get_bots().values())[0]
    # 获取第一个机器人对象
    groups = await bot.get_group_list()
    # 获取机器人加入的所有群
    for group in groups:
        group_id = group["group_id"]
        # 获取群号
        await bot.send_group_msg(group_id=group_id,
                                 message="阵营大攻防将于12:30开始排队，请大家准备好前往主城战场处按时排队，神行请提前十秒起飞！")


@scheduler.scheduled_job("cron", hour="18", minute="20", day_of_week="sat,sun", id="weekly_all")
async def weekly_all():
    logger.info(f"<y>攻防通知!</y>")
    bot = list(get_bots().values())[0]
    # 获取第一个机器人对象
    groups = await bot.get_group_list()
    # 获取机器人加入的所有群
    for group in groups:
        group_id = group["group_id"]
        # 获取群号
        await bot.send_group_msg(group_id=group_id,
                                 message="阵营大攻防将于18:30开始排队，请大家准备好前往主城战场处按时排队，神行请提前十秒起飞！")


@scheduler.scheduled_job("cron", hour="19", minute="20", day_of_week="tue,thu", id="weekly_all")
async def weekly_all():
    logger.info(f"<y>攻防通知!</y>")
    bot = list(get_bots().values())[0]
    # 获取第一个机器人对象
    groups = await bot.get_group_list()
    # 获取机器人加入的所有群
    for group in groups:
        group_id = group["group_id"]
        # 获取群号
        await bot.send_group_msg(group_id=group_id,
                                 message="阵营小攻防将于19:30开始排队，请大家准备好神行或者前往过图点，神行请提前十秒起飞！")


@scheduler.scheduled_job("cron", hour="19", minute="50", day_of_week="wed,fri", id="weekly_all")
async def weekly_all():
    logger.info(f"<y>世界BOSS通知!</y>")
    bot = list(get_bots().values())[0]
    # 获取第一个机器人对象
    groups = await bot.get_group_list()
    # 获取机器人加入的所有群
    for group in groups:
        group_id = group["group_id"]
        # 获取群号
        await bot.send_group_msg(group_id=group_id, message="世界BOSS将于20:00出现在跨服烂柯山，大家请做好排队准备！")


@scheduler.scheduled_job("cron", hour="7", minute="30", id="weekly_all")
async def weekly_all():
    logger.info(f"<y>起床通知!</y>")
    bot = list(get_bots().values())[0]
    # 获取第一个机器人对象
    groups = await bot.get_group_list()
    # 获取机器人加入的所有群
    for group in groups:
        group_id = group["group_id"]
        # 获取群号
        await bot.send_group_msg(group_id=group_id,
                                 message="起床啦，起床啦，别做少爷公主了，起来打工打游戏啦！！！")
