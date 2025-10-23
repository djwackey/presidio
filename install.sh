#!/bin/bash
# 项目安装和设置脚本
# Project Installation and Setup Script

set -e  # Exit on error

echo "开始安装中文文本脱敏项目..."
echo "Starting installation of Chinese Text Anonymization project..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✓ Python version $python_version is supported"
else
    echo "✗ Python version $python_version is not supported. Minimum required: $required_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "激活虚拟环境..."
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "升级 pip..."
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "安装依赖包..."
echo "Installing dependencies..."
pip install -r requirements.txt

# Download Chinese spaCy model
echo "下载中文 spaCy 模型..."
echo "Downloading Chinese spaCy model..."
python -m spacy download zh_core_web_sm

# Install package in development mode
echo "安装项目包..."
echo "Installing project package..."
pip install -e .

echo ""
echo "✓ 安装完成！"
echo "✓ Installation completed!"
echo ""
echo "运行演示:"
echo "Run demo:"
echo "  source venv/bin/activate"
echo "  python demo_simple.py"
echo "  python main.py"