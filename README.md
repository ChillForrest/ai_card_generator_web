# ai_card_generator_web
Just a sxxt program


├── ai_card_generator_web/
│   ├── app.py                         # 主程序（Flask / Gradio Web 服务）
│   ├── generator/
│   │   ├── __init__.py
│   │   ├── text_gen.py               # 调用 GPT/Claude 生成文案
│   │   ├── bg_gen.py                 # 调用 Stable Diffusion 接口生成背景图
│   │   └── image_compose.py          # 用 Pillow 合成文字与背景图
│   ├── static/
│   │   ├── fonts/                     # 存放字体（如微软雅黑.ttf）
│   │   ├── templates/                 # 可选：如果用 Flask，则放 HTML 模板
│   │   └── backgrounds/               # 预置/备用背景图
│   ├── output/
│   │   └── card_xxx.png              # 输出生成的名片图片
│   ├── templates/                    # Gradio 模板 / 前端页面配置（可选）
│   ├── requirements.txt              # 依赖包清单
│   └── config.py                     # 配置项（API密钥、输出大小、路径）

# Git 分支建议：

main                 # 主分支，部署稳定版本
frontend             # 前端优化版分支（美化UI、响应式等）
local-test           # 用于本地Pillow图像调试测试的分支
cloud-deploy         # 部署到Replit / 腾讯云的部署脚本分支
printer-support      # 加入打印机支持（热敏 / 彩打）专用分支

# requirements.txt 示例
openai
replicate
Pillow
gradio
requests
python-dotenv       # 用于管理 API Key 等环境变量

# config.py 示例
OUTPUT_DIR = "output"
FONT_PATH = "static/fonts/msyh.ttc"
CARD_SIZE = (800, 500)
OPENAI_API_KEY = "your-openai-key"
REPLICATE_API_TOKEN = "your-token"
