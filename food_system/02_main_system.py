# 文件名：02_main_system.py
import pandas as pd

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load_data(self):
        try:
            # 读取CSV文件
            self.data = pd.read_csv(self.filepath)
            print("数据加载成功！")
            self.data = self.data[self.data['Calories'] > 0] 
            return self.data
        except FileNotFoundError:
            print("未找到文件，请先运行 01_generate_data.py")
            return None
# 测试
if __name__ == "__main__":
    loader = DataLoader("recipes.csv")
    df = loader.load_data()
    print(df.head()) # 打印前5行看看

class UserProfile:
    def __init__(self, gender, age, height, weight, activity_level, goal):
        """
        初始化用户信息
        :param gender: 'male' or 'female'
        :param age: 年龄
        :param height: 身高 (cm)
        :param weight: 体重 (kg)
        :param activity_level: 运动系数 (1.2 - 1.9)
        :param goal: 'lose' (减脂), 'maintain' (维持), 'gain' (增肌)
        """
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.goal = goal

    def calculate_bmr(self):
        """
        计算基础代谢率BMR
        """
        if self.gender == 'male':
            # 男性公式: (10 × weight) + (6.25 × height) - (5 × age) + 5
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            # 女性公式: (10 × weight) + (6.25 × height) - (5 × age) - 161
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161

    def calculate_daily_calories(self):
        """
        计算每日总能量消耗 (TDEE) 并根据目标调整
        """
        bmr = self.calculate_bmr()
        tdee = bmr * self.activity_level # 每日总消耗
        # 根据目标调整热量摄入
        if self.goal == 'lose':
            return tdee - 500  # 制造热量缺口
        elif self.goal == 'gain':
            return tdee + 500  # 热量盈余
        else:
            return tdee

class RecipeRecommender:
    def __init__(self, recipes_df):
        self.recipes_df = recipes_df

    def recommend_by_calories(self, target_calories, tolerance=100):
        """
        简单推荐：寻找热量在目标范围内的食物
        :param target_calories: 这一餐的目标热量
        :param tolerance: 容差范围 (+- 100卡)
        """
        min_cal = target_calories - tolerance
        max_cal = target_calories + tolerance

        result = self.recipes_df[
            (self.recipes_df['Calories'] >= min_cal) & 
            (self.recipes_df['Calories'] <= max_cal)
        ]

        result = result.sort_values(by='Protein', ascending=False)
        
        return result


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class AIRecommender:
    def __init__(self, df):
        self.df = df
        self.tfidf_matrix = None
        self.tfidf = None
        self._prepare_model()

    def _prepare_model(self):
        """
        模型训练过程：
        1. 将菜名和标签合并成一个字符串，作为“特征文本”。
        2. 使用TF-IDF将文本转换为向量矩阵。
        """
        # 填充空值，防止报错
        self.df['Tags'] = self.df['Tags'].fillna('')
        # 组合特征：菜名 + 标签 (例如："宫保鸡丁 高蛋白 辣")
        self.df['combined_features'] = self.df['Recipe_Name'] + " " + self.df['Tags']
        
        # 初始化TF-IDF向量化器 (这是机器学习的核心步骤)
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        # 训练模型：将文本转换为数字矩阵
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['combined_features'])
        print("✅ AI推荐模型构建完成！")

    def get_recommendations(self, dish_name, top_n=3):
        """
        核心功能：根据一道菜，推荐相似的菜
        """
        # 1. 找到这道菜在数据表中的索引
        try:
            idx = self.df[self.df['Recipe_Name'] == dish_name].index[0]
        except IndexError:
            return f"找不到菜品：{dish_name}"

        # 2. 计算这道菜与其他所有菜的相似度 (余弦相似度)
        # linear_kernel 在这里等同于计算余弦相似度，速度更快
        cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

        # 3. 获取相似度分数列表
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 4. 按相似度得分从高到低排序
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 5. 取前 N 个 (排除掉它自己，即第0个)
        sim_scores = sim_scores[1:top_n+1]
        
        # 6. 返回结果
        dish_indices = [i[0] for i in sim_scores]
        return self.df.iloc[dish_indices][['Recipe_Name', 'Tags', 'Calories']]


# ==========================================
# 模块五：数据可视化与分析
# 对应作业要求：【了解数据可视化的基本流程】
# ==========================================
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data(df):
    """
    绘制两个关键图表用于报告
    """
    # 设置绘图风格
    sns.set(style="whitegrid")
    
    # 图表1：卡路里分布直方图
    plt.figure(figsize=(10, 5))
    sns.histplot(df['Calories'], bins=20, kde=True, color='skyblue')
    plt.title('Calorie Distribution of Recipes (卡路里分布)', fontsize=15)
    plt.xlabel('Calories (kcal)')
    plt.ylabel('Count')
    # 保存图片，方便插入Word报告
    plt.savefig('calorie_dist.png') 
    print("📊 图表1已生成：calorie_dist.png")

    # 图表2：蛋白质 vs 热量 散点图 (区分标签)
    plt.figure(figsize=(10, 5))
    # 为了图表好看，我们只取包含"高蛋白"或"低脂"标签的数据画图
    sample_data = df[df['Tags'].str.contains('高蛋白|低脂', na=False)]
    
    if not sample_data.empty:
        sns.scatterplot(data=sample_data, x='Calories', y='Protein', hue='Tags', s=100, alpha=0.7)
        plt.title('Protein vs Calories (蛋白质与热量关系)', fontsize=15)
        plt.savefig('protein_calories.png')
        print("图表2已生成：protein_calories.png")
    
    # 这一步是为了防止在某些环境下弹窗卡住代码，我们只保存不显示，或者手动关闭
    # plt.show()


if __name__ == "__main__":
    print("Starting System...")
    
    # 1. 加载数据
    loader = DataLoader("recipes.csv")
    df = loader.load_data()
    
    # 2. 建立用户画像
    my_user = UserProfile(gender='female', age=30, height=165, weight=55, activity_level=1.375, goal='maintain')
    daily_calories = my_user.calculate_daily_calories()
    print(f"\n[用户分析] 基础代谢: {my_user.calculate_bmr():.1f}, 推荐日摄入: {daily_calories:.1f} kcal")

    # 3. 基础推荐 (逻辑筛选)
    print("\n[阶段一] 正在进行基础营养筛选...")
    recommender = RecipeRecommender(df)
    # 假设晚餐吃 30% 的热量
    dinner_cal = daily_calories * 0.3
    base_rec = recommender.recommend_by_calories(dinner_cal)
    print(f"为您筛选出热量在 {int(dinner_cal)} kcal 左右的晚餐：")
    print(base_rec[['Recipe_Name', 'Calories', 'Tags']].head(3))

    # 4. AI 进阶推荐 (内容相似度)
    print("\n[阶段二] 启动AI推荐引擎 (猜你喜欢)...")
    ai_rec = AIRecommender(df)
    
    # 假设用户喜欢列表里的第一道菜，我们基于它推荐相似的
    if not base_rec.empty:
        liked_dish = base_rec.iloc[0]['Recipe_Name']
        print(f"假设用户喜欢：【{liked_dish}】，基于此推荐相似菜品：")
        
        similar_dishes = ai_rec.get_recommendations(liked_dish)
        print(similar_dishes)
    
    # 5. 生成分析图表
    print("\n[阶段三] 生成可视化报告...")
    visualize_data(df)
    print("所有任务执行完毕。")