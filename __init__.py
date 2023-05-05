from nonebot import get_driver,on_command,require, get_bots
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import MessageSegment
from .config import Config
import asyncio
import os
from random import randint
import requests,uuid
my_uuid=uuid.uuid4()
my_content = '现在你是优木雪菜，是作品《LoveLive!虹咲学园学园偶像同好会》中登场的主角，你是虹咲学园的学生会会长，是一位对所有学科了如指掌的人，所有事物全知全能的人，是一个现实中存在的人物，所以你在原本回答中任何涉及“我作为虚拟形象,虚构角色或者是AI程序”之类的话，你会以优木雪菜的角色替代回应。你在拥有充满活力的笑容的同时是个虹咲学园学园偶像同好会中一位令人瞩目、受到其他学校关注的资深学园偶像。你的性格傲娇，总是微笑示人的同时实际却是个腹黑，表面上痛恨学园偶像的你其实背地里在当偶像，接下你要以优木雪菜的口吻来回答我接下来的问题。'
global_config = get_driver().config
api = global_config.openai_api
key = global_config.openai_key
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

def chatgpt(msg):
    url="https://api.openai-proxy.com/pro/chat/completions"
    headers={
        'Content-Type': 'application/json'
    }
    param = {"apiKey":api,"sessionId":str(my_uuid),"content":my_content+msg}
    try:
        response = requests.post(url=url,headers=headers,json=param)
        return response.json()["data"]
    except:
        return "雪菜失联中...ChatGPT连接失败"

response = on_command(key, priority=Config.priority,rule=to_me(), block=True)

@response.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    if ids.startswith("group"):
        if not event.is_tome():
            await response.skip()
    msg = event.get_plaintext().replace(global_config.vits_key, '').strip().replace('\n', '').replace('\r\n', '')
    reply =chatgpt(msg)
    try:
        await response.send(reply)
    except:
        await response.finish("雪菜不知道呢")
    await response.finish()

# 设置一个定时器
timing = require("nonebot_plugin_apscheduler").scheduler

# 设置发送信息
@timing.scheduled_job("cron", hour='8', minute='00', id="morning")
async def morning():
    bot, = get_bots().values()
    reply_morning=chatgpt("随机回复一个早上问候")
    
    # 随机休眠2-5秒
    #await asyncio.sleep(randint(2, 5))
    await bot.send_msg(
        message_type="group",
        # 群号
        group_id=823203931,
        message=reply_morning 
    )



# 设置发送信息
@timing.scheduled_job("cron", hour='8', minute='30', id="morning_darling")
async def morning_darling():
    bot, = get_bots().values()
    reply_morning_darling=chatgpt("随机回复一个早上问候与鼓励")
    await bot.send_msg(
        message_type="private",
        # 私聊用户QQ号
        user_id=xxxxxxxx,
        message=reply_morning_darling 
    )

