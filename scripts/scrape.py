#!/usr/bin/env python3
import json, re, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "scraper-config.json"
OUTPUT = ROOT / "data" / "scraped-products.json"
UA = "MaquitosProductHub/1.0 (+GitHub Actions; respectful product metadata fetcher)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")


def iter_jsonld(html):
    for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, flags=re.I | re.S):
        try:
            data = json.loads(raw.strip())
        except Exception:
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            node = stack.pop(0)
            if isinstance(node, dict):
                graph = node.get("@graph")
                if isinstance(graph, list):
                    stack.extend(graph)
                yield node


def product_from(node, source_name, url):
    typ = node.get("@type")
    types = typ if isinstance(typ, list) else [typ]
    if "Product" not in types:
        return None
    offers = node.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    image = node.get("image") or ""
    if isinstance(image, list): image = image[0] if image else ""
    if isinstance(image, dict): image = image.get("url", "")
    brand = node.get("brand") or ""
    if isinstance(brand, dict): brand = brand.get("name", "")
    return {
        "name": node.get("name", ""),
        "description": re.sub(r"\s+", " ", str(node.get("description", ""))).strip(),
        "sku": node.get("sku", ""),
        "brand": brand,
        "image": image,
        "price": offers.get("price") or offers.get("lowPrice") or "",
        "currency": offers.get("priceCurrency", ""),
        "availability": offers.get("availability", ""),
        "source": source_name,
        "url": node.get("url") or url,
    }


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {"sources": []}
    products, errors = [], []
    for source in cfg.get("sources", []):
        if source.get("enabled", True) is False:
            continue
        name = source.get("name") or "Fuente"
        for url in source.get("urls", []):
            try:
                html = fetch(url)
                found = False
                for node in iter_jsonld(html):
                    item = product_from(node, name, url)
                    if item and item.get("name"):
                        products.append(item); found = True
                if not found:
                    errors.append({"source": name, "url": url, "error": "No Product JSON-LD found"})
            except Exception as exc:
                errors.append({"source": name, "url": url, "error": str(exc)[:300]})
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(products),
        "products": products,
        "errors": errors,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Maquitos scraper: {len(products)} products, {len(errors)} notices")

if __name__ == "__main__":
    main()
