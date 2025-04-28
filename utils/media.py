from utils.config import get


def get_full_image_url(image_url: str) -> str:
    return f"{get('IMAGE_URL_PREFIX')}{image_url}"


def get_full_video_url(video_url: str | None) -> str | None:
    if video_url is None:
        return None
    return f"{get('VIDEO_URL_PREFIX')}{video_url}"
