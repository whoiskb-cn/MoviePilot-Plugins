from app.events import eventmanager, EventType, Event
from app.helper.notification import NotificationHelper
from app.schemas.types import MessageChannel
from app.log import logger

_notify_name = "wechat_notify"


def register_event(config: dict = None):
    global _notify_name
    if config:
        _notify_name = config.get("notify_name") or "wechat_notify"


@eventmanager.register(EventType.WebhookMessage)
def handle_webhook(event: Event):
    """
    处理Jellyseerr webhook推送
    """
    if not event or not event.event_data:
        return

    url = event.event_data.get("url", "")
    payload = event.event_data.get("payload")

    if not payload or "/webhook/jelly" not in url:
        return

    # 解析 Jellyseerr payload
    event_type = payload.get("event")
    requested_by = payload.get("requestedBy", {}).get("displayName", "未知用户")
    media_title = payload.get("media", {}).get("title", "未知媒体")

    # 自定义通知标题和内容
    title = f"[Jellyseerr] {event_type}"
    text = f"用户 {requested_by} 请求的《{media_title}》状态变更：{event_type}"

    # 调用通知服务
    notifier = NotificationHelper()
    service = notifier.get_service(name=_notify_name)

    if service and service.instance:
        logger.info(f"发送通知至：{_notify_name} -> {title}")
        service.instance.send_text(title=title, text=text)
    else:
        logger.error(f"找不到通知服务：{_notify_name}")
