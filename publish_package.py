#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

def run_command(command):
    """執行命令並打印輸出"""
    print(f"執行: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(f"錯誤: {result.stderr}")
    if result.returncode != 0:
        print(f"命令執行失敗，退出碼: {result.returncode}")
        sys.exit(1)
    return result

def check_pypi_credentials():
    """檢查 PyPI 認證信息"""
    print("\n檢查 PyPI 認證環境變數...")
    
    # 檢查 TWINE_USERNAME 和 TWINE_PASSWORD 是否已設置
    username = os.environ.get('TWINE_USERNAME')
    password = os.environ.get('TWINE_PASSWORD')
    
    if not username or not password:
        print("沒有找到 TWINE_USERNAME 或 TWINE_PASSWORD 環境變數")
        print("您可以設置以下環境變數以避免手動輸入認證信息:")
        print("  export TWINE_USERNAME=__token__")
        print("  export TWINE_PASSWORD=your_api_token")
        print("\n對於 TestPyPI，您可能需要單獨的 token。")
        print("如果您需要為 TestPyPI 設置不同的認證信息，可以臨時設置這些環境變數:")
        print("  export TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/")
        print("  export TWINE_USERNAME=__token__")
        print("  export TWINE_PASSWORD=your_testpypi_token")
        
        return False
    
    print("已找到 PyPI 認證環境變數")
    return True

def main():
    """主函數：發布包到PyPI"""
    print("準備發布包到PyPI...")
    
    # 檢查認證信息
    has_credentials = check_pypi_credentials()
    if not has_credentials:
        print("\n警告: 未找到環境變數中的認證信息，您可能需要在上傳過程中手動輸入。")
        proceed = input("是否繼續? (y/n): ")
        if proceed.lower() != 'y':
            print("取消發布過程。")
            sys.exit(0)
    
    # 顯示當前環境變數設置
    print("\n當前環境變數設置:")
    for env_var in ['TWINE_USERNAME', 'TWINE_PASSWORD', 'TWINE_REPOSITORY_URL']:
        if env_var in os.environ:
            if env_var == 'TWINE_PASSWORD':
                print(f"{env_var}: ***已設置***")
            else:
                print(f"{env_var}: {os.environ[env_var]}")
        else:
            print(f"{env_var}: 未設置")
    
    # 清理舊的構建文件
    print("\n清理舊的構建文件...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    for item in os.listdir("."):
        if item.endswith(".egg-info"):
            shutil.rmtree(item)
    
    # 構建包
    print("\n構建包...")
    run_command("python setup.py sdist bdist_wheel")
    
    # 檢查包
    print("\n檢查包...")
    run_command("twine check dist/*")
    
    # 詢問是否上傳到TestPyPI
    test_pypi = input("\n是否要上傳到TestPyPI? (y/n): ")
    if test_pypi.lower() == 'y':
        print("\n上傳到TestPyPI...")
        # 使用環境變數指定 TestPyPI 的 URL
        cmd = "twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
        run_command(cmd)
        print("可以使用以下命令安裝測試版本:")
        print("pip install --index-url https://test.pypi.org/simple/ hackmd_mcp")
    
    # 詢問是否上傳到PyPI
    pypi = input("\n是否要上傳到PyPI? (y/n): ")
    if pypi.lower() == 'y':
        print("\n上傳到PyPI...")
        run_command("twine upload dist/*")
        print("包已成功上傳到PyPI!")
        print("可以使用以下命令安裝: pip install hackmd_mcp")
    else:
        print("取消上傳到PyPI。")
    
    print("\n完成!")

if __name__ == "__main__":
    main()
