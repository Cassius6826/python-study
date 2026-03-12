# 文件名：03_app.py
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(page_title="智能食谱推荐系统", page_icon="🥗", layout="wide")

st.title("🥗 AI 智能食谱推荐与营养搭配系统")
st.markdown("**项目说明：** 本系统结合食品营养学与 NLP 算法，为您提供个性化饮食方案。")

# ==========================================
# 2. 核心逻辑类
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("recipes.csv")
        # 简单清洗
        df['Tags'] = df['Tags'].fillna('')
        df['combined_features'] = df['Recipe_Name'] + " " + df['Tags']
        return df
    except FileNotFoundError:
        return pd.DataFrame()

class UserProfile:
    def __init__(self, gender, age, height, weight, activity_level, goal):
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.goal = goal

    def calculate_bmr(self):
        if self.gender == '男':
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161

    def calculate_daily_calories(self):
        bmr = self.calculate_bmr()
        tdee = bmr * self.activity_level
        if self.goal == '减脂': return tdee - 500
        elif self.goal == '增肌': return tdee + 500
        else: return tdee

# ==========================================
# 3. 侧边栏：用户输入
# ==========================================
with st.sidebar:
    st.header("📝 用户档案录入")
    
    st.subheader("1. 身体数据")
    # key参数是可选的，但为了防止报错，Streamlit内部会自动处理，只要不写两遍同样的代码就不会冲突
    gender = st.selectbox("性别", ["男", "女"])
    age = st.number_input("年龄 (岁)", 10, 100, 25)
    height = st.number_input("身高 (cm)", 100, 250, 175)
    weight = st.number_input("体重 (kg)", 30, 150, 70)
    
    st.divider() 
    
    st.subheader("2. 目标设定")
    activity_map = {
        "久坐不动 (1.2)": 1.2,
        "轻度运动 (1.375)": 1.375,
        "中度运动 (1.55)": 1.55,
        "高强度运动 (1.725)": 1.725
    }
    activity_key = st.selectbox("日常活动量", list(activity_map.keys()))
    activity_level = activity_map[activity_key]
    goal = st.radio("您的目标", ["减脂", "维持", "增肌"])

# ==========================================
# 4. 主界面逻辑
# ==========================================
df = load_data()

if df.empty:
    st.error("❌ 未检测到数据，请先运行 01_generate_data.py 生成新数据！")
    st.stop()

# --- A. 健康画像 ---
st.divider()
st.header("📊 第一步：健康画像分析")
user = UserProfile(gender, age, height, weight, activity_level, goal)
bmr = user.calculate_bmr()
daily_cal = user.calculate_daily_calories()

col1, col2, col3 = st.columns(3)
col1.metric("基础代谢 (BMR)", f"{int(bmr)} kcal")
col2.metric("每日推荐摄入 (TDEE)", f"{int(daily_cal)} kcal", help="根据您的目标已调整热量")
col3.metric("当前目标", goal)

# --- B. 智能筛选 ---
st.divider()
st.header("🍽️ 第二步：基于营养学的智能筛选")
st.write("系统根据您的热量预算，自动过滤不符合要求的菜品。")

target_cal = daily_cal * 0.4
st.info(f"💡 建议您这一餐摄入约 **{int(target_cal)} kcal**")

# 滑动条
cal_range = st.slider("🔍 调整热量筛选范围", 0, 1500, (int(target_cal)-100, int(target_cal)+100))

# 筛选
filtered_df = df[(df['Calories'] >= cal_range[0]) & (df['Calories'] <= cal_range[1])]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[['Recipe_Name', 'Calories', 'Protein', 'Tags']].sort_values(by='Protein', ascending=False).head(10),
        use_container_width=True
    )
    st.caption(f"共找到 {len(filtered_df)} 道符合热量的菜品，按蛋白质含量排序。")
else:
    st.warning("在此热量范围内未找到匹配菜品，请尝试扩大范围。")

# --- C. AI 多维推荐 (升级版) ---
st.divider()
st.header("🤖 第三步：AI 综合口味推荐 (多选)")
st.markdown("请选择 **1道或多道** 您平时喜欢的菜，系统将计算您的**口味偏好向量**，推荐相似美食。")

col_a, col_b = st.columns([2, 1])

with col_a:
    all_dishes = df['Recipe_Name'].unique().tolist()
    # 默认值做个检查，防止报错
    default_opts = all_dishes[:2] if len(all_dishes) >=2 else all_dishes
    selected_dishes = st.multiselect("请选择您喜欢的菜品 (支持多选/搜索):", all_dishes, default=default_opts)

with col_b:
    st.write("") 
    st.write("") 
    btn_predict = st.button("🚀 开始 AI 运算", type="primary")

if btn_predict and selected_dishes:
    # 1. 初始化 TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    # 2. 获取用户选择的菜品的索引
    selected_indices = [df[df['Recipe_Name'] == dish].index[0] for dish in selected_dishes]
    
    # 3. 计算用户画像向量
    user_profile_vector = tfidf_matrix[selected_indices].sum(axis=0)
    
    # 4. 计算综合向量与所有菜品的相似度
    cosine_sim = cosine_similarity(np.asarray(user_profile_vector), tfidf_matrix)
    
    # 5. 排序取出前 N 个
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    recommendations = []
    for i, score in sim_scores:
        dish_name = df.iloc[i]['Recipe_Name']
        if dish_name not in selected_dishes:
            recommendations.append((df.iloc[i], score))
        if len(recommendations) >= 5: 
            break
            
    # 6. 展示结果
    tag_preview = df.iloc[selected_indices[0]]['Tags'].split(',')[0] if df.iloc[selected_indices[0]]['Tags'] else "风味"
    st.success(f"基于您喜欢的 {len(selected_dishes)} 道菜，AI 分析您的口味偏好为：**{tag_preview}...**")
    
    rec_cols = st.columns(len(recommendations))
    for idx, (row, score) in enumerate(recommendations):
        with rec_cols[idx]:
            st.markdown(f"**Top {idx+1}**")
            st.write(f"🍲 **{row['Recipe_Name']}**")
            st.caption(f"热量: {row['Calories']} | 相似度: {int(score*100)}%")
            st.progress(min(score, 1.0)) 

elif btn_predict and not selected_dishes:
    st.warning("⚠️ 请至少选择一道您喜欢的菜！")

# --- D. 可视化 ---
st.divider()
st.header("📈 食材库分布概览")
with st.expander("点击展开查看图表"):
    tab1, tab2 = st.tabs(["热量分布", "蛋白-热量关系"])
    with tab1:
        fig1, ax1 = plt.subplots()
        sns.histplot(df['Calories'], kde=True, ax=ax1, color="orange")
        st.pyplot(fig1)
    with tab2:
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=df, x='Calories', y='Protein', hue='Tags', legend=False, ax=ax2)
        st.pyplot(fig2)