"""
Enterprise Interface Module
企业级界面模块 - 提供专业的视觉体验和交互设计
"""

import gradio as gr
from typing import Literal

from src.webui.webui_manager import WebuiManager
from src.webui.components.enterprise_agent_settings import create_enterprise_agent_settings
from src.webui.components.enterprise_browser_settings import create_enterprise_browser_settings
from src.webui.components.enterprise_run_agent import create_enterprise_run_agent
from src.webui.components.enterprise_deep_research import create_enterprise_deep_research
from src.webui.components.enterprise_config_manager import create_enterprise_config_manager


def get_enterprise_css() -> str:
    """获取企业级CSS样式"""
    return """
    /* ==========================================
       🎨 Enterprise Design System
       企业级设计系统 - 专业、现代、优雅
       ========================================== */
    
    /* CSS Variables - Design Tokens */
    :root {
        /* Primary Colors */
        --ep-primary-50: #eff6ff;
        --ep-primary-100: #dbeafe;
        --ep-primary-200: #bfdbfe;
        --ep-primary-300: #93c5fd;
        --ep-primary-400: #60a5fa;
        --ep-primary-500: #3b82f6;
        --ep-primary-600: #2563eb;
        --ep-primary-700: #1d4ed8;
        --ep-primary-800: #1e40af;
        --ep-primary-900: #1e3a8a;
        
        /* Neutral Colors */
        --ep-gray-50: #f9fafb;
        --ep-gray-100: #f3f4f6;
        --ep-gray-200: #e5e7eb;
        --ep-gray-300: #d1d5db;
        --ep-gray-400: #9ca3af;
        --ep-gray-500: #6b7280;
        --ep-gray-600: #4b5563;
        --ep-gray-700: #374151;
        --ep-gray-800: #1f2937;
        --ep-gray-900: #111827;
        
        /* Semantic Colors */
        --ep-success-50: #f0fdf4;
        --ep-success-500: #22c55e;
        --ep-success-600: #16a34a;
        --ep-warning-50: #fffbeb;
        --ep-warning-500: #f59e0b;
        --ep-warning-600: #d97706;
        --ep-error-50: #fef2f2;
        --ep-error-500: #ef4444;
        --ep-error-600: #dc2626;
        --ep-info-50: #eff6ff;
        --ep-info-500: #3b82f6;
        
        /* Typography */
        --ep-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        --ep-font-mono: 'JetBrains Mono', 'Fira Code', Consolas, Monaco, 'Courier New', monospace;
        
        /* Spacing */
        --ep-space-1: 0.25rem;
        --ep-space-2: 0.5rem;
        --ep-space-3: 0.75rem;
        --ep-space-4: 1rem;
        --ep-space-5: 1.25rem;
        --ep-space-6: 1.5rem;
        --ep-space-8: 2rem;
        --ep-space-10: 2.5rem;
        --ep-space-12: 3rem;
        
        /* Shadows */
        --ep-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --ep-shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --ep-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --ep-shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --ep-shadow-glow: 0 0 20px rgba(59, 130, 246, 0.3);
        
        /* Border Radius */
        --ep-radius-sm: 0.375rem;
        --ep-radius-md: 0.5rem;
        --ep-radius-lg: 0.75rem;
        --ep-radius-xl: 1rem;
        --ep-radius-2xl: 1.5rem;
        --ep-radius-full: 9999px;
        
        /* Transitions */
        --ep-transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --ep-transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
        --ep-transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ==========================================
       🌐 Global Styles
       ========================================== */
    
    .gradio-container {
        font-family: var(--ep-font-sans) !important;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%) !important;
        min-height: 100vh !important;
        padding: 0 !important;
    }
    
    /* Hide default Gradio header */
    .gradio-container > .main > .header {
        display: none !important;
    }
    
    /* ==========================================
       🎯 Header Section
       ========================================== */
    
    .ep-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%) !important;
        padding: 2rem 2.5rem !important;
        margin: 0 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .ep-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 100%, rgba(59, 130, 246, 0.1) 0%, transparent 50%) !important;
        pointer-events: none;
    }
    
    .ep-header-content {
        position: relative;
        z-index: 1;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .ep-header-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .ep-header-logo-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
    }
    
    .ep-header-title {
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.025em !important;
        margin: 0 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .ep-header-subtitle {
        font-size: 1rem !important;
        color: #94a3b8 !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }
    
    .ep-header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.875rem;
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #60a5fa;
        margin-top: 1rem;
    }
    
    .ep-header-badge::before {
        content: '';
        width: 6px;
        height: 6px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* ==========================================
       📍 Step Indicator
       ========================================== */
    
    .ep-steps-container {
        background: #ffffff !important;
        padding: 1.5rem 2.5rem 0.5rem !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    .ep-steps {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .ep-step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: var(--ep-radius-lg);
        background: #f1f5f9;
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all var(--ep-transition-base);
    }
    
    .ep-step-active {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
    }
    
    .ep-step-number {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .ep-step-active .ep-step-number {
        background: rgba(255, 255, 255, 0.3);
    }
    
    .ep-step-arrow {
        color: #cbd5e1;
        font-size: 1.25rem;
        font-weight: 300;
    }
    
    @media (max-width: 768px) {
        .ep-step-label {
            display: none;
        }
        .ep-step {
            padding: 0.5rem;
        }
    }
    
    /* ==========================================
       📑 Navigation Tabs
       ========================================== */
    
    .ep-tabs-container {
        background: #ffffff !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 0 2.5rem !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 100 !important;
        box-shadow: var(--ep-shadow-sm) !important;
    }
    
    .ep-tabs {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        gap: 0.25rem;
    }
    
    .ep-tabs .tab-nav {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        gap: 0.25rem !important;
    }
    
    .ep-tabs .tab-nav button {
        padding: 1rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #64748b !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        background: transparent !important;
        transition: all var(--ep-transition-base) !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    
    .ep-tabs .tab-nav button:hover {
        color: #334155 !important;
        background: #f8fafc !important;
    }
    
    .ep-tabs .tab-nav button.selected {
        color: #2563eb !important;
        border-bottom-color: #2563eb !important;
        background: transparent !important;
    }
    
    .ep-tabs .tab-nav button.selected::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 24px;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 3px 3px 0 0;
    }
    
    /* Tab Icons */
    .ep-tab-icon {
        font-size: 1.125rem;
    }
    
    /* ==========================================
       📂 Accordion
       ========================================== */
    
    .ep-accordion {
        background: #ffffff;
        border-radius: var(--ep-radius-lg);
        border: 1px solid #e2e8f0;
        box-shadow: var(--ep-shadow-sm);
        overflow: hidden;
    }
    
    .ep-accordion > .label-wrap {
        padding: 1rem 1.25rem !important;
        background: #f8fafc !important;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .ep-accordion > .label-wrap > span {
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    
    .ep-accordion > .label-wrap > .icon {
        color: #64748b !important;
    }
    
    .ep-accordion > .content-wrap {
        padding: 1.25rem !important;
    }
    
    /* ==========================================
       📦 Content Container
       ========================================== */
    
    .ep-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem 2.5rem;
    }
    
    .ep-panel {
        background: #ffffff;
        border-radius: var(--ep-radius-xl);
        box-shadow: var(--ep-shadow-md);
        border: 1px solid #e2e8f0;
        overflow: hidden;
    }
    
    /* ==========================================
       🎴 Cards
       ========================================== */
    
    .ep-card {
        background: #ffffff;
        border-radius: var(--ep-radius-lg);
        border: 1px solid #e2e8f0;
        box-shadow: var(--ep-shadow-sm);
        transition: all var(--ep-transition-base);
    }
    
    .ep-card:hover {
        box-shadow: var(--ep-shadow-md);
        border-color: #cbd5e1;
    }
    
    .ep-card-header {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .ep-card-header > .markdown {
        margin: 0 !important;
    }
    
    .ep-card-header > .markdown > p {
        margin: 0 !important;
        font-size: 0.9375rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .ep-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .ep-card-title-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    .ep-card-body {
        padding: 1.5rem;
    }
    
    .ep-card-footer {
        padding: 1rem 1.5rem;
        background: #f8fafc;
        border-top: 1px solid #f1f5f9;
    }
    
    /* ==========================================
       📊 Stats Cards (Metrics)
       ========================================== */
    
    .ep-stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .ep-stat-card {
        background: #ffffff;
        border-radius: var(--ep-radius-lg);
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: var(--ep-shadow-sm);
        position: relative;
        overflow: hidden;
        transition: all var(--ep-transition-base);
    }
    
    .ep-stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    
    .ep-stat-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--ep-shadow-md);
    }
    
    .ep-stat-card.primary::before { background: linear-gradient(180deg, #3b82f6, #1d4ed8); }
    .ep-stat-card.success::before { background: linear-gradient(180deg, #22c55e, #16a34a); }
    .ep-stat-card.warning::before { background: linear-gradient(180deg, #f59e0b, #d97706); }
    .ep-stat-card.error::before { background: linear-gradient(180deg, #ef4444, #dc2626); }
    .ep-stat-card.info::before { background: linear-gradient(180deg, #06b6d4, #0891b2); }
    
    .ep-stat-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    
    .ep-stat-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .ep-stat-card.primary .ep-stat-icon { background: #eff6ff; }
    .ep-stat-card.success .ep-stat-icon { background: #f0fdf4; }
    .ep-stat-card.warning .ep-stat-icon { background: #fffbeb; }
    .ep-stat-card.error .ep-stat-icon { background: #fef2f2; }
    .ep-stat-card.info .ep-stat-icon { background: #ecfeff; }
    
    .ep-stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .ep-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.2;
    }
    
    .ep-stat-desc {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }
    
    /* ==========================================
       ⌨️ Form Elements
       ========================================== */
    
    .ep-form-group {
        margin-bottom: 1.5rem;
    }
    
    .ep-form-label {
        display: block;
        font-size: 0.875rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .ep-form-hint {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Text Input */
    .ep-input,
    .ep-input textarea,
    input[type="text"].ep-input,
    textarea.ep-input {
        width: 100% !important;
        padding: 0.625rem 0.875rem !important;
        font-size: 0.875rem !important;
        line-height: 1.5 !important;
        color: #1f2937 !important;
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: var(--ep-radius-md) !important;
        transition: all var(--ep-transition-fast) !important;
        font-family: var(--ep-font-sans) !important;
    }
    
    .ep-input:focus,
    .ep-input:focus-within,
    .ep-input textarea:focus {
        outline: none !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .ep-input::placeholder {
        color: #9ca3af !important;
    }
    
    /* Text Area Large */
    .ep-textarea-lg textarea {
        min-height: 120px !important;
        resize: vertical !important;
    }
    
    /* Select/Dropdown */
    .ep-select {
        appearance: none !important;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e") !important;
        background-position: right 0.5rem center !important;
        background-repeat: no-repeat !important;
        background-size: 1.5em 1.5em !important;
        padding-right: 2.5rem !important;
    }
    
    /* Checkbox & Radio */
    .ep-checkbox {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        font-size: 0.875rem;
        color: #374151;
    }
    
    .ep-checkbox input[type="checkbox"] {
        width: 1rem;
        height: 1rem;
        border: 1px solid #d1d5db;
        border-radius: 0.25rem;
        accent-color: #3b82f6;
    }
    
    /* Slider */
    .ep-slider input[type="range"] {
        width: 100%;
        height: 6px;
        background: #e5e7eb;
        border-radius: 3px;
        outline: none;
        accent-color: #3b82f6;
    }
    
    /* ==========================================
       🔘 Buttons
       ========================================== */
    
    .ep-btn {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
        padding: 0.625rem 1.25rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        border-radius: var(--ep-radius-md) !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
        transition: all var(--ep-transition-fast) !important;
        font-family: var(--ep-font-sans) !important;
    }
    
    .ep-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .ep-btn-primary {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border-color: transparent !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2) !important;
    }
    
    .ep-btn-primary:hover:not(:disabled) {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-1px);
    }
    
    .ep-btn-secondary {
        background: #ffffff !important;
        color: #374151 !important;
        border-color: #d1d5db !important;
    }
    
    .ep-btn-secondary:hover:not(:disabled) {
        background: #f9fafb !important;
        border-color: #9ca3af !important;
    }
    
    .ep-btn-success {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.2) !important;
    }
    
    .ep-btn-success:hover:not(:disabled) {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
        box-shadow: 0 6px 8px -1px rgba(34, 197, 94, 0.3) !important;
    }
    
    .ep-btn-danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2) !important;
    }
    
    .ep-btn-danger:hover:not(:disabled) {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        box-shadow: 0 6px 8px -1px rgba(239, 68, 68, 0.3) !important;
    }
    
    .ep-btn-ghost {
        background: transparent !important;
        color: #6b7280 !important;
        border-color: transparent !important;
    }
    
    .ep-btn-ghost:hover:not(:disabled) {
        background: #f3f4f6 !important;
        color: #374151 !important;
    }
    
    .ep-btn-lg {
        padding: 0.875rem 2rem !important;
        font-size: 1rem !important;
    }
    
    .ep-btn-sm {
        padding: 0.375rem 0.875rem !important;
        font-size: 0.75rem !important;
    }
    
    /* ==========================================
       📋 Chat/Message Area
       ========================================== */
    
    .ep-chat-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: var(--ep-radius-lg);
        overflow: hidden;
    }
    
    .ep-chat-header {
        padding: 1rem 1.25rem;
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .ep-chat-messages {
        padding: 1.25rem;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .ep-message {
        margin-bottom: 1rem;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .ep-message-user {
        display: flex;
        justify-content: flex-end;
    }
    
    .ep-message-user .ep-message-content {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        border-radius: 16px 16px 4px 16px;
    }
    
    .ep-message-assistant .ep-message-content {
        background: #f1f5f9;
        color: #1e293b;
        border-radius: 16px 16px 16px 4px;
    }
    
    .ep-message-content {
        padding: 0.875rem 1.125rem;
        max-width: 80%;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    /* ==========================================
       🖼️ Browser View
       ========================================== */
    
    .ep-browser-frame {
        background: #1e293b;
        border-radius: var(--ep-radius-lg);
        overflow: hidden;
        box-shadow: var(--ep-shadow-lg);
    }
    
    .ep-browser-header {
        background: #334155;
        padding: 0.75rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .ep-browser-dots {
        display: flex;
        gap: 0.375rem;
    }
    
    .ep-browser-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    .ep-browser-dot.red { background: #ef4444; }
    .ep-browser-dot.yellow { background: #f59e0b; }
    .ep-browser-dot.green { background: #22c55e; }
    
    .ep-browser-address {
        flex: 1;
        background: #1e293b;
        border-radius: 6px;
        padding: 0.375rem 0.75rem;
        font-size: 0.75rem;
        color: #94a3b8;
        font-family: var(--ep-font-mono);
    }
    
    .ep-browser-content {
        background: #f8fafc;
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .ep-browser-content img {
        max-width: 100%;
        max-height: 500px;
        object-fit: contain;
    }
    
    /* ==========================================
       🏷️ Badges & Tags
       ========================================== */
    
    .ep-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.625rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
    }
    
    .ep-badge-primary {
        background: #eff6ff;
        color: #1d4ed8;
    }
    
    .ep-badge-success {
        background: #f0fdf4;
        color: #15803d;
    }
    
    .ep-badge-warning {
        background: #fffbeb;
        color: #b45309;
    }
    
    .ep-badge-error {
        background: #fef2f2;
        color: #b91c1c;
    }
    
    /* ==========================================
       🔔 Alerts
       ========================================== */
    
    .ep-alert {
        padding: 1rem 1.25rem;
        border-radius: var(--ep-radius-lg);
        border-left: 4px solid;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .ep-alert-info {
        background: #eff6ff;
        border-color: #3b82f6;
        color: #1e40af;
    }
    
    .ep-alert-success {
        background: #f0fdf4;
        border-color: #22c55e;
        color: #166534;
    }
    
    .ep-alert-warning {
        background: #fffbeb;
        border-color: #f59e0b;
        color: #92400e;
    }
    
    .ep-alert-error {
        background: #fef2f2;
        border-color: #ef4444;
        color: #991b1b;
    }
    
    /* ==========================================
       📱 Responsive
       ========================================== */
    
    @media (max-width: 768px) {
        .ep-content {
            padding: 1rem;
        }
        
        .ep-header {
            padding: 1.5rem 1rem !important;
        }
        
        .ep-header-title {
            font-size: 1.5rem !important;
        }
        
        .ep-tabs-container {
            padding: 0 1rem !important;
        }
        
        .ep-tabs .tab-nav button {
            padding: 0.75rem 1rem !important;
            font-size: 0.8125rem !important;
        }
        
        .ep-stats-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* ==========================================
       🎭 Animations
       ========================================== */
    
    .ep-fade-in {
        animation: epFadeIn 0.4s ease-out;
    }
    
    @keyframes epFadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .ep-slide-in {
        animation: epSlideIn 0.3s ease-out;
    }
    
    @keyframes epSlideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ==========================================
       🎯 Utility Classes
       ========================================== */
    
    .ep-flex { display: flex; }
    .ep-flex-col { flex-direction: column; }
    .ep-items-center { align-items: center; }
    .ep-justify-between { justify-content: space-between; }
    .ep-gap-2 { gap: 0.5rem; }
    .ep-gap-4 { gap: 1rem; }
    .ep-gap-6 { gap: 1.5rem; }
    
    .ep-mb-0 { margin-bottom: 0; }
    .ep-mb-2 { margin-bottom: 0.5rem; }
    .ep-mb-4 { margin-bottom: 1rem; }
    .ep-mb-6 { margin-bottom: 1.5rem; }
    
    .ep-mt-2 { margin-top: 0.5rem; }
    .ep-mt-4 { margin-top: 1rem; }
    
    .ep-p-4 { padding: 1rem; }
    .ep-p-6 { padding: 1.5rem; }
    
    .ep-text-sm { font-size: 0.875rem; }
    .ep-text-xs { font-size: 0.75rem; }
    .ep-text-lg { font-size: 1.125rem; }
    .ep-font-medium { font-weight: 500; }
    .ep-font-semibold { font-weight: 600; }
    .ep-font-bold { font-weight: 700; }
    
    .ep-text-gray { color: #6b7280; }
    .ep-text-primary { color: #3b82f6; }
    .ep-text-success { color: #22c55e; }
    .ep-text-warning { color: #f59e0b; }
    .ep-text-error { color: #ef4444; }
    
    .ep-hidden { display: none !important; }
    .ep-w-full { width: 100%; }
    
    /* ==========================================
       📝 Config List
       ========================================== */
    
    .ep-config-list {
        background: #f8fafc;
        border-radius: var(--ep-radius-md);
        padding: 1rem;
        font-size: 0.875rem;
        line-height: 1.8;
    }
    
    .ep-config-list p {
        margin: 0;
    }
    
    .ep-config-list strong {
        color: #1e293b;
        font-weight: 600;
    }
    """


def create_enterprise_ui(theme_mode: Literal["light", "dark", "auto"] = "auto", lang: Literal["zh", "en"] = "zh"):
    """
    创建企业级WebUI界面
    
    Args:
        theme_mode: 主题模式
        lang: 界面语言
    """
    
    # 文本内容配置
    texts = {
        "zh": {
            "title": "AI测试",
            "subtitle": "AI用例执行",
            "status": "系统运行正常",
            "tabs": {
                "agent_settings": "🤖 模型配置",
                "browser_settings": "🌐 环境配置", 
                "run_agent": "▶️ 运行任务",
                "deep_research": "🔬 深度研究",
                "config": "💾 配置管理"
            },
            "steps": {
                "step1": "配置模型",
                "step2": "设置环境",
                "step3": "运行任务",
                "step4": "查看结果"
            }
        },
        "en": {
            "title": "AI Test",
            "subtitle": "AI Test Execution",
            "status": "System Operational",
            "tabs": {
                "agent_settings": "🤖 Model Config",
                "browser_settings": "🌐 Environment",
                "run_agent": "▶️ Run Task",
                "deep_research": "🔬 Deep Research",
                "config": "💾 Config"
            },
            "steps": {
                "step1": "Config Model",
                "step2": "Set Environment",
                "step3": "Run Task",
                "step4": "View Results"
            }
        }
    }
    
    t = texts[lang]
    
    # 获取企业级CSS
    css = get_enterprise_css()
    
    # JavaScript for theme detection
    js = """
    () => {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const url = new URL(window.location);
        const currentTheme = url.searchParams.get('__theme');
        
        if (!currentTheme || currentTheme === 'auto') {
            if (prefersDark) {
                url.searchParams.set('__theme', 'dark');
            } else {
                url.searchParams.set('__theme', 'light');
            }
            window.location.href = url.href;
        }
    }
    """
    
    # 创建UI管理器
    ui_manager = WebuiManager()
    
    with gr.Blocks(
        title=t["title"],
        css=css,
        js=js,
        theme=gr.themes.Default(
            primary_hue="blue",
            secondary_hue="indigo",
            neutral_hue="slate",
        )
    ) as demo:
        
        # ==================== Header ====================
        with gr.Row(elem_classes=["ep-header"]):
            with gr.Column():
                gr.Markdown(f"""
                <div class="ep-header-content">
                    <div class="ep-header-logo">
                        <div class="ep-header-logo-icon">🌐</div>
                        <div>
                            <h1 class="ep-header-title">{t["title"]}</h1>
                            <p class="ep-header-subtitle">{t["subtitle"]}</p>
                        </div>
                    </div>
                    <div class="ep-header-badge">{t["status"]}</div>
                </div>
                """, elem_classes=["ep-header-markdown"])
        
        # ==================== Step Indicator ====================
        with gr.Row(elem_classes=["ep-steps-container"]):
            with gr.Column(elem_classes=["ep-content"]):
                gr.Markdown(f"""
                <div class="ep-steps">
                    <div class="ep-step ep-step-active">
                        <div class="ep-step-number">1</div>
                        <div class="ep-step-label">{t["steps"]["step1"]}</div>
                    </div>
                    <div class="ep-step-arrow">→</div>
                    <div class="ep-step">
                        <div class="ep-step-number">2</div>
                        <div class="ep-step-label">{t["steps"]["step2"]}</div>
                    </div>
                    <div class="ep-step-arrow">→</div>
                    <div class="ep-step">
                        <div class="ep-step-number">3</div>
                        <div class="ep-step-label">{t["steps"]["step3"]}</div>
                    </div>
                    <div class="ep-step-arrow">→</div>
                    <div class="ep-step">
                        <div class="ep-step-number">4</div>
                        <div class="ep-step-label">{t["steps"]["step4"]}</div>
                    </div>
                </div>
                """)
        
        # ==================== Navigation Tabs ====================
        with gr.Row(elem_classes=["ep-tabs-container"]):
            with gr.Tabs(elem_classes=["ep-tabs"]) as tabs:
                
                # Tab 1: Agent Settings
                with gr.TabItem(t["tabs"]["agent_settings"]):
                    create_enterprise_agent_settings(ui_manager, lang)
                
                # Tab 2: Browser Settings
                with gr.TabItem(t["tabs"]["browser_settings"]):
                    create_enterprise_browser_settings(ui_manager, lang)
                
                # Tab 3: Run Agent (Main)
                with gr.TabItem(t["tabs"]["run_agent"]):
                    create_enterprise_run_agent(ui_manager, lang)
                
                # Tab 4: Deep Research
                with gr.TabItem(t["tabs"]["deep_research"]):
                    create_enterprise_deep_research(ui_manager, lang)
                
                # Tab 5: Config Management
                with gr.TabItem(t["tabs"]["config"]):
                    create_enterprise_config_manager(ui_manager, lang)
    
    return demo
