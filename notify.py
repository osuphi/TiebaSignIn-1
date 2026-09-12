"""微信推送：PushPlus / Server酱

- PushPlus: 接口文档 https://www.pushplus.plus/doc/guide/api.html
- Server酱: 调用实例 https://github.com/easychen/serverchan-demo
    SCT 开头的 SendKey: https://sctapi.ftqq.com/<sendkey>.send
    sctp<数字>t 开头的 SendKey (Server酱³): https://<数字>.push.ft07.com/send/<sendkey>.send

按 key 前缀自动选择通道，未配置 key 时不会发起任何网络请求；
推送失败只记录日志，不会让 Actions 失败。
"""

import logging
import re

import requests

logger = logging.getLogger(__name__)

PUSHPLUS_URL = "https://www.pushplus.plus/send"
SERVERCHAN_URL = "https://sctapi.ftqq.com/{key}.send"
SERVERCHAN_SC3_RE = re.compile(r"^sctp(\d+)t", re.IGNORECASE)


def build_title(stats: dict, total: int) -> str:
    """根据签到统计生成推送标题（Server酱 要求 title 不能含换行）"""
    if stats["error"] > 0:
        return f"贴吧签到 {stats['success']}/{total}，失败 {stats['error']}"
    return f"贴吧签到 {stats['success']}/{total}，全部成功"


def build_content(total: int, stats: dict, final_failed_names: list) -> str:
    """生成 markdown 格式的推送正文"""
    lines = [
        f"- 贴吧总数: **{total}**",
        f"- 签到成功: **{stats['success']}**",
        f"- 已经签到: **{stats['exist']}**",
        f"- 被屏蔽的: **{stats['shield']}**",
        f"- 签到失败: **{stats['error']}**",
    ]
    if final_failed_names:
        lines.append("")
        lines.append(f"重试后仍失败: {', '.join(final_failed_names)}")
    return "\n".join(lines)


def serverchan_url(sendkey: str):
    """根据 SendKey 生成 Server酱推送地址，格式无法识别时返回 None"""
    if sendkey.lower().startswith("sctp"):
        match = SERVERCHAN_SC3_RE.match(sendkey)
        if not match:
            return None
        return f"https://{match.group(1)}.push.ft07.com/send/{sendkey}.send"
    if sendkey.upper().startswith("SCT"):
        return SERVERCHAN_URL.format(key=sendkey)
    return None


def send_serverchan(sendkey: str, title: str, content: str, timeout: int = 10) -> bool:
    """通过 Server酱发送，成功判定为响应中的 code == 0"""
    url = serverchan_url(sendkey)
    if url is None:
        logger.warning("SendKey 格式无法识别，跳过 Server酱推送")
        return False

    payload = {"title": title, "desp": content}
    headers = {"Content-Type": "application/json;charset=utf-8"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        data = resp.json()
    except Exception as e:
        logger.warning(f"Server酱推送异常: {e}")
        return False

    if data.get("code") == 0:
        logger.info("Server酱推送成功")
        return True

    logger.warning(f"Server酱推送失败: code={data.get('code')} message={data.get('message')}")
    return False


def send_pushplus(token: str, title: str, content: str, topic: str = "", timeout: int = 10) -> bool:
    """通过 PushPlus 发送，成功判定为响应中的 code == 200"""
    if not token:
        logger.info("未配置 PUSHPLUS_TOKEN，跳过推送")
        return False

    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown",
    }
    if topic:
        payload["topic"] = topic

    try:
        resp = requests.post(PUSHPLUS_URL, json=payload, timeout=timeout)
        data = resp.json()
    except Exception as e:
        logger.warning(f"PushPlus 推送异常: {e}")
        return False

    if data.get("code") == 200:
        logger.info("PushPlus 推送成功")
        return True

    logger.warning(f"PushPlus 推送失败: code={data.get('code')} msg={data.get('msg')}")
    return False


def send(key: str, title: str, content: str, topic: str = "", timeout: int = 10) -> bool:
    """按 key 前缀自动选择通道：SCT / sctp 开头走 Server酱，其它走 PushPlus"""
    if not key:
        logger.info("未配置推送 key，跳过推送")
        return False

    if key.upper().startswith("SCT"):
        return send_serverchan(key, title, content, timeout=timeout)

    return send_pushplus(key, title, content, topic=topic, timeout=timeout)
