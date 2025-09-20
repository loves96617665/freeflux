import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI
import zipfile
import io
import os

# 訪問控制設置
ACCESS_PASSWORD = os.getenv("APP_ACCESS_PASSWORD", "your_password_here")  # 請替換為您的密碼

st.set_page_config(page_title="Flux AI 圖像生成器 (v9)", layout="wide")

# 登錄驗證
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("請輸入訪問密碼以繼續")
    password = st.text_input("訪問密碼", type="password")
    if st.button("登入"):
        if password == ACCESS_PASSWORD:
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("密碼錯誤，請重試")
else:
    st.title("🎨 Flux AI 圖像生成器 (v9) - 會員專區")

    # API 配置區
    st.sidebar.header("API 配置")
    api_key_default = os.getenv("OPENAI_API_KEY", "")
    api_key = st.sidebar.text_input("API Key", value=api_key_default, type="password")
    base_url_default = os.getenv("OPENAI_BASE_URL", "https://api.navy/v1")
    base_url = st.sidebar.text_input("Base URL", value=base_url_default)

    # 模型選擇
    models = [
        "flux.1-schnell", "flux.1.1-por", "flux.latest",
        "flux.1-krea-dev", "flux.1-kontext-pro", "flux.1-kontext-max"
    ]
    model = st.sidebar.selectbox("選擇模型", models, index=0)

    # 根據模型動態配置 style 和 quality
    styles_dict = {
        "flux.1-schnell": [
            "vivid", "natural", "fantasy", "Japanese anime style", "black and white sketch",
            "manga", "watercolor", "pop art", "pixel art", "cyberpunk"
        ],
        "flux.1.1-por": ["cinematic", "photographic", "noir (黑白電影風格)", "vintage anime"],
        "flux.latest": ["modern", "retro", "monochrome", "surrealistic"],
        "flux.1-krea-dev": ["artistic", "minimal", "futuristic", "manga style", "charcoal drawing"],
        "flux.1-kontext-pro": ["professional", "clean", "corporate"],
        "flux.1-kontext-max": ["maximalist", "bold", "creative"]
    }
    qualities_dict = {
