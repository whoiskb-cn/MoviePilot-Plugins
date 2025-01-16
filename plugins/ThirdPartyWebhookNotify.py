from app.plugins import _PluginBase
from typing import Any, List, Dict, Tuple
from app.log import logger
from app.schemas import NotificationType
from app import schemas


class ThirdPartyWebhookNotify(_PluginBase):
    # 插件名称
    plugin_name = "第三方Webhook通知"
    # 插件描述
    plugin_desc = "接收第三方Webhook通知并推送到MoviePilot。"
    # 插件图标
    plugin_icon = "https://raw.githubusercontent.com/yourrepo/icons/thirdparty.png"
    # 插件版本
    plugin_version = "1.0"
    # 插件作者
    plugin_author = "YourName"
    # 作者主页
    author_url = "https://github.com/yourusername"
    # 插件配置项ID前缀
    plugin_config_prefix = "thirdpartywebhook_"
    # 加载顺序
    plugin_order = 40
    # 可使用的用户级别
    auth_level = 1

    _enabled = False
    _notify = False
    _msgtype = None

    def init_plugin(self, config: dict = None):
        if config:
            self._enabled = config.get("enabled")
            self._notify = config.get("notify")
            self._msgtype = config.get("msgtype")

    def send_notify(self, text: str) -> schemas.Response:
        """
        发送通知
        """
        logger.info(f"收到第三方webhook消息: {text}")
        if self._enabled and self._notify:
            mtype = NotificationType.Manual
            if self._msgtype:
                mtype = NotificationType.__getitem__(str(self._msgtype)) or NotificationType.Manual
            self.post_message(title="第三方通知",
                              mtype=mtype,
                              text=text)

        return schemas.Response(
            success=True,
            message="发送成功"
        )

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        """
        获取插件API
        """
        return [{
            "path": "/webhook",
            "endpoint": self.receive_webhook,
            "methods": ["POST"],
            "summary": "接收第三方Webhook",
            "description": "此API接收来自第三方系统的Webhook通知，并推送到MoviePilot。",
        }]

    def receive_webhook(self, data: dict) -> schemas.Response:
        """
        接收第三方Webhook通知
        """
        if self._enabled:
            # 假设 'text' 是Webhook数据中的一部分
            text = data.get("text", "无内容")
            self.send_notify(text)
        else:
            logger.warning("插件未启用，无法处理Webhook通知。")
        
        return schemas.Response(
            success=True,
            message="Webhook接收成功"
        )

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面
        """
        # 编历 NotificationType 枚举，生成消息类型选项
        MsgTypeOptions = []
        for item in NotificationType:
            MsgTypeOptions.append({
                "title": item.value,
                "value": item.name
            })
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'notify',
                                            'label': '开启通知',
                                        }
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12
                                },
                                'content': [
                                    {
                                        'component': 'VSelect',
                                        'props': {
                                            'multiple': False,
                                            'chips': True,
                                            'model': 'msgtype',
                                            'label': '消息类型',
                                            'items': MsgTypeOptions
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': '第三方Webhook配置：http://ip:3001/api/v1/plugin/ThirdPartyWebhookNotify/webhook?apikey=*****&text=hello world。'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "notify": False,
            "msgtype": ""
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        pass
