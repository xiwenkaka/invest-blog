#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业数据抓取脚本 - 电解铝库存
抓取铝相关行业数据

数据来源：
- 上海期货交易所 (SHFE)
- LME 伦敦金属交易所
- 我的有色网（需要登录）

本脚本使用期货交易所公开数据
"""

import os
import json
import requests
from datetime import datetime

def fetch_shfe_aluminum():
    """获取上海期货交易所铝库存数据"""
    try:
        # SHFE 仓单日报 API
        url = "http://www.shfe.com.cn/data/dailydata/wk warehouse_receipts.dat"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # 提取铝相关数据
        aluminum_data = {}
        for item in data.get('o_stocks', []):
            if item.get('variety') == 'AL':
                aluminum_data = {
                    'date': item.get('trandate', ''),
                    'warehouse_receipts': item.get('wrstorehouse', ''),
                    'total_receipts': item.get('wrrtotal', '')
                }
                break
        return aluminum_data
    except Exception as e:
        print(f"获取SHFE数据失败: {e}")
        return None

def fetch_lme_aluminum():
    """获取LME铝库存数据"""
    try:
        # LME 官方数据
        url = "https://lme-metal-api.bloomberg.net/v1/lme/aluminium"
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"获取LME数据失败: {e}")
        return None

def generate_industry_page(shfe_data, output_path):
    """生成行业数据页面"""
    content = f"""---
title: 电解铝库存跟踪
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

## 电解铝库存数据

### 上海期货交易所 (SHFE)

| 指标 | 数据 |
|------|------|
| 日期 | {shfe_data.get('date', 'N/A') if shfe_data else 'N/A'} |
| 仓单量 | {shfe_data.get('warehouse_receipts', 'N/A') if shfe_data else 'N/A'} |
| 总库存 | {shfe_data.get('total_receipts', 'N/A') if shfe_data else 'N/A'} |

### 观察要点

- SHFE 铝库存持续下降 → 现货偏紧，利好铝价
- 库存上升 → 下游需求疲软，压力加大

> 数据更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 数据来源：上海期货交易所
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"电解铝数据页面已更新: {output_path}")

if __name__ == "__main__":
    output = "../blog/source/_posts/aluminum-industry.md"
    shfe_data = fetch_shfe_aluminum()
    generate_industry_page(shfe_data, output)
