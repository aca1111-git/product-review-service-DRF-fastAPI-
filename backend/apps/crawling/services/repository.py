from apps.crawling.models import CrawlRawData

def upsert_raw_data(unique_key: str, defaults: dict):
    """
    unique_key 기준으로 CrawlRawData를 update_or_create 합니다.
    """
    obj, created = CrawlRawData.objects.update_or_create(
        unique_key=unique_key,
        defaults=defaults,
    )
    return obj, created
