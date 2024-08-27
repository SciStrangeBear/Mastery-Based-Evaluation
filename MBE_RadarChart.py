import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# 设置页面标题
st.title("Radar Chart of Mastery Levels")

# 创建左右两列布局
col1, col2 = st.columns([1, 2])  # 比例可以根据需要调整

with col1:
    # 1. Widget部分

    # 创建两个输入框，让用户输入评价项目和对应的评分
    evaluation_items = st.text_area("Please enter Learning Outcomes (one per line):").splitlines()
    scores = st.text_area("Please enter mastery levels in number(one per line)：").splitlines()

    # 增加一个滑动条来控制图片大小
    fig_size = st.slider("Size of the Chart", min_value=2, max_value=6, value=4, step=1)

    # 创建一个生成按钮，当用户点击按钮时，触发后续的代码
    generate_button = st.button("Generate")

with col2:
    if generate_button:
        # 2. 数据处理部分

        # 将用户输入的评分转换为数值类型
        scores = [float(score) for score in scores]

        # 创建一个数据框来存储评价项目和对应的评分
        data = pd.DataFrame({
            'LOs': evaluation_items,
            'Scores': scores
        })

        # 3. 作图部分

        # 设置雷达图的角度
        angles = np.linspace(0, 2 * np.pi, len(evaluation_items), endpoint=False).tolist()

        # 为了使雷达图闭合，重复第一个角度和评分
        scores += scores[:1]
        angles += angles[:1]

        # 开始绘制雷达图
        fig, ax = plt.subplots(figsize=(fig_size, fig_size), subplot_kw=dict(polar=True))

        # 画出雷达图的线条和填充区域
        ax.fill(angles, scores, color='b', alpha=0.25)
        ax.plot(angles, scores, color='b', linewidth=2)

        # 添加评价项目的标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(data['LOs'])

        # 显示图形
        st.pyplot(fig)

        # 4. 保存图片并创建下载按钮

        # 将图像保存为字节流
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)

        # 创建下载按钮
        st.download_button(
            label="Download",
            data=img_buffer,
            file_name="radar_chart.png",
            mime="image/png"
        )
