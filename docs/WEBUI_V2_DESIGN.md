# WebUI V2 设计文档

## 设计理念

WebUI V2 基于 `.kiro/skills/ui-ux` 中的专业UI/UX设计规范，采用现代化的左侧导航栏布局，提供更好的用户体验和视觉一致性。

## 布局架构

### 整体布局

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  ┌──────────┐  ┌──────────────────────────────────────────┐ │
│  │          │  │         Header Area                       │ │
│  │          │  │  ┌────────────────────────────────────┐  │ │
│  │          │  │  │ 🤖 Run Agent                       │  │ │
│  │  Left    │  │  │ 智能浏览器自动化测试平台            │  │ │
│  │  Sidebar │  │  └────────────────────────────────────┘  │ │
│  │          │  ├──────────────────────────────────────────┤ │
│  │  Nav     │  │                                          │ │
│  │          │  │         Main Content Area                │ │
│  │          │  │                                          │ │
│  │          │  │  ┌────────────────────────────────────┐ │ │
│  │          │  │  │                                    │ │ │
│  │          │  │  │     Content Cards                  │ │ │
│  │          │  │  │                                    │ │ │
│  │          │  │  └────────────────────────────────────┘ │ │
│  │          │  │                                          │ │
│  └──────────┘  └──────────────────────────────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 尺寸规范

| 区域 | 宽度 | 高度 | 说明 |
|------|------|------|------|
| 左侧导航栏 | 220px | 100vh | 固定宽度，全屏高度 |
| 右侧内容区 | flex: 1 | 100vh | 自适应宽度 |
| Header区域 | 100% | auto | 自适应高度 |
| 主内容区 | 100% | calc(100vh - header) | 可滚动 |
| 内容区内边距 | 40px | - | 左右内边距 |

## 左侧导航栏设计

### Logo区域
```
┌──────────────────┐
│                  │
│  🌐 AI测试平台    │
│  Browser Use     │
│     WebUI        │
│                  │
└──────────────────┘
```

- 居中对齐
- 品牌渐变色文字
- 底部分割线

### 导航菜单

```
┌──────────────────┐
│ ⚙️ Agent Settings │  ← 普通状态
├──────────────────┤
│ 🌐 Browser Settings│
├──────────────────┤
│ 🤖 Run Agent     │  ← 激活状态 (蓝紫色背景)
├──────────────────┤
│ 🎁 Agent Marketplace│
├──────────────────┤
│ 📁 Load & Save Config│
└──────────────────┘
```

#### 菜单项状态

**普通状态**
- 背景: 透明
- 文字: #333333
- 图标: 18px
- 内边距: 12px 16px
- 圆角: 8px

**悬停状态**
- 背景: #F5F7FF (浅蓝色)
- 文字: #4F4FF6 (蓝紫色)

**激活状态**
- 背景: #E6E9FD (蓝紫色背景)
- 文字: #4F4FF6 (蓝紫色)
- 字重: 600

## 右侧内容区设计

### Header区域

```
┌────────────────────────────────────────────────────────┐
│  🤖 Run Agent                                          │
│  智能浏览器自动化测试平台 | Control your browser...    │
└────────────────────────────────────────────────────────┘
```

- 背景: 白色
- 内边距: 20px 40px
- 底部边框: 1px solid #D7DEF4
- 阴影: 0 2px 8px rgba(0,0,0,0.05)

#### 标题样式
- 字体大小: 24px
- 字重: 700
- 颜色: #333333
- 底部间距: 8px

#### 副标题样式
- 字体大小: 14px
- 颜色: #545E74

### 主内容区

```
┌────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────┐ │
│  │                                                  │ │
│  │  Content Card                                    │ │
│  │                                                  │ │
│  │  ┌────────────────────────────────────────────┐ │ │
│  │  │                                            │ │ │
│  │  │  Form / Table / Content                    │ │ │
│  │  │                                            │ │ │
│  │  └────────────────────────────────────────────┘ │ │
│  │                                                  │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Another Card                                    │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

- 内边距: 24px 40px
- 可滚动: overflow-y: auto
- 背景: #F1F3FA

## 卡片组件设计

### 内容卡片

```css
.content-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}
```

### 统计卡片

```
┌─────────────────────────┐
│ │ 状态                  │  ← 左侧彩色边框
│ │                       │
│ │ 执行统计              │  ← 标签
│ │                       │
│ │ 42                    │  ← 数值
│ │                       │
└─────────────────────────┘
```

**样式规范**
- 左侧边框: 4px solid
- 边框颜色: 
  - 默认: #676BEF
  - 成功: #52c41a
  - 警告: #faad14
  - 信息: #1890ff
- 悬停效果: 上浮2px + 阴影加深

## 色彩系统

### 品牌色

```css
/* 主品牌色 - 渐变 */
background: linear-gradient(to right, #3462FE, #9D34FE);

/* 主色调 */
--primary: #676BEF;
--primary-light: #E6E9FD;
--primary-hover: #4F4FF6;
```

### 中性色

```css
/* 文字 */
--text-primary: #333333;    /* 主要文字 */
--text-secondary: #545E74;  /* 次要文字 */
--text-tertiary: #9297A9;   /* 辅助文字 */

/* 背景 */
--bg-page: #F1F3FA;         /* 页面背景 */
--bg-content: #FFFFFF;      /* 内容背景 */
--bg-hover: #F5F7FF;        /* 悬停背景 */

/* 边框 */
--border-light: #D7DEF4;    /* 浅色边框 */
--border-primary: #8eb0f9;  /* 主要边框 */
```

### 功能色

```css
/* 成功 */
--success: #52c41a;
--success-bg: #f6ffed;

/* 警告 */
--warning: #faad14;
--warning-bg: #fffbe6;

/* 错误 */
--error: #ff4d4f;
--error-bg: #fff2f0;

/* 信息 */
--info: #1890ff;
--info-bg: #e6f7ff;
```

## 按钮设计

### 主要按钮

```css
.btn-primary {
    background: linear-gradient(to right, #3462FE, #9D34FE);
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    padding: 12px 24px;
    font-size: 14px;
    box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
}
```

### 次要按钮

```css
.btn-secondary {
    background: white;
    border: 2px solid #676BEF;
    border-radius: 8px;
    color: #676BEF;
    font-weight: 600;
    padding: 10px 24px;
    font-size: 14px;
}

.btn-secondary:hover {
    background: #F5F7FF;
}
```

### 危险按钮

```css
.btn-danger {
    background: #F35859;
    border: none;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    padding: 12px 24px;
    font-size: 14px;
}

.btn-danger:hover {
    background: #e04748;
    transform: translateY(-1px);
}
```

## 表单组件设计

### 输入框

```css
.gr-textbox, .gr-dropdown, .gr-number {
    border-radius: 8px;
    border: 1px solid #D7DEF4;
    transition: all 0.3s ease;
}

.gr-textbox:focus {
    border-color: #676BEF;
    box-shadow: 0 0 0 3px rgba(103, 107, 239, 0.1);
}
```

### 滑块

```css
.gr-slider input[type="range"] {
    accent-color: #676BEF;
}
```

## 交互动画

### 过渡效果

所有交互元素使用统一的过渡时间:

```css
transition: all 0.3s ease;
```

### 悬停效果

- 按钮: 上浮2px + 阴影加深
- 卡片: 上浮2px + 阴影加深
- 导航项: 背景色变化

### 激活效果

- 导航项: 背景色 + 文字颜色变化
- 输入框: 边框颜色 + 外发光

## 响应式设计

### 断点

```css
@media (max-width: 1260px) {
    .sidebar-nav {
        width: 180px;
        min-width: 180px;
    }
    
    .main-content {
        padding: 20px 24px;
    }
}
```

### 最小宽度

```css
min-width: 1260px;  /* 防止内容过度压缩 */
```

## 滚动条美化

```css
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
```

## 可访问性

### 语义化

- 使用语义化的HTML标签
- 合理的标题层级
- 清晰的标签关联

### 键盘导航

- 所有交互元素可通过Tab键访问
- 保持逻辑的Tab顺序
- 明确的焦点状态

### 颜色对比

- 文字与背景对比度 ≥ 4.5:1
- 不仅依赖颜色区分状态
- 配合图标、文字等多种方式

## 性能优化

### CSS优化

- 使用CSS变量统一管理颜色
- 避免过度使用阴影和渐变
- 合理使用GPU加速 (transform)

### 布局优化

- 使用Flexbox布局
- 避免深层嵌套
- 合理使用overflow

## 设计原则

1. **一致性优先**: 统一的视觉语言和交互模式
2. **响应式友好**: 支持多屏幕尺寸
3. **可访问性**: 语义化标签、键盘导航
4. **性能优化**: 减少DOM节点、优化渲染

## 参考资料

- [UI/UX Skill 完整文档](../.kiro/skills/ui-ux/SKILL.md)
- [Ant Design 设计规范](https://ant.design/docs/spec/introduce-cn)
- [Material Design](https://material.io/design)

---

**维护者**: AI Developer Platform Team  
**版本**: 2.0.0  
**最后更新**: 2026-02-11
