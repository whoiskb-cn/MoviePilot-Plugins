from ...events import eventmanager, EventType, Event
from ...helper.notification import NotificationHelper
from ...log import logger

_notify_name = "wechat_notify"

def register_event(config: dict = None):
    global _notify_name
    if config:
        _notify_name = config.get("notify_name") or "wechat_notify"

@eventmanager.register(EventType.WebhookMessage)
def handle_webhook(event: Event):
    if not event or not event.event_data:
        return

    url = event.event_data.get("url", "")
    payload = event.event_data.get("payload")

    # 确认请求是来自 jellyseerr webhook
    if not payload or "/webhook/jelly" not in url:
        return

    event_type = payload.get("event", "未知事件")
    requested_by = payload.get("requestedBy", {}).get("displayName", "未知用户")
    media_title = payload.get("media", {}).get("title", "未知媒体")

    title = f"[Jellyseerr] {event_type}"
    text = f"用户 {requested_by} 请求的《{media_title}》状态变更：{event_type}"

    notifier = NotificationHelper()
    service = notifier.get_service(name=_notify_name)

    if service and service.instance:
        try:
            logger.info(f"发送通知至：{_notify_name} -> {title}")
            # 有的通知服务可能是 send_text，也可能是 send
            if hasattr(service.instance, "send_text"):
                service.instance.send_text(title=title, text=text)
            elif hasattr(service.instance, "send"):
                service.instance.send(title=title, text=text)
            else:
                logger.error(f"通知服务实例不支持发送方法")
        except Exception as e:
            logger.error(f"通知发送失败: {e}")
    else:
        logger.error(f"找不到通知服务：{_notify_name}")
