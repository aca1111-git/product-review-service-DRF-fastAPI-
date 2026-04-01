from bs4 import BeautifulSoup
# from urllib.parse import urljoin


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def extract_page_info(html: str) -> dict:
    soup = get_soup(html)
    text = soup.get_text(" ", strip=True)

    return {
        "title": soup.title.get_text(strip=True) if soup.title else "",
        "a_count": len(soup.select("a[href]")),
        "contains_review_word": "리뷰" in text,
        "contains_keyword": "수분크림" in text,
        "text_preview": text[:500],
    }

# 아래는 collectors로 이동
# def extract_candidate_links(site: str, base_url: str, html: str) -> list[dict]:
#     soup = get_soup(html)
#     candidates = []

#     for a in soup.select("a[href]"):
#         href = (a.get("href") or "").strip()
#         text = a.get_text(" ", strip=True)

#         if not href:
#             continue

#         full_url = urljoin(base_url, href)
#         keep = False

#         if site == "danawa":
#             if "prod.danawa.com" in full_url:
#                 keep = True

#         elif site == "hwahae":
#             if "hwahae.co.kr" in full_url and (
#                 "/products/" in full_url
#                 or "/product/" in full_url
#                 or "/goods/" in full_url
#             ):
#                 keep = True

#         elif site == "glowpick":
#             if "glowpick.co.kr" in full_url and (
#                 "/product/" in full_url
#                 or "/products/" in full_url
#                 or "/ranking/" in full_url
#             ):
#                 keep = True

#         if keep:
#             candidates.append({
#                 "title": text[:255],
#                 "url": full_url,
#             })

#     unique_items = []
#     seen = set()

#     for item in candidates:
#         if item["url"] not in seen:
#             seen.add(item["url"])
#             unique_items.append(item)

#     return unique_items