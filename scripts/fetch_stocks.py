#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据抓取脚本
使用 Tushare Pro API 获取股票数据
"""

import os
import pandas as pd
from datetime import datetime

try:
    import tushare as ts
except ImportError:
    print("请先安装 tushare：pip install tushare")
    exit(1)

TOKEN = os.getenv("TUSHARE_TOKEN", "")

def fetch_stock_data():
    if not TOKEN:
        print("请设置 TUSHARE_TOKEN 环境变量")
        return None
    
    pro = ts.pro_api(TOKEN)
    try:
        df = pro.index_daily(ts_code='000001.SH')
        return df.head(10).to_dict('records')
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def generate_stock_page(data, output_path):
    if not data:
        content = "数据获取失败，请检查 Token 或网络连接。"
    else:
        df = pd.DataFrame(data)
        table = df.to_markdown(index=False)
        content = f"""---
title: 股票跟踪
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

## 最新行情

{table}

> 数据更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"股票数据页面已更新: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output = os.path.join(base_dir, "source/_posts/stock-tracking.md")
    data = fetch_stock_data()
    generate_stock_page(data, output)
