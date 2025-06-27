from app.events import eventmanager, EventType, Event
from app.helper.notification import NotificationHelper
from app.schemas.types import MessageChannel

_notify_name = None

def register_webhook_handler(config: dict = None):
    global _notify_name
    _notify_name = config.get("wechat_name") or "wechat_notify"  # 默认通知服务名


@eventmanager.register(EventType.WebhookMessage)
def handle_jellyseerr_webhook(event: Event):
    """
    监听 Jellyseerr Webhook 消息
    """
    if not event or not event.event_data:
        return

    payload = event.event_data.get("payload")
    headers = event.event_data.get("headers")
    url = event.event_data.get("url", "")

    # 你可以根据url判断来源，例如 Jellyseerr 设置 webhook 为 http://xxx/webhook/jelly
    if "/webhook/jelly" not in url:
        return

    # 提取消息字段（根据 Jellyseerr 的 webhook 格式来解析）
    event_type = payload.get("event")  # 如 media.approved
    requested_by = payload.get("requestedBy", {}).get("displayName", "未知用户")
    media_title = payload.get("media", {}).get("title")
    status = event_type.replace(".", " ").title() if event_type else "通知"

    # 构造通知
    title = f"[Jellyseerr] {status}"
    text = f"用户 {requested_by} 请求的《{media_title}》状态：{status}"

    # 发送通知
    notifier = NotificationHelper()
    service_info = notifier.get_service(name=_notify_name)
    if service_info and service_info.instance:
        service_info.instance.send_text(title=title, text=text)

