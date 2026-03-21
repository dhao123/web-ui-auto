"""
Enterprise-grade WebUI for Browser Agent
企业级浏览器代理Web界面

这是一个全新的企业级界面入口，完全复用现有业务逻辑，但提供更专业、美观的视觉体验。
"""

from dotenv import load_dotenv
load_dotenv()

import argparse
from src.webui.enterprise_interface import create_enterprise_ui


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise WebUI for Browser Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python webui_enterprise.py --ip 0.0.0.0 --port 7888
  python webui_enterprise.py --theme dark
        """
    )
    parser.add_argument(
        "--ip", 
        type=str, 
        default="127.0.0.1", 
        help="绑定的IP地址 (默认: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=7888, 
        help="监听端口 (默认: 7888)"
    )
    parser.add_argument(
        "--theme",
        type=str,
        default="auto",
        choices=["light", "dark", "auto"],
        help="主题模式 (默认: auto)"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="zh",
        choices=["zh", "en"],
        help="界面语言 (默认: zh)"
    )
    
    args = parser.parse_args()

    demo = create_enterprise_ui(theme_mode=args.theme, lang=args.lang)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                   🌐 Browser Agent Enterprise                 ║
║                        企业级智能浏览器平台                    ║
╠══════════════════════════════════════════════════════════════╣
║  🚀 服务地址: http://{args.ip}:{args.port:<5}                    ║
║  🎨 主题模式: {args.theme:<10}                                  ║
║  🌐 界面语言: {'中文' if args.lang == 'zh' else 'English':<10}              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    demo.queue(max_size=100).launch(
        server_name=args.ip,
        server_port=args.port,
        show_error=True,
        show_api=False,
        quiet=True,
    )


if __name__ == '__main__':
    main()
