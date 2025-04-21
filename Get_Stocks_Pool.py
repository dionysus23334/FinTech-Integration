
import pandas as pd 
import streamlit as st

from interface.momentum import MomentumApp
from interface.general import GeneralIndicator
from interface.avglines import AvgLines

st.set_page_config(page_title="📈 股票筛选池", layout="wide")

st.title("📊 股票筛选池整合平台")

# 分别上传两个数据文件
st.subheader("📁 数据上传")
col1, col2 = st.columns(2)

with col1:
    uploaded_main = st.file_uploader("上传主行情数据（包含收盘价）", type=["csv"], key="main")
with col2:
    uploaded_ma = st.file_uploader("上传均线数据（包含MA_5, MA_10, MA_20）", type=["csv"], key="ma")

if uploaded_main is not None and uploaded_ma is not None:
    df_main = pd.read_csv(uploaded_main, dtype={"股票代码": str})
    df_main["日期"] = pd.to_datetime(df_main["日期"])

    df_ma = pd.read_csv(uploaded_ma, dtype={"股票代码": str})
    df_ma["日期"] = pd.to_datetime(df_ma["日期"])

    tab1, tab2, tab3 = st.tabs(["🔥 动量策略", "📈 RPS & 波动率", "🔄 均线收敛"])

    with tab1:
        st.header("🔥 动量筛选器")
        N = st.slider("动量周期（N日）", min_value=5, max_value=90, value=30)
        top_k = st.slider("展示前Top-K动量股票", min_value=5, max_value=2000, value=20)

        mom_app = MomentumApp(df_main.copy())
        top_df = mom_app.get_top_momentum(N, top_k)
        st.dataframe(top_df)
        st.altair_chart(mom_app.get_bar_chart(), use_container_width=True)
        momentum_codes = set(top_df["股票代码"])

    with tab2:
        st.header("📈 RPS + 波动率筛选器")
        vol_period = st.slider("波动率周期", 5, 90, 20)
        rps_threshold = st.number_input("最低RPS（任意周期）阈值", value=20.0)
        vol_max = st.number_input("最大允许波动率", value=60.0)

        gen = GeneralIndicator(df_main.copy())
        rps_df = gen.get_rps_and_std(vol_period)
        filtered = rps_df[
            (rps_df.filter(like="RPS").max(axis=1) > rps_threshold) &
            (rps_df[f"波动率{vol_period}"] < vol_max)
        ]
        st.dataframe(filtered)
        rps_vol_codes = set(filtered["股票代码"])

    with tab3:
        st.header("🔄 均线收敛筛选器")
        window = st.slider("连续下降天数窗口", 3, 20, 5)
        threshold = st.number_input("收敛阈值 P", value=1.0)

        avg = AvgLines(df_ma.copy())
        converged_df = avg.get_convergent_stocks(window, threshold)
        st.dataframe(converged_df)
        avgline_codes = set(converged_df["股票代码"])

    st.markdown("---")
    st.header("📌 筛选交集结果")

    selected_methods = st.multiselect(
        "请选择需要满足的策略交集条件",
        options=["动量策略", "RPS & 波动率", "均线收敛"],
        default=["动量策略", "RPS & 波动率"]
    )

    sets = []
    if "动量策略" in selected_methods:
        sets.append(momentum_codes)
    if "RPS & 波动率" in selected_methods:
        sets.append(rps_vol_codes)
    if "均线收敛" in selected_methods:
        sets.append(avgline_codes)

    if sets:
        final_selection = set.intersection(*sets)
        st.success(f"最终筛选出 {len(final_selection)} 支股票")
        st.dataframe(pd.DataFrame({"股票代码": list(final_selection)}))
    else:
        st.info("请至少选择一个策略以进行筛选")
else:
    st.warning("请上传两个数据文件后继续操作。")




