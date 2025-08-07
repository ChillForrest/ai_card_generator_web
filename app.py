import os
import uuid
import gradio as gr
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark  # 火山方舟官方SDK

# 加载 .env 环境变量
load_dotenv()

# 读取API Key
api_key = os.getenv("ARK_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 ARK_API_KEY")

# 初始化火山方舟客户端
client = Ark(api_key=api_key)

# 图片尺寸和输出目录
CARD_SIZE = (800, 500)
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ai_generate_image(prompt):
    try:
        response = client.images.generate(
            model="doubao-seedream-3-0-t2i-250415",  # 图像生成模型，确保你有权限
            prompt=prompt,
            size="800x500",
            n=1
        )
        image_url = response.data[0].url
        img_response = requests.get(image_url)
        return Image.open(BytesIO(img_response.content))
    except Exception as e:
        print(f"❌ 图像生成失败：{e}")
        return None

def ai_generate_text(prompt):
    try:
        completion = client.chat.completions.create(
            model="doubao-1-5-pro-32k-250115",  # 文案生成模型
            messages=[
                {"role": "system", "content": "你是一个专业的文案设计助手"},
                {"role": "user", "content": f"我想设计一个风格为「{prompt}」的名片，请给我一句简短有力的 slogan，以及一句对这个风格的解释"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"⚠️ 文案生成失败：{e}")
        return "⚠️ 无法生成文案"

def generate_card(prompt, name, title, contact):
    image = ai_generate_image(prompt)
    if image is None:
        return "❌ 无法生成图像，请检查提示词或网络连接"

    ai_text = ai_generate_text(prompt)

    # 加载字体
    try:
        font_large = ImageFont.truetype("static/fonts/msyh.ttc", 36)
        font_small = ImageFont.truetype("static/fonts/msyh.ttc", 24)
    except Exception as e:
        print(f"❌ 字体加载失败：{e}")
        return "❌ 字体加载失败，请检查 static/fonts 目录是否存在 msyh.ttc 文件"

    draw = ImageDraw.Draw(image)
    draw.text((30, 30), name, font=font_large, fill=(0, 0, 0))
    draw.text((30, 90), title, font=font_small, fill=(0, 0, 0))
    draw.text((30, 130), contact, font=font_small, fill=(0, 0, 0))
    draw.text((30, 190), ai_text, font=font_small, fill=(50, 50, 50))

    return image

demo = gr.Interface(
    fn=generate_card,
    inputs=[
        gr.Textbox(label="风格提示词（如：未来科技、国风、赛博朋克）"),
        gr.Textbox(label="姓名"),
        gr.Textbox(label="职位 / 称谓"),
        gr.Textbox(label="联系方式")
    ],
    outputs=gr.Image(label="生成的名片"),
    title="🎨 AI 图像风格名片生成器",
    description="输入姓名、风格提示词等，自动生成专属名片图像与文案，基于火山方舟 Doubao 模型"
)

if __name__ == "__main__":
    demo.launch()
