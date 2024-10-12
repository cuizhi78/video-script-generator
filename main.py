import streamlit as st
from utils import generate_script
import openai
import requests

st.set_page_config(
    page_title="视频脚本生成器",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="auto",
)

# 初始化按钮状态
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

# 初始化提交状态
if 'submit' not in st.session_state:
    st.session_state.submit = False


def on_click():
    st.session_state.button_disabled = True
    st.session_state.submit = True


st.title("🎬视频脚本生成器")

with st.sidebar:
    openai_api_key = st.text_input(
        "请输入API密钥：",
        type="password",
        value="")
    st.markdown("[获取API密钥](#)")

subject = st.text_input("💡 请输入视频主题：")
search_info = st.text_area("🔎 请输入辅助信息：", max_chars=300)
video_length = st.number_input("⏰ 请输入视频时长（单位：分钟）：", min_value=1, max_value=2, step=1, value=1)
creativity = st.slider(
    "🎨 请输入视频脚本的创造力（数字越小越严谨，反之更多样）：",
    min_value=0.1,
    max_value=1.0,
    step=0.1,
    value=0.7
)

# **在渲染按钮之前处理提交逻辑**
if st.session_state.submit:
    # 验证输入
    if not openai_api_key:
        st.error("请输入API密钥")
    elif not subject:
        st.error("请输入视频主题")
    elif not video_length >= 0.1:
        st.error("请输入视频时长并不能小于0.1")
    else:
        with st.spinner("AI正在生成视频脚本，请稍等..."):
            # 调用您的 generate_script 函数
            try:
                title, script = generate_script(subject, search_info, video_length, creativity, openai_api_key)
            except openai.AuthenticationError:
                st.error("认证错误：请检查您的 OpenAI API 密钥是否正确。")
            except openai.RateLimitError:
                st.error("请求太频繁：请稍后再试。")
            except requests.exceptions.RequestException as e:
                st.error(f"网络请求错误：{e}")
            except Exception as e:
                st.error(f"发生未知错误：{e}")
            else:
                st.success("视频脚本生成成功")
                st.subheader("🔥 视频标题：")
                st.info(title)
                st.subheader("📝 视频脚本：")
                st.info(script)

                with st.expander("🧰 辅助信息："):
                    st.info(search_info)

    # **提交处理完毕，重置按钮状态和提交状态**
    st.session_state.button_disabled = False
    st.session_state.submit = False

# **渲染按钮**
st.button("🎮 生成视频脚本", on_click=on_click, disabled=st.session_state.button_disabled)
