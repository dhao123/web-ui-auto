/**
 * ConfigTemplates - 配置模板页面
 * 专业级设计，保存和加载配置模板
 */
import { useState } from 'react';
import { Card, Button, Tag, Modal, Form, Input, message, Popconfirm, Row, Col } from 'antd';
import { Icon } from '@iconify/react';

import { useApp } from '@/context/AppContext';
import type { ConfigTemplate } from '@/types/common';

const { TextArea } = Input;

// 模拟模板数据
const mockTemplates: ConfigTemplate[] = [
  {
    id: '1',
    name: '默认配置',
    description: '适用于大多数场景的默认配置',
    agentConfig: {
      agentType: 'custom',
      maxSteps: 100,
      useVision: true,
      maxActionsPerStep: 10,
      toolCallInContent: true,
      maxInputTokens: 128000,
      toolCallingMethod: 'auto',
    },
    browserConfig: {
      headless: false,
      disableSecurity: true,
      windowWidth: 1280,
      windowHeight: 1100,
      useOwnBrowser: false,
      keepBrowserOpen: true,
    },
    llmConfig: {
      provider: 'openai',
      modelName: 'gpt-4o',
      temperature: 0.6,
    },
    createdAt: '2026-02-01T10:00:00Z',
    updatedAt: '2026-02-01T10:00:00Z',
  },
  {
    id: '2',
    name: '震坤行电商测试',
    description: '针对震坤行电商平台的专用配置',
    agentConfig: {
      agentType: 'custom',
      maxSteps: 50,
      useVision: true,
      maxActionsPerStep: 5,
      toolCallInContent: true,
      maxInputTokens: 64000,
      toolCallingMethod: 'function_calling',
    },
    browserConfig: {
      headless: true,
      disableSecurity: true,
      windowWidth: 1920,
      windowHeight: 1080,
      useOwnBrowser: false,
      keepBrowserOpen: true,
    },
    llmConfig: {
      provider: 'zkh',
      modelName: 'ep_20250805_urdq',
      temperature: 0.5,
    },
    createdAt: '2026-02-05T14:30:00Z',
    updatedAt: '2026-02-10T09:15:00Z',
  },
  {
    id: '3',
    name: '深度研究模式',
    description: '用于深度研究任务的高性能配置',
    agentConfig: {
      agentType: 'custom',
      maxSteps: 200,
      useVision: true,
      maxActionsPerStep: 15,
      toolCallInContent: true,
      maxInputTokens: 256000,
      toolCallingMethod: 'auto',
    },
    browserConfig: {
      headless: false,
      disableSecurity: true,
      windowWidth: 1280,
      windowHeight: 1100,
      useOwnBrowser: false,
      keepBrowserOpen: true,
    },
    llmConfig: {
      provider: 'openai',
      modelName: 'gpt-4o',
      temperature: 0.7,
      plannerEnabled: true,
      plannerProvider: 'openai',
      plannerModelName: 'gpt-4o-mini',
    },
    createdAt: '2026-02-08T16:45:00Z',
    updatedAt: '2026-02-08T16:45:00Z',
  },
];

// 模板卡片组件
function TemplateCard({ 
  template, 
  onApply, 
  onExport, 
  onDelete 
}: { 
  template: ConfigTemplate;
  onApply: (t: ConfigTemplate) => void;
  onExport: (t: ConfigTemplate) => void;
  onDelete: (id: string) => void;
}) {
  return (
    <Card 
      style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
      bodyStyle={{ flex: 1, display: 'flex', flexDirection: 'column' }}
    >
      <div style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
          <h3 style={{ fontSize: 17, fontWeight: 600, color: '#ffffff', margin: 0 }}>{template.name}</h3>
          {template.id === '1' && (
            <Tag style={{ margin: 0, background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8', border: 'none' }}>默认</Tag>
          )}
        </div>
        <p style={{ fontSize: 14, color: '#8b95a5', margin: 0, lineHeight: 1.6 }}>{template.description}</p>
      </div>
      
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
        <Tag style={{ background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.2)', color: '#818cf8', margin: 0 }}>
          <Icon icon="mdi:robot" style={{ marginRight: 4 }} />
          {template.agentConfig.agentType}
        </Tag>
        <Tag style={{ background: 'rgba(34, 197, 94, 0.1)', border: '1px solid rgba(34, 197, 94, 0.2)', color: '#22c55e', margin: 0 }}>
          <Icon icon="mdi:brain" style={{ marginRight: 4 }} />
          {template.llmConfig.provider}
        </Tag>
        <Tag style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.2)', color: '#f59e0b', margin: 0 }}>
          <Icon icon="mdi:eye" style={{ marginRight: 4 }} />
          {template.agentConfig.useVision ? '视觉' : '文本'}
        </Tag>
      </div>
      
      <div style={{ marginTop: 'auto', paddingTop: 16, borderTop: '1px solid #2d3748' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 12, color: '#5a6478' }}>
            更新于: {new Date(template.updatedAt).toLocaleDateString()}
          </span>
          <div style={{ display: 'flex', gap: 8 }}>
            <Button 
              type="primary" 
              size="small"
              icon={<Icon icon="mdi:check" />}
              onClick={() => onApply(template)}
              style={{ height: 32 }}
            >
              应用
            </Button>
            <Button 
              size="small"
              icon={<Icon icon="mdi:download" />}
              onClick={() => onExport(template)}
              style={{ height: 32 }}
            >
              导出
            </Button>
            <Popconfirm
              title="确认删除"
              description={`确定要删除模板 "${template.name}" 吗？`}
              onConfirm={() => onDelete(template.id)}
              okText="确定"
              cancelText="取消"
            >
              <Button 
                size="small"
                danger
                icon={<Icon icon="mdi:delete" />}
                style={{ height: 32 }}
              >
                删除
              </Button>
            </Popconfirm>
          </div>
        </div>
      </div>
    </Card>
  );
}

export function ConfigTemplates() {
  const { agentConfig, browserConfig, llmConfig, setAgentConfig, setBrowserConfig, setLLMConfig } = useApp();
  const [templates, setTemplates] = useState<ConfigTemplate[]>(mockTemplates);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleApplyTemplate = (template: ConfigTemplate) => {
    setAgentConfig(template.agentConfig);
    setBrowserConfig(template.browserConfig);
    setLLMConfig(template.llmConfig);
    message.success(`已应用模板: ${template.name}`);
  };

  const handleDeleteTemplate = (templateId: string) => {
    setTemplates(prev => prev.filter(t => t.id !== templateId));
    message.success('模板已删除');
  };

  const handleSaveTemplate = async (values: { name: string; description: string }) => {
    setLoading(true);
    try {
      const newTemplate: ConfigTemplate = {
        id: Date.now().toString(),
        name: values.name,
        description: values.description,
        agentConfig: { ...agentConfig },
        browserConfig: { ...browserConfig },
        llmConfig: { ...llmConfig },
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      setTemplates(prev => [newTemplate, ...prev]);
      message.success('模板保存成功');
      setIsModalVisible(false);
      form.resetFields();
    } finally {
      setLoading(false);
    }
  };

  const handleExportTemplate = (template: ConfigTemplate) => {
    const dataStr = JSON.stringify(template, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = `${template.name}.json`;
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* 页面标题 */}
      <div className="page-header">
        <div className="page-header-title">
          <div className="page-header-icon">
            <Icon icon="mdi:content-save" />
          </div>
          <div className="page-header-text">
            <h1>配置模板</h1>
            <p>保存和加载配置模板，快速切换测试场景</p>
          </div>
        </div>
        <Button
          type="primary"
          size="large"
          icon={<Icon icon="mdi:plus" />}
          onClick={() => setIsModalVisible(true)}
          style={{ height: 44, padding: '0 24px' }}
        >
          保存当前配置
        </Button>
      </div>

      {/* 模板列表 */}
      <Row gutter={[24, 24]}>
        {templates.map(template => (
          <Col key={template.id} xs={24} md={12} xl={8}>
            <TemplateCard 
              template={template}
              onApply={handleApplyTemplate}
              onExport={handleExportTemplate}
              onDelete={handleDeleteTemplate}
            />
          </Col>
        ))}
      </Row>

      {/* 保存模板弹窗 */}
      <Modal
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ 
              width: 36, height: 36, borderRadius: 8,
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:content-save" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 16, fontWeight: 600, color: '#ffffff' }}>保存配置模板</span>
          </div>
        }
        open={isModalVisible}
        onCancel={() => {
          setIsModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={520}
      >
        <Form form={form} layout="vertical" onFinish={handleSaveTemplate} style={{ marginTop: 16 }}>
          <Form.Item
            label="模板名称"
            name="name"
            rules={[{ required: true, message: '请输入模板名称' }]}
          >
            <Input placeholder="例如: 震坤行电商测试配置" />
          </Form.Item>

          <Form.Item
            label="描述"
            name="description"
            rules={[{ required: true, message: '请输入模板描述' }]}
          >
            <TextArea rows={3} placeholder="描述此配置的适用场景..." />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, marginTop: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
              <Button size="large" onClick={() => setIsModalVisible(false)} style={{ height: 44 }}>
                取消
              </Button>
              <Button 
                type="primary" 
                htmlType="submit"
                loading={loading}
                size="large"
                style={{ height: 44, padding: '0 28px' }}
              >
                保存
              </Button>
            </div>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default ConfigTemplates;
