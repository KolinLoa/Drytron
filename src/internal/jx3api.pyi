from typing import Optional

from httpx import AsyncClient
from pydantic import BaseModel

from src.config import Jx3ApiConfig

class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: dict | list[dict]
    """返回数据"""
    time: int
    """时间戳"""

class JX3API:
    """jx3api接口类"""

    client: AsyncClient
    """浏览器客户端"""
    config: Jx3ApiConfig
    """api设置"""

    # ------------------------------------------------------------
    #                      Free  API
    # ------------------------------------------------------------
    async def view_active_current(self, *, server: str, num: int = ..., robot: str) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `num`: 可选，查询天数，默认为0
        """
        ...
    async def view_active_calculate(self, *, num: int = ...) -> Response:
        """
        说明:
            搜索当天前后指定日期的日常信息

        参数:
            * `num`：可选，计算天数，搜索当天前后指定日期的日常信息
        """
        ...
    async def view_trade_demon(self, *, server: str, limit: int = ..., robot: str) -> Response:
        """
        说明：
            当前时间的金币比例

        参数:
            * `server`：服务器名
            * `limit`： 单页数量，设置单页返回的数量；默认值 : 10。
        """
        ...
    async def data_server_check(self, *, server: str) -> Response:
        """
        说明：
            服务器当前的状态 [ 已开服/维护中 ]

        参数：
            * `server`：服务器名
        """
        ...
    async def data_server_status(self, *, server: str) -> Response:
        """
        说明:
            服务器当前的状态 [ 维护/正常/繁忙/爆满 ]

        参数:
            * `server`：服务器名
        """
        ...
    async def data_server_search(self, *, name: str) -> Response:
        """
        说明:
            简称搜索主次服务器

        参数:
            * `name`：区服别名，查询指定别名的区服信息。
        """
        ...
    async def data_exam_answer(self, *, question: str, limit: int = ...) -> Response:
        """
        说明:
            搜索科举试题的答案

        参数:
            * `question`：科举题目，搜索目标题目答案
            * `limit`：单页数量，设置单页返回的数量；默认值 : 10。
        """
        ...
    async def data_web_news(self, *, limit: int = ...) -> Response:
        """
        说明:
            搜索官方近期发布的最新公告，新闻等相关内容。

        参数:
            * `limit`：单页数量，设置单页返回的数量；默认值 : 10。
        """
        ...
    async def data_web_announce(self, *, limit: int = ...) -> Response:
        """
        说明:
            搜索官方近期发布的维护公告。

        参数:
            * `limit`：单页数量，设置单页返回的数量；默认值 : 10。
        """
        ...

    async def data_home_flower(
        self, *, server: str, map: str = ..., flower: str = ...
    ) -> Response:
        """
        说明:
            检查当天鲜花最高价格收购线路。

        参数:
            * `server`：服务器名
            * `map`：可选，用于筛选地图
            * `flower`：可选， 用于筛选鲜花
        """
        ...
    async def data_home_travel(self, *, name: str) -> Response:
        """
        说明:
            器物谱地图产出装饰

        参数:
            * `name`：地图名称，查询指定地图的产出装饰
        """
        ...
    async def data_school_equip(self, *, name: str) -> Response:
        """
        说明:
            推荐的角色配装(萌新系列)

        参数:
            * `name`：心法名称
        """
        ...
    async def data_school_matrix(self, *, name: str) -> Response:
        """
        说明:
            职业阵眼效果

        参数:
            * `name`：心法名称
        """
        ...

    async def data_chat_random(self) -> Response:
        """
        说明:
            召唤一条骚话。
        """
        ...

    def app_server(self, *, name: str) -> Optional[str]:
        """
        说明:
            主从大区

        参数:
            * `name`：大区名称

        返回:
            * `str`：主区名称
        """
        ...
    # -------------------------------------------------------------------
    #                            VIP API
    # -------------------------------------------------------------------
    async def data_token_ticket(self, *, ticket: str) -> Response:
        """
        说明:
            推栏 token 是否有效

        参数:
            * `ticket`：推栏标识，检查指定标识是否有效；
        """
        ...

    async def data_server_sand(self, *, server: str,) -> Response:
        """
        说明：
            沙盘数据
        参数：
        * 'server':服务器名称
        """
        ...

    async def data_movie_editor(self, *, name: str) -> Response:
        """
        说明:
            动画编辑器物品编号

        参数:
            * `name`：物品名称，查询指定名称的物品编号信息。
        """
        ...
    async def view_luck_require(self, *, name: str, robot: str) -> Response:
        """
        说明:
            触发奇遇的前置条件

        参数:
            * `name`：奇遇名称
        """
        ...
    async def view_luck_adventure(
        self, *, server: str, name: str, ticket: str, robot: str
    ) -> Response:
        """
        说明:
            角色奇遇触发记录(不保证遗漏)

        参数:
            * `server`：区服名称，筛选记录
            * `name`：角色名称，查询指定角色的触发记录
            * `ticket`：推栏标识，检查数据完整性
        """
        ...
    async def view_luck_statistical(
        self, *, server: str, name: str, limit: int = ..., robot: str
    ) -> Response:
        """
        说明:
            统计奇遇近期触发角色记录

        参数:
            * `server`：区服名称，筛选记录
            * `name`：奇遇名称，统计指定奇遇触发记录
            * `limit`：单页数量，设置单页返回的数量；默认值 : 20
        """
        ...
    async def view_luck_collect(self, *, server: str, days: int = ..., robot: str) -> Response:
        """
        说明:
            统计奇遇近期触发角色记录

        参数:
            * `server`：区服名称，筛选记录
            * `days`：汇总时间，汇总指定天数内的奇遇记录；默认值 : 7
        """
        ...
    async def view_luck_server_adventure(self, *, name: str, robot: str) -> Response:
        """
        说明:
            统计全服奇遇记录

        参数:
            * `name`：奇遇名称，查询指定奇遇的全服记录
        """
        ...
    async def view_luck_server_statistical(
        self, *, name: str, limit: int = ..., robot: str
    ) -> Response:
        """
        说明:
            统计全服近期奇遇记录

        参数:
            * `name`：奇遇名称，查询指定奇遇的全服记录
            * `limit`：单页数量，设置单页返回的数量；默认值 : 20
        """
        ...

    async def view_match_recent(
        self, *, server: str, name: str, ticket: str, mode: int = ..., robot: str
    ) -> Response:
        """
        说明:
            角色近期战绩记录

        参数:
            * `server`：区服名称，筛选记录
            * `name`：角色名称，查询指定角色的战绩记录
            * `ticket`：推栏标识，检查请求权限
            * `mode`：可选，比赛模式，可选值22/33/55，未输入或输入0 时返回全部模式记录。
        """
        ...
    async def view_match_awesome(
        self, *, ticket: str, mode: int = ..., limit: int = ..., robot: str
    ) -> Response:
        """
        说明:
            名剑排行

        参数:
            * `ticket`：推栏标识，检查请求权限
            * `mode`：可选，比赛模式，可选值22/33/55，默认值33
            * `limit`：单页数量，设置单页返回的数量；默认值 : 20
        """
        ...
    async def view_match_schools(self, *, ticket: str, mode: int = ..., robot: str) -> Response:
        """
        说明:
            名剑统计

        参数:
            * `ticket`：推栏app的ticket
            * `mode`：比赛模式，可选值22/33/55，默认值33。
        """
        ...
    async def view_member_recruit(self, *, server: str, robot: str) -> Response:
        """
        说明：
            团队招募
        server: 服务器
        """
        ...
    async def data_movie_editor(self, *, name: str) -> Response:
        """
        说明
            动画编辑器物品编号
            name：物品名称
        """
        ...
    async def view_role_roleInfo(self, *, server: str, name: str, robot: str) -> Response:
        """
        说明:
            角色详细信息

        参数:
            * `server`：服务器名
            * `name`：角色名
        """
        ...
    async def data_save_roleInfo(
        self, *, server: str, roleId: str, ticket: str
    ) -> Response:
        """
        说明:
            自动更新角色信息

        参数:
            * `server`：区服名称，查询指定区服的角色信息
            * `roleId`：角色数字账号，查询指定数字账号的角色信息
            * `ticket`：推栏标识，检查请求权限
        """
        ...
    async def data_role_teamCdList(
        self, *, server: str, name: str, ticket: str
    ) -> Response:
        """
        说明:
            角色副本通关记录

        参数:
            * `server`：区服名称，筛选记录
            * `name`：角色名称，查询指定角色的副本通关记录
            * `ticket`：推栏标识，检查请求权限
        """
        ...
    async def data_role_achievement(
        self, *, server: str, role: str, name: str, ticket: str
    ) -> Response:
        """
        说明:
            角色成就进度

        参数:
            * `server`：区服名称，筛选记录
            * `role`：角色名称，查询指定角色的副本通关记录
            * `name`：成就/系列名称，查询指定成就/系列的完成进度
            * `ticket`：推栏标识，检查请求权限
        """
        ...
    async def view_role_attribute(
        self, *, server: str, name: str, ticket: str, robot: str
    ) -> Response:
        """
        说明:
            角色装备属性详情

        参数:
            * `server`：区服名称，筛选记录
            * `name`：角色名称，查询指定角色的装备属性
            * `ticket`：推栏标识，检查请求权限
        """
        ...
    async def view_school_excellent(
        self, *, ticket: str, school: str = ..., server: str = ..., robot:str
    ) -> Response:
        """
        说明:
            游戏资历榜单

        参数:
            * `ticket`：推栏标识，检查请求权限
            * `school`：门派简称，查询指定门派的资历榜单，默认值 : ALL
            * `server`：区服名称，筛选记录，默认值 : ALL
        """
        ...
    async def data_rank_excellent(self, *, table: str, name: str, server: str = ...) -> Response:
        """
        说明:
            客户端战功榜与风云录

        参数:
            [√] 必选的 [table] [name] 榜单类型与榜单名称，[table] 与 [name] 的关联：
            [table] : 个人，[name] : [名士五十强 老江湖五十强 兵甲藏家五十强 名师五十强 阵营英雄五十强 薪火相传五十强 庐园广记一百强]；
            [table] : 帮会，[name] : [浩气神兵宝甲五十强 恶人神兵宝甲五十强 浩气爱心帮会五十强 恶人爱心帮会五十强]；
            [table] : 阵营，[name] : [赛季恶人五十强 赛季浩气五十强 上周恶人五十强 上周浩气五十强 本周恶人五十强 本周浩气五十强]；
            [table] : 试炼，[name] : [万花 七秀 少林 纯阳 天策 五毒 唐门 明教 苍云 长歌 藏剑 丐帮 霸刀 蓬莱 凌雪 衍天 药宗 刀宗]；
            [√] 必选的 [server] 区服名称，筛选记录；
            [√] 必选的 [token] 站点标识，检查请求权限。
        """
        ...
    async def data_server_event(self, *, name: str, limit: int = ...) -> Response:
        """
        说明
            全服阵营大事件
        :param name:阵营名称，筛选记录；
        :param limit:设置单页数量，默认 : 100；
        :return:
        """
        ...
    async def view_trade_record(self, *, name: str, robot: str) -> Response:
        """
        说明
            黑市物品价格
        :param name: 查找的物品
        :return:
        """
        ...
    async  def data_chat_mixed(self, *, name: str, session: str, text: str) -> Response:
        """
        说明：
            混合聊天
        :param name: 机器人名字
        :param session: 会话标识，当调用小爱助手时偶尔会出现上线文联想。
        :param text:提问的内容
        :return:
        """
    # ------------------------------------------------------------
    #                      VRF  API
    # ------------------------------------------------------------
    async def data_music_tencent(self, *, name: str) -> Response:
        """
        说明:
            搜索腾讯音乐歌曲编号。

        参数:
            * `name`：歌曲名称，搜索指定歌曲的音乐编号
        """
        ...
    async def data_music_netease(self, *, name: str) -> Response:
        """
        说明:
            搜索网易云音乐歌曲编号。

        参数:
            * `name`：歌曲名称，搜索指定歌曲的音乐编号
        """
        ...
    async def data_chat_tencent(
        self, *, secretId: str, secretKey: str, name: str, question: str
    ) -> Response:
        """
        说明:
            腾讯云智障聊天

        参数:
            * `secretId`：腾讯云secretId
            * `secretKey`：腾讯云secretKey
            * `name`：机器人名称
            * `question`：对话内容
        """
        ...
    async def data_voice_alitts(
        self,
        *,
        appkey: str,
        access: str,
        secret: str,
        voice: str,
        format: str,
        sample_rate: int,
        volume: int,
        speech_rate: int,
        pitch_rate: int,
        text: str
    ) -> Response:
        """
        说明:
            阿里云语音合成（TTS）

        参数:
            * `appkey`：阿里云appkey
            * `access`：阿里云access
            * `secret`：阿里云secret
            * `voice`：发音人，默认Aitong
            * `format`：编码格式，支持 PCM WAV MP3，默认：MP3
            * `sample_rate`：采样率，默认：16000
            * `volume`：音量，取值范围：0～100，默认：50
            * `speech_rate`：语速，取值范围：-500～500，默认：0
            * `pitch_rate`： 音调，取值范围：-500～500，默认：0
        """
        ...
    async def data_saohua_content(self) -> Response:
        """
        说明:
            召唤一条舔狗日记。
        """
        ...

    async def data_saohua_random(self) -> Response:
        """
        说明
            召唤骚话
        :return:
        """
        ...
    async def data_idiom_solitaire(self, *, name: str) -> Response:
        """
        说明:
            搜索下一个成语，已清除收尾同音的成语。

        参数:
            * `name`：输入四字成语，已去除收尾同音成语。
        """
        ...
