"""
动画效果 - @keyframes 定义
"""


def get_animation_styles() -> str:
    """获取所有动画效果样式"""
    return """
    /* === 微光动画 - 侧边栏顶部装饰条 === */
    @keyframes shimmer {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }

    /* === 涟漪动画 - 导航选中状态 === */
    @keyframes ripple {
        0%, 100% {
            opacity: 0.3;
        }
        50% {
            opacity: 0.6;
        }
    }

    /* === 边框发光动画 - 欢迎卡片 === */
    @keyframes borderGlow {
        0%, 100% {
            opacity: 0.6;
            filter: brightness(1);
        }
        50% {
            opacity: 1;
            filter: brightness(1.2);
        }
    }

    /* === 标题脉冲动画 - 欢迎卡片标题 === */
    @keyframes titlePulse {
        0%, 100% {
            filter: brightness(1);
        }
        50% {
            filter: brightness(1.1);
        }
    }

    /* === 淡入动画 === */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* === 淡出动画 === */
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }

    /* === 缩放进入动画 === */
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* === 滑入动画 - 从左侧 === */
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* === 滑入动画 - 从右侧 === */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* === 滑入动画 - 从底部 === */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* === 旋转动画 - 加载指示器 === */
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    /* === 弹跳动画 === */
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
    }

    /* === 闪烁动画 === */
    @keyframes blink {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    /* === 脉冲动画 === */
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 var(--primary-alpha);
        }
        70% {
            transform: scale(1.02);
            box-shadow: 0 0 0 10px rgba(103, 107, 239, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(103, 107, 239, 0);
        }
    }

    /* === 骨架屏加载动画 === */
    @keyframes skeleton {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }

    /* === 渐变移动动画 === */
    @keyframes gradientMove {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    /* === 动画应用类 === */
    .animate-fade-in {
        animation: fadeIn var(--transition-normal) var(--ease-default) forwards;
    }

    .animate-fade-out {
        animation: fadeOut var(--transition-normal) var(--ease-default) forwards;
    }

    .animate-scale-in {
        animation: scaleIn var(--transition-normal) var(--ease-default) forwards;
    }

    .animate-slide-in-left {
        animation: slideInLeft var(--transition-normal) var(--ease-default) forwards;
    }

    .animate-slide-in-right {
        animation: slideInRight var(--transition-normal) var(--ease-default) forwards;
    }

    .animate-slide-in-up {
        animation: slideInUp var(--transition-normal) var(--ease-default) forwards;
    }

    .animate-spin {
        animation: spin 1s linear infinite;
    }

    .animate-bounce {
        animation: bounce 1s var(--ease-default) infinite;
    }

    .animate-pulse {
        animation: pulse 2s var(--ease-default) infinite;
    }

    .animate-blink {
        animation: blink 1.5s var(--ease-default) infinite;
    }

    /* === 骨架屏样式 === */
    .skeleton {
        background: linear-gradient(
            90deg,
            var(--bg-hover) 25%,
            var(--border-light) 50%,
            var(--bg-hover) 75%
        );
        background-size: 200px 100%;
        animation: skeleton 1.5s ease-in-out infinite;
        border-radius: var(--radius-sm);
    }

    .skeleton-text {
        height: 1em;
        margin: 0.5em 0;
    }

    .skeleton-title {
        height: 1.5em;
        width: 60%;
        margin-bottom: 1em;
    }

    .skeleton-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
    }

    .skeleton-rect {
        height: 100px;
    }

    /* === 过渡效果增强 === */
    .transition-all {
        transition: all var(--transition-normal) var(--ease-default) !important;
    }

    .transition-fast {
        transition: all var(--transition-fast) var(--ease-default) !important;
    }

    .transition-slow {
        transition: all var(--transition-slow) var(--ease-default) !important;
    }

    /* === 悬停效果增强 === */
    .hover-lift:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    .hover-scale:hover {
        transform: scale(1.02);
    }

    .hover-glow:hover {
        box-shadow: var(--shadow-primary-sm);
    }
    """
