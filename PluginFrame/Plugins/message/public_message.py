import requests
from loguru import logger

from PluginFrame.PluginManager import ModelComponent
from PluginFrame.plugins_conf import registration_directive
from config import Config
from cqhttp import SendMsgModel
from cqhttp.api import CQApiConfig
from cqhttp.cq_code import CqReply
from cqhttp.request_model import SendPrivateMsgRequest, SendGroupMsgRequest, DeleteMsgRequest
from globe import connections, HOST_REGX
from sk import manager
from utils.text_to_img import to_image


@registration_directive(matching=r'^#(美女|放松心情|轻松一刻)', message_types=("private", "group"))
class DouYinBellePlugin(ModelComponent):
    __name__ = 'DouYinBellePlugin'
    __desc__ = '都因'

    async def start(self, message_parameter):

        message_info = message_parameter.get("message_info")
        sender = message_info.get("sender")
        # 调用GPT-3聊天机器人

        resp = f"[CQ:video,file={self.get_girl_url()}]"
        if message_info.get("message_type") == "group":
            logger.info(
                f"收到群组({message_info.get('group_id')})消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )
            await SendGroupMsgRequest(group_id=message_info.get("group_id"), message=resp).send_request(
                CQApiConfig.message.send_group_msg.Api
            )
        elif message_info.get("message_type") == "private":
            logger.info(
                f"收到私人消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )
            await SendPrivateMsgRequest(user_id=sender.get("user_id"), message=resp).send_request(
                CQApiConfig.message.send_private_msg.Api
            )


    def get_girl_url(self):

        resp = requests.get("http://xin-hao.top/sqlWork/randomDouyin")
        try:
            url = resp.history[1].url
        except:
            url = "http://xin-hao.top/sqlWork/randomDouyin"
        logger.info("取到的url为：{}".format(url))
        return url


@registration_directive(matching=r'^#(ping|Ping) '+HOST_REGX, message_types=("private", "group"))
class PingHostPlugin(ModelComponent):
    __name__ = 'PingHostPlugin'

    async def start(self, message_parameter):
        message_info = message_parameter.get("message_info")
        sender = message_info.get("sender")
        re_obj = message_parameter.get("re_obj")
        host = re_obj.group(2) + re_obj.group(3)
        if message_info.get("message_type") == "group":
            logger.info(
                f"收到群组({message_info.get('group_id')})消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )
            if Config.cqhttp.cqType == "http":
                wait = f"""{CqReply(message_info.get("message_id")).cq} 正在查询中，请稍后..."""
                wait_message = await self.send_group_msg(message_info.get("group_id"), wait)
                wait_message = wait_message.get("data")
                status, data = self.get_girl_url(host)
                await DeleteMsgRequest(message_id=wait_message.get("message_id")).send_request(
                    CQApiConfig.message.delete_msg.Api
                )
            else:
                status, data = self.get_girl_url(host)
            data = f"{CqReply(message_info.get('message_id')).cq} {await to_image(data)}"
            await self.send_group_msg(message_info.get("group_id"), data)

        elif message_info.get("message_type") == "private":
            logger.info(
                f"收到私人消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )
            if Config.cqhttp.cqType == "http":
                wait = f"""{CqReply(message_info.get("message_id")).cq} 正在查询中，请稍后..."""
                wait_message = await self.send_private_msg(message_info.get("group_id"), wait)
                wait_message = wait_message.get("data")
                status, data = self.get_girl_url(host)
                await DeleteMsgRequest(message_id=wait_message.get("message_id")).send_request(
                    CQApiConfig.message.delete_msg.Api
                )
            else:
                status, data = self.get_girl_url(host)
            data = f"{CqReply(message_info.get('message_id')).cq} {await to_image(data)}"
            await self.send_private_msg(message_info.get("group_id"), data)
        return ''

    @staticmethod
    def get_girl_url(url):
        resp = requests.get(f"https://v.api.aa1.cn/api/api-ping/ping.php?url={url}").json()
        try:
            data = f"""
            Ping {url} 的结果为：
                域名：{resp.get("host")}
                 IP：{resp.get("ip")}
                最小延迟：{resp.get("ping_time_min")}
                最大延迟：{resp.get("ping_time_max")}
                服务器运营部：{resp.get("location")}
                服务器归属地：{resp.get("node")}
            """
            status = 0
        except:
            data = "查询失败，接口可能出现问题！！！"
            status = 1
        return status, data

    @staticmethod
    async def send_group_msg(group_id, message):
        return await SendGroupMsgRequest(group_id=group_id, message=message).send_request(
            CQApiConfig.message.send_group_msg.Api
        )

    @staticmethod
    async def send_private_msg(user_id, message):
        return await SendPrivateMsgRequest(user_id=user_id, message=message).send_request(
            CQApiConfig.message.send_private_msg.Api
        )
