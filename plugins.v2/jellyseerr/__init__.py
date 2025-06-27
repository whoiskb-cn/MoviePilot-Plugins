from app.plugins import _PluginBase
from .handler import register_event
from typing import List, Dict, Any, Tuple, Optional
from app.helper.notification import NotificationHelper
from app.schemas import ServiceInfo
from app.events import EventType, eventmanager, Event

class Jellyseerr(_PluginBase):
    plugin_name = "Jellyseerr通知推送"
    plugin_desc = "监听Jellyseerr Webhook并通过MoviePilot通知推送"
    plugin_icon = "Wechat.png"
    plugin_version = "1.0"
    plugin_author = "whoiskb-cn"
    plugin_config_prefix = "jellyseerr"
    plugin_order = 99
    auth_level = 1

    def init_plugin(self, config: dict = None):
        self.config = config or {}
        self.notify_name: str = self.config.get("notify_name", "wechat_notify")
        self.notification_helper = NotificationHelper()
        self.notify_service: Optional[ServiceInfo] = self.notification_helper.get_service(name=self.notify_name)
        register_event(config)  # 你可以改成传递 self 方便调用 send_notify

    def get_state(self) -> bool:
        return True

    def stop_service(self):
        pass  # 无需关闭资源

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {'cols': 12},
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'notify_name',
                                            'label': '通知服务名称',
                                            'placeholder': '如 wechat_notify',
                                            'clearable': True,
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VAlert',
                        'props': {
                            'type': 'info',
                            'text': '确保Jellyseerr的Webhook地址指向MoviePilot的 /webhook/jelly 路径。',
                            'variant': 'tonal'
                        }
                    }
                ]
            }
        ], {
            "notify_name": "wechat_notify"
        }

    def send_notify(self, title: str, text: str) -> bool:
        """
        通过选定的通知服务发送消息
        """
        if not self.notify_service or not self.notify_service.instance:
            return False
        try:
            # 具体发送接口可能是 send/send_text/send_message，根据实际通知模块调整
            return self.notify_service.instance.send(title=title, text=text)
        except Exception as e:
            print(f"通知发送失败: {e}")
            return False

    @eventmanager.register(EventType.ModuleReload)
    def on_module_reload(self, event: Event):
        """
        监听模块重载事件，重置通知服务实例，保证服务是最新的
        """
        event_data = event.event_data or {}
        module_id = event_data.get("module_id")
        # 如果没有指定模块，表示所有模块重载
        if not module_id:
            self.notify_service = self.notification_helper.get_service(name=self.notify_name)
