import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from src.internal.database import database_init
from src.utils.scheduler import start_scheduler


nonebot.init()

app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 开启数据库
driver.on_startup(database_init)
# 开启定时器
driver.on_startup(start_scheduler)

nonebot.load_builtin_plugins('echo')

# 加载其他插件
nonebot.load_from_toml("pyproject.toml", encoding="utf-8")
nonebot.load_plugins("src/managers")

#nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()