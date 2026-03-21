#!/usr/bin/env python3
"""
WebUI V3启动脚本
基于ui-ux skill的企业级设计体系
"""
from dotenv import load_dotenv
load_dotenv()

import argparse
from src.webui.interface_v3 import create_ui_v3


def main():
    parser = argparse.ArgumentParser(description="Browser Use WebUI V3 - 企业级界面")
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
    
    print("=" * 80)
    print("🚀 AI浏览器自动化测试平台 - WebUI V3 (企业级)")
    print("=" * 80)
    print(f"主题: {args.theme}")
    print(f"地址: http://{args.server_name}:{args.server_port}")
    if args.share:
        print("分享模式: 已启用")
    print("=" * 80)
    print("\n✨ 全新特性:")
    print("  • 企业级UI/UX设计")
    print("  • 任务历史记录管理")
    print("  • 实时执行监控面板")
    print("  • 配置模板快速切换")
    print("  • 震坤行MCP专属配置")
    print("=" * 80)
    
    demo = create_ui_v3(theme_name=args.theme)
    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        share=args.share,
        show_error=True
    )


if __name__ == "__main__":
    main()
