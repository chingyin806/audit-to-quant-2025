#!/usr/bin/env python
# coding: utf-8

# In[3]:


#install
get_ipython().system('pip install selenium')


# In[2]:


# Day 3 matplotlib 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np          # 

# 讀取pre儲存嘅 TQQQ 數據
df = pd.read_csv("TQQQ_30d_real.csv", index_col='Date', parse_dates=True)

# 計20日同25日均線（only got29日數據，用25日代替60日）
df['SMA20'] = df['Close'].rolling(window=20).mean()
df['SMA25'] = df['Close'].rolling(window=25).mean()

# 金叉死叉訊號
df['Signal'] = 0
df['Signal'][20:] = np.where(df['SMA20'][20:] > df['SMA25'][20:], 1, -1)
df['Position'] = df['Signal'].diff()   # 1=金叉買入，-1=死叉賣出

# === 下面開始畫超靚 K 線 ===
fig, ax = plt.subplots(figsize=(16,9))

# 上漲日（綠色）
up = df[df.Close >= df.Open]
# 下跌日（紅色）
down = df[df.Close < df.Open]

# 畫 K 線實體同影線
width = 0.6
width2 = 0.1

ax.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color='green')
ax.bar(up.index, up.High-up.Close, width2, bottom=up.Close, color='green')
ax.bar(up.index, up.Low-up.Open, width2, bottom=up.Open, color='green')

ax.bar(down.index, down.Open-down.Close, width, bottom=down.Close, color='red')
ax.bar(down.index, down.High-down.Open, width2, bottom=down.Open, color='red')
ax.bar(down.index, down.Low-down.Close, width2, bottom=down.Close, color='red')

# 畫均線
ax.plot(df.index, df['SMA20'], color='orange', label='20日均線', linewidth=2)
ax.plot(df.index, df['SMA25'], color='blue', label='25日均線', linewidth=2)

# 金叉綠箭咀，死叉紅箭咀
ax.scatter(df.index[df['Position']==1], df['Close'][df['Position']==1],
           marker='^', color='lime', s=300, label='金叉買入', zorder=5)
ax.scatter(df.index[df['Position']==-1], df['Close'][df['Position']==-1],
           marker='v', color='red', s=300, label='死叉賣出', zorder=5)

ax.set_title('TQQQ 3x Nasdaq-100 | 20/25 day average cross\nBig 4 Audit → Quant Day 3', fontsize=18)#20/25日均線交叉策略
ax.set_ylabel('Price (US$)', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('TQQQ_day3_FINAL.png', dpi=300, bbox_inches='tight')
plt.show()

print("Day 3！Graph saved as TQQQ_day3_FINAL.png")


# In[ ]:




