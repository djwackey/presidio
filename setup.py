from setuptools import setup, find_packages

setup(
    name="presidio-chinese-anonymizer",
    version="1.0.0",
    description="中文文本脱敏工具 - Chinese Text Anonymization Tool using Presidio",
    author="",
    packages=find_packages(),
    install_requires=[
        "presidio-analyzer>=2.2.33",
        "presidio-anonymizer>=2.2.33", 
        "spacy>=3.4.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)