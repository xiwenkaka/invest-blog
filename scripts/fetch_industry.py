#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业数据抓取脚本 - 电解铝库存
"""

import os
import requests
from datetime import datetime

def fetch_shfe_aluminum():
    try:
        url = "http://www.shfe.com.cn/data/dailydata/wk warehouse_receipts.dat"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        for item in data.get('o_stocks', []):
            if item.get('variety') == 'AL':
                return {
                    'date': item.get('trandate', ''),
                    'warehouse_receipts': item.get('wrstorehouse', ''),
                    'total_receipts': item.get('wrrtotal', '')
                }
        return None
    except Exception as e:
        print(f"获取SHFE数据失败: {e}")
        return None

def generate_industry_page(shfe_data, output_path):
    content = f"""---
title: 电解铝库存跟踪
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

## 电解铝库存数据

| 指标 | 数据 |
|------|------|
| 日期 | {shfe_data.get('date', 'N/A') if shfe_data else 'N/A'} |
| 仓单量 | {shfe_data.get('warehouse_receipts', 'N/A') if shfe_data else 'N/A'} |
| 总库存 | {shfe_data.get('total_receipts', 'N/A') if shfe_data else 'N/A'} |

> 数据更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"电解铝数据页面已更新: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output = os.path.join(base_dir, "source/_posts/aluminum-industry.md")
    shfe_data = fetch_shfe_aluminum()
    generate_industry_page(shfe_data, output)
