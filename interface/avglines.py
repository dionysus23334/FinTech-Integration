
import streamlit as st
import pandas as pd


class AvgLines:

    def __init__(self, df: pd.DataFrame):
        
        self.df = df
        # 计算 P(t)
        self.df = self.df.sort_values(["股票代码", "日期"])
        self.df["P"] = (self.df["MA_5"] - self.df["MA_10"])**2 + (self.df["MA_10"] - self.df["MA_20"])**2 + (self.df["MA_5"] - self.df["MA_20"])**2
        self.df["P_diff"] = self.df.groupby("股票代码")["P"].diff()

        # 判断是否收敛
    def is_converging(self, group, window_length, threshold):
        group = group.dropna(subset=["P_diff", "P"])
        if len(group) < window_length:
            return False
        last_n = group.tail(window_length)
        return all(last_n["P_diff"] < 0) and all(last_n["P"] < threshold)
    
    def get_convergent_stocks(self, window_length, threshold):
        # 筛选股票
        converging_stocks = []
        for code, group in self.df.groupby("股票代码"):
        if self.is_converging(group, window_length, threshold):
            converging_stocks.append(code)
        
        return converging_stocks

