#!/usr/bin/env python3
"""
优化后的WebUI启动脚本
使用左侧导航栏设计 - 完全优化版
"""
import argparse
from src.webui.interface_v2_optimized import create_ui_v2


def main():
    parser = argparse.ArgumentParser(description="Browser Use WebUI V2 - 完全优化版")
    parser.add_argument(
        "--theme",
        type=str,
        default="Soft",
        choices=["Default", "Soft", "Monochrome", "Glass", "Origin", "Citrus", "Ocean", "Base"],
        help="Gradio主题选择"
    )
    parser.add_argument(
        "--server-name",
        type=str,
        default="0.0.0.0",
        help="服务器地址"
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=7860,
        help="服务器端口"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="创建公共分享链接"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🌐 AI测试平台 - Browser Use WebUI V2 (完全优化版)")
    print("=" * 60)
    print(f"主题: {args.theme}")
    print(f"地址: http://{args.server_name}:{args.server_port}")
    if args.share:
        print("分享模式: 已启用")
    print("=" * 60)
    
    demo = create_ui_v2(theme_name=args.theme)
    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        share=args.share,
        show_error=True
    )


if __name__ == "__main__":
    main()
