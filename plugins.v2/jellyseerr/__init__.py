from app.plugins import PluginBase
from .handler import register_webhook_handler

class Plugin(PluginBase):
    def init_plugin(self, config: dict = None):
        register_webhook_handler(config)

    def get_plugin_info(self):
        return {
            "name": "Jellyseerr通知转发",
            "description": "监听Jellyseerr Webhook并推送通知到微信",
            "author": "whoiskb",
            "version": "1.0"
        }

