#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def main():
    """設置 PyPI 和 TestPyPI 認證環境變數"""
    print("這個腳本會幫助您設置用於 twine 上傳的環境變數。")
    print("注意：設置的環境變數只在當前終端會話中有效。\n")
    
    # 詢問是設置 PyPI 還是 TestPyPI
    repo_type = input("您想設置哪個倉庫的認證？(1: PyPI, 2: TestPyPI, 3: 兩者都設置): ")
    
    if repo_type in ['1', '3']:
        print("\n--- PyPI 認證設置 ---")
        pypi_token = input("請輸入您的 PyPI API token: ")
        os.environ['TWINE_USERNAME'] = '__token__'
        os.environ['TWINE_PASSWORD'] = pypi_token
        print("PyPI 認證已設置為環境變數。\n")
        
        # 生成添加到 .bashrc 或 .zshrc 的命令
        print("如果您想永久保存這些設置，請將以下內容添加到您的 .bashrc 或 .zshrc 文件中：")
        print(f'export TWINE_USERNAME=__token__')
        print(f'export TWINE_PASSWORD={pypi_token}')
    
    if repo_type in ['2', '3']:
        print("\n--- TestPyPI 認證設置 ---")
        test_pypi_token = input("請輸入您的 TestPyPI API token: ")
        if repo_type == '2':
            os.environ['TWINE_USERNAME'] = '__token__'
            os.environ['TWINE_PASSWORD'] = test_pypi_token
            os.environ['TWINE_REPOSITORY_URL'] = 'https://test.pypi.org/legacy/'
            print("TestPyPI 認證已設置為環境變數。\n")
            
            # 生成添加到 .bashrc 或 .zshrc 的命令
            print("如果您想永久保存這些設置，請將以下內容添加到您的 .bashrc 或 .zshrc 文件中：")
            print(f'export TWINE_USERNAME=__token__')
            print(f'export TWINE_PASSWORD={test_pypi_token}')
            print('export TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/')
        else:
            print("\n如果您需要上傳到 TestPyPI，請在運行 publish_package.py 之前運行以下命令：")
            print(f'export TWINE_USERNAME=__token__')
            print(f'export TWINE_PASSWORD={test_pypi_token}')
            print('export TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/')
            
    print("\n記得在上傳到 PyPI/TestPyPI 之前運行這些命令或者這個腳本。")
    print("您現在可以運行 publish_package.py 來發布您的包。")

if __name__ == "__main__":
    main()
