import time
from typing import Optional

from httpx import AsyncClient
from pydantic import BaseModel, Extra, Field

from src.config import config as baseconfig
from src.utils.log import logger


class Config(BaseModel, extra=Extra.ignore):
    """沙盘配置"""

    account: str = Field("", alias="j3sp_account")
    """j3sp账号"""
    password: str = Field("", alias="j3sp_password")
    """j3sp密码"""


class Response(BaseModel):
    """响应数据"""

    code: int
    """响应代码"""
    msg: str
    """消息"""
    time: str
    """时间戳"""
    data: dict
    """数据"""


class UserData(BaseModel):
    """userinfo数据模型"""

    id: int
    username: str
    nickname: str
    mobile: str
    avatar: str
    score: int
    token: str
    user_id: int
    createtime: int
    expiretime: int
    expires_in: int


class UserInfo(BaseModel):

    userinfo: UserData


class LoginResponse(Response):
    """登录响应数据"""

    data: Optional[UserInfo]


class RefreshData(BaseModel):

    token: str
    expires_in: int


class RefreshResponse(Response):
    """刷新接口响应模型"""

    data: Optional[RefreshData]


class SandData(BaseModel):
    """沙盘接口响应"""

    regionName: str
    """大区名"""
    serverName: str
    """服务器名"""
    status: str
    """更新状态"""
    userName: str
    """更新用户"""
    createTime: str
    """创建时间"""
    sandImage: str
    """地图url"""
    sentenceyelp: Optional[str] = None


class SandInfo(BaseModel):

    sand_data: SandData
    """沙盘数据"""


class SandResponse(Response):
    """沙盘接口响应"""

    data: Optional[SandInfo]
    """返回数据"""


class SandManager:
    """沙盘类"""

    client: AsyncClient
    """客户端"""
    config: Config
    """配置"""
    token: str = ""
    """访问token"""
    expired_time: int = 0
    """过期时间"""

    def __init__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        self.client = AsyncClient(headers=headers)
        self.config = Config.parse_obj(baseconfig)

    @property
    def is_expired(self) -> bool:
        """token是否过期"""
        return self.expired_time - int(time.time()) < 300

    async def login(self) -> bool:
        """登录"""
        url = "https://www.j3sp.com/api/user/login"
        params = {"account": self.config.account, "password": self.config.password}
        try:
            res = await self.client.get(url=url, params=params)
            response = LoginResponse.parse_obj(res.json())
            if response.code == 1:
                # 登录成功
                self.token = response.data.userinfo.token
                self.expired_time = response.data.userinfo.expiretime
                return True
            else:
                logger.debug(f"剑三沙盘 | 登录出错 | {response.msg}")
                return False
        except Exception as e:
            logger.error(f"剑三沙盘 | 登录出错 | {str(e)}")
            return False

    async def refresh_token(self) -> bool:
        """刷新token"""
        url = "https://www.j3sp.com/api/token/refresh"
        try:
            res = await self.client.get(url=url)
            response = RefreshResponse.parse_obj(res.json())
            if response.code == 1:
                self.token = response.data.token
                self.expired_time = int(response.time) + response.data.expires_in
                return True
            else:
                logger.debug(f"剑三沙盘 | 刷新出错 | {response.msg}")
                return False
        except Exception as e:
            logger.error(f"剑三沙盘 | 登录出错 | {str(e)}")
            return False

    async def get_sand_pic(self, server: str) -> SandResponse:
        """获取沙盘图片"""
        # 登录
        if not self.token:
            if not await self.login():
                return SandResponse(code=0, msg="沙盘查询出错：请检查配置项是否正确！", time=0)

        # token是否过期
        if self.is_expired:
            if not await self.refresh_token():
                self.token = ""
                return SandResponse(code=0, msg="沙盘查询出错：token过期，重新查询试试！", time=0)

        url = "https://www.j3sp.com/api/sand/"
        params = {"serverName": server, "is_history": 0, "shadow": 1}
        try:
            res = await self.client.get(url=url, params=params)
            return SandResponse.parse_obj(res.json())
        except Exception as e:
            logger.error(f"剑三沙盘 | 查询沙盘出错 | {str(e)}")
            return SandResponse(code=0, msg=f"沙盘查询出错：{str(e)}", time=0)


sand_manager = SandManager()
"""沙盘管理器实例"""
