import pandas as pd
import numpy as np

class GeneralIndicator:

    def __init__(self, df: pd.DataFrame):
        
        self.df = df
        # 设置周期参数
        self.periods = [10, 20, 30, 60, 90]
        self.latest_date = self.df["日期"].max()
        self.result_df = None

    # 指标计算函数
    def calc_metrics(self, group):
        group = group.sort_values("日期")
        res = {"股票代码": group["股票代码"].iloc[0]}
        
        for p in self.periods:
            recent = group[group["日期"] <= self.latest_date].tail(p)
            if len(recent) < p:
                res[f"涨幅{p}"] = np.nan
                res[f"RPS{p}"] = np.nan
            else:
                start = recent["收盘价"].iloc[0]
                end = recent["收盘价"].iloc[-1]
                change = (end - start) / start * 100
                res[f"涨幅{p}"] = change
                res[f"RPS{p}"] = change  # 后续再统一替换为百分位排名

        returns = group["收盘价"].pct_change().dropna()
        recent_ret = returns[-vol_period:]
        res[f"波动率{vol_period}"] = (
            recent_ret.std() * np.sqrt(252) if len(recent_ret) >= vol_period else np.nan
        )

        return pd.Series(res)

    def get_rps_and_std(self):
        # 应用函数
        self.result_df = self.df.groupby("股票代码").apply(self.calc_metrics).reset_index(drop=True)
        return self.result_df
        
    def get_result(self):
        return self.result_df

      
