@echo off
chcp 65001
echo 安装虚拟环境
python -m venv env
echo 激活虚拟环境
call env\Scripts\activate.bat
echo 安装依赖
pip install -r requirements
echo 开始打包
pyinstaller --clean --win-private-assemblies -i images/icon.ico -F yachtDice.py --add-data "audio;audio" --add-data "images;images" --add-data "font;font"
