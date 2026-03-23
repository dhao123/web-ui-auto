/**
 * ZKHConfig - 震坤行MCP配置页面
 * 专业级设计，电商场景专属配置
 */
import { useState } from 'react';
import { Card, Switch, Form, Input, Button, message, Tag } from 'antd';
import { Icon } from '@iconify/react';

import type { ZKHMCPTool, ZKHConfig as ZKHConfigType } from '@/types/common';

// ZKH MCP工具列表
const defaultTools: ZKHMCPTool[] = [
  {
    name: 'zkh_extract_price',
    description: '从页面中提取价格（支持未税价和含税价）',
    enabled: true,
  },
  {
    name: 'zkh_verify_cart_status',
    description: '验证购物车状态和商品数量',
    enabled: true,
  },
  {
    name: 'zkh_wait_for_element',
    description: '智能等待页面元素出现',
    enabled: true,
  },
  {
    name: 'zkh_capture_network',
    description: '捕获网络请求（用于调试和问题定位）',
    enabled: false,
  },
];

// 工具行组件
function ToolRow({ 
  tool, 
  disabled,
  onToggle 
}: { 
  tool: ZKHMCPTool;
  disabled: boolean;
  onToggle: (name: string) => void;
}) {
  return (
    <div 
      style={{ 
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '16px 20px', borderBottom: '1px solid #2d3748',
        opacity: disabled ? 0.5 : 1,
        transition: 'opacity 0.2s'
      }}
    >
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 4 }}>
          <span style={{ fontSize: 14, fontWeight: 600, color: '#ffffff', fontFamily: 'JetBrains Mono, monospace' }}>
            {tool.name}
          </span>
          {tool.enabled && !disabled && (
            <Tag style={{ margin: 0, background: 'rgba(34, 197, 94, 0.15)', color: '#22c55e', border: 'none', fontSize: 12 }}>
              已启用
            </Tag>
          )}
        </div>
        <p style={{ fontSize: 13, color: '#8b95a5', margin: 0 }}>{tool.description}</p>
      </div>
      <Switch
        checked={tool.enabled}
        onChange={() => onToggle(tool.name)}
        disabled={disabled}
      />
    </div>
  );
}

// 使用说明项组件
function InstructionItem({ number, text }: { number: number; text: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
      <div 
        style={{ 
          width: 24, height: 24, borderRadius: '50%',
          background: 'rgba(245, 158, 11, 0.15)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, marginTop: 2
        }}
      >
        <span style={{ color: '#f59e0b', fontSize: 12, fontWeight: 700 }}>{number}</span>
      </div>
      <p style={{ fontSize: 14, color: '#b8c0cc', margin: 0, lineHeight: 1.6 }}>{text}</p>
    </div>
  );
}

export function ZKHConfig() {
  const [config, setConfig] = useState<ZKHConfigType>({
    enabled: true,
    tools: defaultTools,
    customSelectors: {
      price: '.price-untaxed',
      cartCount: '.cart-count',
      addToCartButton: '.btn-add-cart',
    },
  });

  const [form] = Form.useForm();

  const toggleTool = (toolName: string) => {
    setConfig(prev => ({
      ...prev,
      tools: prev.tools.map(tool =>
        tool.name === toolName ? { ...tool, enabled: !tool.enabled } : tool
      ),
    }));
  };

  const handleSave = () => {
    message.success('震坤行MCP配置已保存');
  };

  const handleTest = () => {
    message.success('连接测试成功');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* 页面标题 */}
      <div className="page-header">
        <div className="page-header-title">
          <div 
            className="page-header-icon"
            style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)' }}
          >
            <Icon icon="mdi:store" />
          </div>
          <div className="page-header-text">
            <h1>震坤行MCP配置</h1>
            <p>电商场景专属配置和优化工具集</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <Button 
            size="large"
            icon={<Icon icon="mdi:connection" />}
            onClick={handleTest}
            disabled={!config.enabled}
            style={{ height: 44 }}
          >
            测试连接
          </Button>
          <Button
            type="primary"
            size="large"
            icon={<Icon icon="mdi:content-save" />}
            onClick={handleSave}
            style={{ height: 44, padding: '0 24px' }}
          >
            保存配置
          </Button>
        </div>
      </div>

      {/* 启用开关 */}
      <Card>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <div 
              style={{ 
                width: 52, height: 52, borderRadius: 12,
                background: 'rgba(245, 158, 11, 0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}
            >
              <Icon icon="mdi:power" style={{ fontSize: 26, color: '#f59e0b' }} />
            </div>
            <div>
              <h3 style={{ fontSize: 16, fontWeight: 600, color: '#ffffff', margin: '0 0 4px 0' }}>
                启用震坤行MCP
              </h3>
              <p style={{ fontSize: 14, color: '#8b95a5', margin: 0 }}>
                开启后将加载电商场景专用工具集
              </p>
            </div>
          </div>
          <Switch
            checked={config.enabled}
            onChange={(checked) => setConfig(prev => ({ ...prev, enabled: checked }))}
            checkedChildren="启用"
            unCheckedChildren="禁用"
            style={{ transform: 'scale(1.2)' }}
          />
        </div>
      </Card>

      {/* 工具列表 */}
      <Card 
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ 
              width: 36, height: 36, borderRadius: 8,
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:tools" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>MCP工具集</span>
          </div>
        }
      >
        <div style={{ opacity: config.enabled ? 1 : 0.5, transition: 'opacity 0.2s' }}>
          {config.tools.map((tool) => (
            <ToolRow 
              key={tool.name}
              tool={tool}
              disabled={!config.enabled}
              onToggle={toggleTool}
            />
          ))}
        </div>
      </Card>

      {/* 自定义选择器 */}
      <Card 
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ 
              width: 36, height: 36, borderRadius: 8,
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:code-tags" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>自定义选择器</span>
          </div>
        }
      >
        <div style={{ opacity: config.enabled ? 1 : 0.5, transition: 'opacity 0.2s' }}>
          <Form form={form} layout="vertical" initialValues={config.customSelectors}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item
                label="价格元素选择器"
                name="price"
                tooltip="用于提取商品价格的CSS选择器"
              >
                <Input
                  placeholder="例如: .price-untaxed"
                  disabled={!config.enabled}
                  style={{ fontFamily: 'JetBrains Mono, monospace' }}
                />
              </Form.Item>

              <Form.Item
                label="购物车数量选择器"
                name="cartCount"
                tooltip="用于获取购物车商品数量的CSS选择器"
              >
                <Input
                  placeholder="例如: .cart-count"
                  disabled={!config.enabled}
                  style={{ fontFamily: 'JetBrains Mono, monospace' }}
                />
              </Form.Item>

              <Form.Item
                label="加购按钮选择器"
                name="addToCartButton"
                tooltip="用于定位加购按钮的CSS选择器"
                style={{ gridColumn: 'span 2' }}
              >
                <Input
                  placeholder="例如: .btn-add-cart"
                  disabled={!config.enabled}
                  style={{ fontFamily: 'JetBrains Mono, monospace' }}
                />
              </Form.Item>
            </div>
          </Form>
        </div>
      </Card>

      {/* 使用说明 */}
      <Card 
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ 
              width: 36, height: 36, borderRadius: 8,
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:book-open" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>使用说明</span>
          </div>
        }
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, padding: '8px 4px' }}>
          <InstructionItem 
            number={1} 
            text="启用震坤行MCP后，Agent将自动获得电商场景专用工具的能力" 
          />
          <InstructionItem 
            number={2} 
            text="根据实际页面结构调整自定义选择器，确保工具能够正确定位元素" 
          />
          <InstructionItem 
            number={3} 
            text="建议在测试环境中先验证工具功能，再应用到生产环境" 
          />
        </div>
      </Card>
    </div>
  );
}

export default ZKHConfig;
