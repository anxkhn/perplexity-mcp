import argparse
import json
import re
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from perplexity import Client


CATEGORIES = [
    "twitter",
    "youtube",
    "interviews",
    "articles",
    "podcasts",
    "newsletters",
    "websites",
]

PERSON_CONTEXT = {
    "Mukund Jha": "CEO, Emergent",
    "Hemant Mohapatra": "Partner, Lightspeed",
    "Shashank Kumar": "Co-Founder, Razorpay",
    "Varun Mayya": "Entrepreneur, Content Creator",
    "Mukul Rustagi": "Co-founder, Polaris School of Technology",
    "Kavikrut": "CEO, T-Hub",
    "Akash Balasubramani": "Ecosystem Lead, Starkware",
    "Shubham Gupta": "Co-Founder & General Partner, Together Fund",
    "Ajit Tripathi": "Executive Director, EigenCloud",
    "Jared Friedman": "General Partner, YCombinator",
    "Chandra R. Srikanth": "Executive Editor, Technology & Startups, Moneycontrol",
}

ROUND_SIZE = 100
MAX_ROUNDS = 1
DEFAULT_MODEL = None
DEFAULT_MODE = "auto"
MAX_REQUEST_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5
VALID_URL_PATTERNS = {
    "twitter": [
        re.compile(r"^https?://(x|twitter)\.com/[A-Za-z0-9_./?=&%-]+$"),
    ],
    "youtube": [
        re.compile(r"^https?://(www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]{6,}$"),
        re.compile(r"^https?://(www\.)?youtube\.com/shorts/[A-Za-z0-9_-]{6,}$"),
        re.compile(r"^https?://(www\.)?youtube\.com/@[A-Za-z0-9_.-]+$"),
        re.compile(
            r"^https?://(www\.)?youtube\.com/c/[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)?$"
        ),
        re.compile(
            r"^https?://(www\.)?youtube\.com/channel/[A-Za-z0-9_-]+(/[A-Za-z0-9_.-]+)?$"
        ),
        re.compile(r"^https?://(www\.)?youtube\.com/playlist\?list=[A-Za-z0-9_-]+$"),
        re.compile(r"^https?://youtu\.be/[A-Za-z0-9_-]{6,}$"),
        re.compile(r"^https?://music\.youtube\.com/podcast/[A-Za-z0-9_-]+$"),
    ],
}


@dataclass
class LinkItem:
    url: str
    published_at: Optional[str]


def extract_json_array(text: str) -> List[dict]:
    fence_match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if fence_match:
        return json.loads(fence_match.group(1))

    bracket_match = re.search(r"(\[\s*\{.*\}\s*\])", text, re.DOTALL)
    if bracket_match:
        return json.loads(bracket_match.group(1))

    raise ValueError("No JSON array found in response")


def normalize_url(url: str) -> str:
    return url.strip().rstrip("/")


def is_valid_url_for_category(url: str, category: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False
    patterns = VALID_URL_PATTERNS.get(category)
    if not patterns:
        return True
    return any(pattern.match(url) for pattern in patterns)


def build_prompt(person: str, category: str, existing_urls: Iterable[str]) -> str:
    context = PERSON_CONTEXT[person]
    category_rules = {
        "twitter": "Prefer x.com/twitter.com profile or post links directly tied to this person.",
        "youtube": "Prefer direct YouTube video, channel, or playlist links tied to this person.",
        "interviews": "Prefer direct interview pages, transcripts, or interview videos featuring this person.",
        "articles": "Prefer direct article links written by or substantially about this person.",
        "podcasts": "Prefer direct podcast episode or show links featuring this person.",
        "newsletters": "Prefer direct newsletter posts or archives authored by or featuring this person.",
        "websites": "Prefer official personal, company, profile, or primary website pages directly relevant to this person.",
    }[category]
    exclusions = json.dumps(list(existing_urls), ensure_ascii=True)
    return (
        f"Find up to {ROUND_SIZE} unique public links for {person} ({context}) in category '{category}'. "
        f"{category_rules} Return ONLY a JSON array. Each item must be an object with keys 'url' and 'published_at'. "
        "Use the exact published date/time if confidently known from the source or result metadata; otherwise use null. "
        "Do not include explanations, markdown, or prose. Do not invent URLs or timestamps. "
        f"Important context for disambiguation: the target person is {person}, who is {context}. "
        "If there are fewer than 100 real links, return only as many high-confidence real links as exist. "
        f"Exclude these URLs: {exclusions}"
    )


def fetch_category(
    person: str,
    category: str,
    cookies: Dict[str, str],
    mode: str,
    model: Optional[str],
) -> List[LinkItem]:
    client = Client(cookies)
    collected: List[LinkItem] = []
    seen = set()

    for _ in range(MAX_ROUNDS):
        prompt = build_prompt(person, category, [item.url for item in collected])
        response = None
        for attempt in range(MAX_REQUEST_ATTEMPTS):
            try:
                response = client.search(prompt, mode=mode, model=model)
            except Exception:
                response = None
            if isinstance(response, dict):
                break
            time.sleep(RETRY_DELAY_SECONDS)

        if not isinstance(response, dict):
            break

        answer = response.get("answer", "")

        try:
            payload = extract_json_array(answer)
        except Exception:
            break

        new_count = 0
        for item in payload:
            url = normalize_url(str(item.get("url", "")))
            if not url or url in seen or not is_valid_url_for_category(url, category):
                continue
            seen.add(url)
            published_at = item.get("published_at")
            if published_at is not None:
                published_at = str(published_at).strip() or None
            collected.append(LinkItem(url=url, published_at=published_at))
            new_count += 1
            if len(collected) >= 100:
                return collected

        if new_count == 0:
            break

    return collected


def write_markdown(
    output_path: str, results: Dict[str, Dict[str, List[LinkItem]]]
) -> None:
    lines: List[str] = []
    for person in results:
        lines.append(f"# {person}")
        for category in CATEGORIES:
            lines.append(f"## {category}")
            items = results[person].get(category, [])
            if not items:
                lines.append("- none found")
            else:
                for item in items:
                    published = item.published_at if item.published_at else "unknown"
                    lines.append(f"- {item.url} | published: {published}")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def append_section(
    file_handle,
    person: str,
    category: str,
    items: List[LinkItem],
    write_person_header: bool,
) -> None:
    file_handle.write(f"# {person}\n" if write_person_header else "")
    file_handle.write(f"## {category}\n")
    if not items:
        file_handle.write("- none found\n\n")
    else:
        for item in items:
            published = item.published_at if item.published_at else "unknown"
            file_handle.write(f"- {item.url} | published: {published}\n")
        file_handle.write("\n")
    file_handle.flush()


def load_completed_sections(output_path: str) -> Dict[str, set]:
    completed: Dict[str, set] = {}
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            current_person = None
            for raw_line in f:
                line = raw_line.strip()
                if line.startswith("# "):
                    current_person = line[2:]
                    completed.setdefault(current_person, set())
                elif line.startswith("## ") and current_person:
                    completed.setdefault(current_person, set()).add(line[3:])
    except FileNotFoundError:
        return {}
    return completed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cookies-json", required=True)
    parser.add_argument("--people", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--mode", default=DEFAULT_MODE)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    cookies = json.loads(args.cookies_json)
    completed = load_completed_sections(args.output) if args.resume else {}
    file_mode = "a" if args.resume else "w"
    with open(args.output, file_mode, encoding="utf-8") as f:
        for person in args.people:
            print(f"Starting person: {person}", flush=True)
            person_header_written = person in completed
            for category in CATEGORIES:
                if category in completed.get(person, set()):
                    print(f"  Skipping {category}, already written", flush=True)
                    continue
                print(f"  Collecting {category}...", flush=True)
                items = fetch_category(
                    person,
                    category,
                    cookies,
                    args.mode,
                    args.model,
                )
                append_section(
                    f,
                    person,
                    category,
                    items,
                    write_person_header=not person_header_written,
                )
                person_header_written = True
                print(f"  Wrote {len(items)} item(s) for {category}", flush=True)


if __name__ == "__main__":
    main()
