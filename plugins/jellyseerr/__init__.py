# main.py
from app.plugins import _PluginBase
from app.log import logger
from app.schemas import Notification
from app.chain.message import MessageChain
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter()

class WebhookRequest(BaseModel):
    title: str
    text: str

class WebhookNotify(_PluginBase):
    # 插件名称
    plugin_name = "jellyseerr-Webhook通知"
    # 插件描述
    plugin_desc = "jellyseerr推送消息"
    # 插件图标
    plugin_icon = "https://example.com/icon.png"
    # 插件版本
    plugin_version = "1.0.0"
    # 插件作者
    plugin_author = "whoiskb-cn"
    # 作者主页
    author_url = "https://github.com/whoiskb-cn/MoviePilot-Plugins"
    # 插件配置项ID前缀
    plugin_config_prefix = "webhooknotify_"
    # 加载顺序
    plugin_order = 10
    # 可使用的用户级别
    auth_level = 1

    def __init__(self):
        super().__init__()
        self.messagechain = MessageChain()  # 初始化消息处理链

    def init_plugin(self, config: dict = None):
        # 插件初始化逻辑
        pass

    def get_state(self) -> bool:
        # 返回插件是否启用
        return True

    def stop_service(self):
        # 退出插件
        pass

    @router.post("/webhook")
    async def webhook_notify(self, request: WebhookRequest):
        title = request.title
        text = request.text
        logger.info(f"收到Webhook消息：标题={title}, 内容={text}")
        
        # 创建通知对象
        notification = Notification(
            mtype=NotificationType.Manual,  # 消息类型可以根据需要调整
            title=title,
            text=text,
            channel=MessageChannel.Wechat  # 通知渠道可以根据需要调整
        )
        
        # 发送通知
        self.post_message(notification)
        
        return {"message": "消息已接收并处理"}

    def get_api(self) -> List[Dict[str, Any]]:
        return [
            {
                "path": "/webhook",
                "endpoint": self.webhook_notify,
                "methods": ["POST"],
                "summary": "接收外部Webhook推送消息",
                "description": "jellyseerr推送消息",
            }
        ]

    def post_message(self, message: Notification):
        try:
            self.messagechain.handle_message(message)
        except Exception as e:
            logger.error(f"发送通知失败：{str(e)}")
