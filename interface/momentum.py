import streamlit as st
import pandas as pd
import altair as alt

class MomentumApp:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.top_momentum = None
  
    def get_top_momentum(self, N, top_k):
      
          # 对每只股票分别计算 N 日动量
        self.df['动量基准价'] = self.df.groupby('股票代码')['收盘价'].shift(N)
        self.df['动量'] = (self.df['收盘价'] - self.df['动量基准价']) / self.df['动量基准价']
    
        # 提取最新日期每只股票的动量
        latest_date = self.df['日期'].max()
        latest_df = self.df[self.df['日期'] == latest_date][['股票代码', '动量']].dropna()
 
        top_momentum = latest_df.sort_values('动量', ascending=False).head(top_k)
        top_momentum = top_momentum.reset_index(drop=True)

        self.top_momentum = top_momentum
      
        return top_momentum

    def get_bar_chart(self, width=800, height=400, labelAngle=45):
      
        # 使用 Altair 绘制柱状图，按动量值降序排列
        chart = alt.Chart(self.top_momentum).mark_bar().encode(
            x=alt.X('股票代码:N', title='股票代码'),
            y=alt.Y('动量:Q', title='动量'),
            color='动量:Q',
            tooltip=['股票代码', '动量']
        ).properties(
            width=width,
            height=height
        ).configure_axis(
            labelAngle=labelAngle  # 如果标签过长，可以调整角度
        )

        return chart
        

