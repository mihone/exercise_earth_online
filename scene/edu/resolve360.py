#!/usr/bin/env python3
"""还原 360 搜索 /link?m= 跳转链为真实 URL。

用法: python3 resolve360.py "<URL>" [URL2 ...]
"""
import re
import subprocess
import sys

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def resolve(link):
    # 跟随重定向，打印最终落地 URL
    out = subprocess.run(
        ["curl", "-sL", "-o", "/dev/null", "-w", "%{url_effective}",
         "--max-time", "20", "-A", UA, link],
        capture_output=True)
    final = out.stdout.decode("utf-8", errors="ignore").strip()
    if final and "so.com/link" not in final:
        return final
    # 兜底：从 meta refresh / JS 跳转里抠地址
    page = subprocess.run(
        ["curl", "-sL", "--max-time", "20", "-A", UA, link],
        capture_output=True).stdout.decode("utf-8", errors="ignore")
    m = re.search(r'(?:URL=|location\.(?:href|replace)\(["\'])(https?://[^"\'>\s)]+)',
                  page, re.I)
    return m.group(1) if m else link


if __name__ == "__main__":
    for u in sys.argv[1:]:
        print(resolve(u))
