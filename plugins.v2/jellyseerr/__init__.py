from app.plugins import _PluginBase
from .handler import register_event
from typing import List, Dict, Any, Tuple


class JellyseerrNotify(_PluginBase):
    plugin_name = "Jellyseerr通知推送"
    plugin_desc = "监听Jellyseerr Webhook并通过MoviePilot通知推送"
    plugin_icon = "Wechat.png"
    plugin_version = "1.0"
    plugin_author = "whoiskb"
    plugin_config_prefix = "jellyseerr_notify_"
    plugin_order = 99
    auth_level = 1

    def init_plugin(self, config: dict = None):
        register_event(config)

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
