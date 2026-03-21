"""
Web UI React 版本启动入口
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def main():
    """启动React前端和FastAPI后端"""
    project_root = Path(__file__).parent
    frontend_dir = project_root / "frontend"
    
    print("=" * 60)
    print("  AI Browser Automation - React Web UI")
    print("=" * 60)
    
    # 检查前端是否已构建
    if not (frontend_dir / "dist").exists():
        print("\n[INFO] 前端尚未构建，正在构建...")
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"[ERROR] 前端构建失败: {result.stderr}")
            sys.exit(1)
        print("[INFO] 前端构建完成")
    
    # 启动FastAPI后端
    print("\n[INFO] 启动后端服务...")
    print("[INFO] API服务地址: http://localhost:8000")
    print("[INFO] 前端访问地址: http://localhost:8000")
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        # 使用uvicorn启动
        import uvicorn
        from src.api.main import app
        
        # 延迟打开浏览器
        import threading
        def open_browser():
            import time
            time.sleep(2)
            webbrowser.open("http://localhost:8000")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except ImportError:
        print("[ERROR] 请安装uvicorn: pip install uvicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] 服务已停止")

if __name__ == "__main__":
    main()
