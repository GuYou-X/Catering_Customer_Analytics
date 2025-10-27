import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 设置页面
st.set_page_config(
    page_title="在线食品订单分析平台",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("🍕 在线食品订单分析平台")
st.markdown("---")

# 加载数据集
df = pd.read_csv('onlinefoods.csv')

# 数据预处理
df.columns = ['年龄', '性别', '婚姻状态', '职业', '月收入', '教育背景', '家庭人数', '纬度', '经度', '邮政编码', '订单状态', '反馈', 'Unnamed: 12']

df['性别'] = df['性别'].replace({
    'Female': '女性',
    'Male': '男性'
})

# 替换 '婚姻状态' 列中的值
df['婚姻状态'] = df['婚姻状态'].replace({
    'Single': '单身',
    'Married': '已婚',
    'Prefer not to say': '不愿透露'
})

# 替换 '职业' 列中的值
df['职业'] = df['职业'].replace({
    'Student': '学生',
    'Employee': '员工',
    'Self Employeed': '自雇',
    'House wife': '家庭主妇'
})

# 替换 '月收入' 列中的值
df['月收入'] = df['月收入'].replace({
    'No Income': '无收入',
    'Below Rs.10000': '低于10000元',
    'More than 50000': '超过50000元',
    '10001 to 25000': '10001到25000元',
    '25001 to 50000': '25001到50000元'
})

# 替换 '教育背景' 列中的值
df['教育背景'] = df['教育背景'].replace({
    'Post Graduate': '研究生',
    'Graduate': '本科',
    'Ph.D': '博士',
    'Uneducated': '未受教育',
    'School': '中学'
})

# 替换 '订单状态' 列中的值
df['订单状态'] = df['订单状态'].replace({
    'Yes': '是',
    'No': '否'
})

# 替换 '反馈' 列中的值
df['反馈'] = df['反馈'].replace({
    'Positive': '积极',
    'Negative ': '消极'
})

# 替换 'Unnamed: 12' 列中的值
df['Unnamed: 12'] = df['Unnamed: 12'].replace({
    'Yes': '是',
    'No': '否'
})

df.drop(['Unnamed: 12'],axis=1,inplace=True)

df.drop_duplicates(inplace=True)

# 侧边栏 - 数据筛选器
st.sidebar.header("🔍 数据筛选器")

# 年龄筛选
age_range = st.sidebar.slider(
    "选择年龄范围",
    min_value=int(df['年龄'].min()),
    max_value=int(df['年龄'].max()),
    value=(int(df['年龄'].min()), int(df['年龄'].max()))
)

# 性别筛选
genders = ['全部'] + list(df['性别'].unique())
selected_gender = st.sidebar.selectbox("选择性别", genders)

# 婚姻状态筛选
marital_statuses = ['全部'] + list(df['婚姻状态'].unique())
selected_marital = st.sidebar.selectbox("选择婚姻状态", marital_statuses)

# 收入筛选
incomes = ['全部'] + list(df['月收入'].unique())
selected_income = st.sidebar.selectbox("选择月收入范围", incomes)

# 教育背景筛选
educations = ['全部'] + list(df['教育背景'].unique())
selected_education = st.sidebar.selectbox("选择教育背景", educations)

# 应用筛选条件
filtered_df = df[
    (df['年龄'] >= age_range[0]) & 
    (df['年龄'] <= age_range[1])
]

if selected_gender != '全部':
    filtered_df = filtered_df[filtered_df['性别'] == selected_gender]

if selected_marital != '全部':
    filtered_df = filtered_df[filtered_df['婚姻状态'] == selected_marital]

if selected_income != '全部':
    filtered_df = filtered_df[filtered_df['月收入'] == selected_income]

if selected_education != '全部':
    filtered_df = filtered_df[filtered_df['教育背景'] == selected_education]

# 主页面布局
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 数据概览", "👥 客户分析", "💰 收入分析", "🗺️ 地理分布", "📋 订单分析"])

with tab1:
    st.header("数据概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总记录数", len(filtered_df))
    
    with col2:
        st.metric("平均年龄", f"{filtered_df['年龄'].mean():.1f}岁")
    
    with col3:
        st.metric("平均家庭人数", f"{filtered_df['家庭人数'].mean():.1f}人")
    
    with col4:
        male_count = len(filtered_df[filtered_df['性别'] == '男'])
        female_count = len(filtered_df[filtered_df['性别'] == '女'])
        gender_ratio = male_count / (male_count + female_count) * 100 if (male_count + female_count) > 0 else 0
        st.metric("性别比例(男:女)", f"{gender_ratio:.1f}% : {100-gender_ratio:.1f}%")
    
    # 数据显示
    st.subheader("筛选后的数据")
    st.dataframe(filtered_df, use_container_width=True)
    
    # 数据基本信息
    st.subheader("数据基本信息")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("数据类型:")
        st.write(filtered_df.dtypes)
    
    with col2:
        st.write("数据描述:")
        st.write(filtered_df[['年龄', '家庭人数']].describe())

with tab2:
    st.header("客户特征分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 年龄分布
        fig_age = px.histogram(
            filtered_df, 
            x='年龄', 
            title='年龄分布',
            color_discrete_sequence=['#FF6B6B']
        )
        fig_age.update_layout(
            xaxis_title="年龄",
            yaxis_title="人数"
        )
        st.plotly_chart(fig_age, use_container_width=True)
        
        # 性别分布
        gender_counts = filtered_df['性别'].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title='性别分布',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # 婚姻状态分布
        marital_counts = filtered_df['婚姻状态'].value_counts()
        fig_marital = px.bar(
            x=marital_counts.index,
            y=marital_counts.values,
            title='婚姻状态分布',
            color=marital_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_marital.update_layout(
            xaxis_title="婚姻状态",
            yaxis_title="人数"
        )
        st.plotly_chart(fig_marital, use_container_width=True)
        
        # 教育背景分布
        education_counts = filtered_df['教育背景'].value_counts()
        fig_education = px.pie(
            values=education_counts.values,
            names=education_counts.index,
            title='教育背景分布',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_education, use_container_width=True)
    
    # 职业分布
    st.subheader("职业分布")
    occupation_counts = filtered_df['职业'].value_counts()
    fig_occupation = px.bar(
        y=occupation_counts.index,
        x=occupation_counts.values,
        title='职业分布',
        orientation='h',
        color=occupation_counts.values,
        color_continuous_scale='Plasma'
    )
    fig_occupation.update_layout(
        yaxis_title="职业",
        xaxis_title="人数"
    )
    st.plotly_chart(fig_occupation, use_container_width=True)

with tab3:
    st.header("收入与消费能力分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 月收入分布
        income_counts = filtered_df['月收入'].value_counts()
        fig_income = px.bar(
            x=income_counts.index,
            y=income_counts.values,
            title='月收入分布',
            color=income_counts.values,
            color_continuous_scale='Blues'
        )
        fig_income.update_layout(
            xaxis_title="月收入范围",
            yaxis_title="人数"
        )
        st.plotly_chart(fig_income, use_container_width=True)
        
        # 收入 vs 教育背景
        income_edu = pd.crosstab(filtered_df['教育背景'], filtered_df['月收入'])
        fig_income_edu = px.imshow(
            income_edu,
            title='教育背景 vs 月收入热力图',
            aspect="auto",
            color_continuous_scale='YlOrRd'
        )
        st.plotly_chart(fig_income_edu, use_container_width=True)
    
    with col2:
        # 收入 vs 职业
        income_occupation = pd.crosstab(filtered_df['职业'], filtered_df['月收入'])
        fig_income_occupation = px.imshow(
            income_occupation,
            title='职业 vs 月收入热力图',
            aspect="auto",
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_income_occupation, use_container_width=True)
        
        # 收入 vs 年龄散点图
        # 为月收入创建数值映射以便绘图
        income_mapping = {
            '<3000': 1500,
            '3000-8000': 5500,
            '8000-15000': 11500,
            '15000-30000': 22500,
            '>30000': 35000
        }
        filtered_df['income_numeric'] = filtered_df['月收入'].map(income_mapping)
        
        fig_income_age = px.scatter(
            filtered_df,
            x='年龄',
            y='income_numeric',
            color='职业',
            title='年龄 vs 月收入分布',
            size='家庭人数',
            hover_data=['教育背景', '婚姻状态']
        )
        fig_income_age.update_layout(
            xaxis_title="年龄",
            yaxis_title="月收入(估算值)"
        )
        st.plotly_chart(fig_income_age, use_container_width=True)

with tab4:
    st.header("地理分布分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 地理散点图
        if '纬度' in filtered_df.columns and '经度' in filtered_df.columns:
            fig_map = px.scatter_geo(
                filtered_df,
                lat='纬度',
                lon='经度',
                color='月收入',
                size='家庭人数',
                hover_name='职业',
                title='客户地理分布',
                projection='natural earth'
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("数据中缺少经纬度信息")
    
    with col2:
        # 邮政编码分布
        if '邮政编码' in filtered_df.columns:
            postal_counts = filtered_df['邮政编码'].value_counts().head(10)
            fig_postal = px.bar(
                x=postal_counts.index.astype(str),
                y=postal_counts.values,
                title='Top 10 邮政编码分布',
                color=postal_counts.values,
                color_continuous_scale='Purples'
            )
            fig_postal.update_layout(
                xaxis_title="邮政编码",
                yaxis_title="客户数量"
            )
            st.plotly_chart(fig_postal, use_container_width=True)
        
        # 家庭人数分布
        family_counts = filtered_df['家庭人数'].value_counts().sort_index()
        fig_family = px.pie(
            values=family_counts.values,
            names=family_counts.index.astype(str) + '人',
            title='家庭人数分布',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_family, use_container_width=True)

with tab5:
    st.header("订单与反馈分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 订单状态分布
        order_counts = filtered_df['订单状态'].value_counts()
        fig_order = px.pie(
            values=order_counts.values,
            names=order_counts.index,
            title='订单状态分布',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_order, use_container_width=True)
        
        # 反馈分布
        feedback_counts = filtered_df['反馈'].value_counts()
        fig_feedback = px.bar(
            x=feedback_counts.index,
            y=feedback_counts.values,
            title='客户反馈分布',
            color=feedback_counts.values,
            color_continuous_scale='RdYlGn'
        )
        fig_feedback.update_layout(
            xaxis_title="反馈类型",
            yaxis_title="数量"
        )
        st.plotly_chart(fig_feedback, use_container_width=True)
    
    with col2:
        # 反馈 vs 收入
        feedback_income = pd.crosstab(filtered_df['反馈'], filtered_df['月收入'])
        fig_feedback_income = px.imshow(
            feedback_income,
            title='反馈 vs 月收入热力图',
            aspect="auto",
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig_feedback_income, use_container_width=True)
        
        # 订单状态 vs 职业
        order_occupation = pd.crosstab(filtered_df['职业'], filtered_df['订单状态'])
        fig_order_occupation = px.imshow(
            order_occupation,
            title='职业 vs 订单状态热力图',
            aspect="auto",
            color_continuous_scale='YlGnBu'
        )
        st.plotly_chart(fig_order_occupation, use_container_width=True)
    
    # 综合分析：不同特征的客户反馈
    st.subheader("多维度客户反馈分析")
    
    analysis_option = st.selectbox(
        "选择分析维度",
        ['职业', '教育背景', '婚姻状态', '月收入']
    )
    
    feedback_cross = pd.crosstab(filtered_df[analysis_option], filtered_df['反馈'], normalize='index') * 100
    fig_feedback_cross = px.bar(
        feedback_cross,
        barmode='stack',
        title=f'{analysis_option} vs 客户反馈分布',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_feedback_cross.update_layout(
        xaxis_title=analysis_option,
        yaxis_title="百分比(%)",
        legend_title="反馈类型"
    )
    st.plotly_chart(fig_feedback_cross, use_container_width=True)

# 侧边栏的额外信息
st.sidebar.markdown("---")
st.sidebar.header("📊 数据统计")
st.sidebar.write(f"总记录数: {len(df)}")
st.sidebar.write(f"筛选后记录数: {len(filtered_df)}")
st.sidebar.write(f"数据完整性: {(len(filtered_df) / len(df) * 100):.1f}%")

# 下载筛选后的数据
st.sidebar.markdown("---")
st.sidebar.header("💾 数据导出")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="下载筛选数据(CSV)",
    data=csv,
    file_name="filtered_food_orders.csv",
    mime="text/csv"
)

# 页脚
st.markdown("---")
st.markdown("### 💡 分析洞察总结")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **👥 客户特征:**
    - 主要年龄分布
    - 性别比例平衡
    - 主要婚姻状态
    - 教育背景构成
    """)

with col2:
    st.info("""
    **💰 收入模式:**
    - 主要收入区间
    - 收入与教育关系
    - 职业收入差异
    - 地域收入分布
    """)

with col3:
    st.info("""
    **📈 业务表现:**
    - 订单完成率
    - 客户满意度
    - 地域覆盖情况
    - 目标客户群体
    """)

st.markdown("---")
st.caption("在线食品订单分析平台 | 基于Streamlit构建")