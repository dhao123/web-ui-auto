/**
 * Settings - 系统配置页面
 * 专业级设计，无重叠问题
 */
import { useState, useMemo, useEffect } from 'react';
import { Form, Input, InputNumber, Switch, Select, Button, Card, Tabs, message, Slider, Upload } from 'antd';
import { Icon } from '@iconify/react';
import type { AgentConfig, BrowserConfig, LLMConfig } from '@/types/common';
import { useApp } from '@/context/AppContext';
import { api } from '@/utils/api';

const { TextArea } = Input;

// Provider与模型名称配置
const llmProviderOptions = [
  { label: 'ZKH AI Gateway', value: 'zkh' },
  { label: 'OpenAI', value: 'openai' },
  { label: 'Anthropic', value: 'anthropic' },
  { label: 'Google Gemini', value: 'gemini' },
  { label: 'DeepSeek', value: 'deepseek' },
  { label: 'Ollama (本地模型)', value: 'ollama' },
  { label: 'Azure OpenAI', value: 'azure_openai' },
  { label: 'Qwen (通义千问)', value: 'qwen' },
  { label: 'Moonshot (月之暗面)', value: 'moonshot' },
];

const modelNamesByProvider: Record<string, { label: string; value: string }[]> = {
  zkh: [
    { label: 'GPT-4o', value: 'ep_20250805_urdq' },
    { label: 'DeepSeek-V3', value: 'ep_20251217_i18v' },
    { label: 'GPT-4o-mini', value: 'ep_20250805_4q5l' },
    { label: '通义千问VL-Max', value: 'ep_20250805_ur59' },
  ],
  openai: [
    { label: 'GPT-4o', value: 'gpt-4o' },
    { label: 'GPT-4', value: 'gpt-4' },
    { label: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo' },
  ],
  anthropic: [
    { label: 'Claude 3.5 Sonnet', value: 'claude-3-5-sonnet-20241022' },
    { label: 'Claude 3 Opus', value: 'claude-3-opus-20240229' },
  ],
  gemini: [
    { label: 'Gemini 2.0 Flash', value: 'gemini-2.0-flash' },
    { label: 'Gemini 1.5 Pro', value: 'gemini-1.5-pro' },
  ],
  deepseek: [
    { label: 'DeepSeek Chat', value: 'deepseek-chat' },
    { label: 'DeepSeek Reasoner', value: 'deepseek-reasoner' },
  ],
  ollama: [
    { label: 'Qwen2.5 7B', value: 'qwen2.5:7b' },
    { label: 'DeepSeek-R1 14B', value: 'deepseek-r1:14b' },
  ],
  azure_openai: [
    { label: 'GPT-4o', value: 'gpt-4o' },
    { label: 'GPT-4', value: 'gpt-4' },
  ],
  qwen: [
    { label: 'Qwen-MAX', value: 'qwen-max' },
    { label: 'Qwen-Plus', value: 'qwen-plus' },
  ],
  moonshot: [
    { label: 'Moonshot-v1-8k', value: 'moonshot-v1-8k' },
    { label: 'Moonshot-v1-32k', value: 'moonshot-v1-32k' },
  ],
};

const agentTypeOptions = [
  { label: 'Custom Agent', value: 'custom' },
  { label: 'Hugging Face Agent', value: 'hf' },
  { label: 'LangChain Agent', value: 'langchain' },
];

const toolCallingMethodOptions = [
  { label: 'Auto (自动选择)', value: 'auto' },
  { label: 'Function Call', value: 'function_call' },
  { label: 'Raw', value: 'raw' },
  { label: 'JSON Mode', value: 'json_mode' },
  { label: 'Tools', value: 'tools' },
];

// 配置卡片组件
function ConfigCard({ 
  title, 
  icon, 
  children,
  extra,
}: { 
  title: string;
  icon: string;
  children: React.ReactNode;
  extra?: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: 24 }}>
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        padding: '16px 20px',
        background: '#1c2333',
        borderRadius: '12px 12px 0 0',
        border: '1px solid #2d3748',
        borderBottom: 'none'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ 
            width: 36, height: 36, borderRadius: 8,
            background: 'rgba(99, 102, 241, 0.15)',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
          }}>
            <Icon icon={icon} style={{ color: '#818cf8', fontSize: 18 }} />
          </div>
          <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>{title}</span>
        </div>
        {extra}
      </div>
      <div style={{ 
        padding: 24,
        background: '#151b2b',
        borderRadius: '0 0 12px 12px',
        border: '1px solid #2d3748',
        borderTop: 'none'
      }}>
        {children}
      </div>
    </div>
  );
}

export function Settings() {
  const { agentConfig, setAgentConfig, browserConfig, setBrowserConfig, llmConfig, setLLMConfig } = useApp();
  const [agentForm] = Form.useForm();
  const [browserForm] = Form.useForm();
  const [llmForm] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [plannerEnabled, setPlannerEnabled] = useState(llmConfig.plannerEnabled || false);
  const [mainProvider, setMainProvider] = useState(llmConfig.provider || 'openai');
  const [plannerProvider, setPlannerProvider] = useState(llmConfig.plannerProvider || 'openai');
  const [activeTab, setActiveTab] = useState('agent');

  const mainModelOptions = useMemo(() => modelNamesByProvider[mainProvider] || [], [mainProvider]);
  const plannerModelOptions = useMemo(() => modelNamesByProvider[plannerProvider] || [], [plannerProvider]);

  useEffect(() => {
    agentForm.setFieldsValue(agentConfig);
    browserForm.setFieldsValue(browserConfig);
    llmForm.setFieldsValue(llmConfig);
  }, [agentConfig, browserConfig, llmConfig, agentForm, browserForm, llmForm]);

  const handleSaveAgent = async (values: AgentConfig) => {
    setLoading(true);
    try {
      const res = await api.updateAgentConfig(values);
      if (res.code === 0) {
        setAgentConfig(values);
        message.success('Agent配置保存成功');
      } else {
        message.error(res.message || '保存失败');
      }
    } catch {
      message.error('网络错误');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveBrowser = async (values: BrowserConfig) => {
    setLoading(true);
    try {
      const res = await api.updateBrowserConfig(values);
      if (res.code === 0) {
        setBrowserConfig(values);
        message.success('Browser配置保存成功');
      } else {
        message.error(res.message || '保存失败');
      }
    } catch {
      message.error('网络错误');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveLLM = async (values: LLMConfig) => {
    setLoading(true);
    try {
      const res = await api.updateLLMConfig(values);
      if (res.code === 0) {
        setLLMConfig(values);
        message.success('LLM配置保存成功');
      } else {
        message.error(res.message || '保存失败');
      }
    } catch {
      message.error('网络错误');
    } finally {
      setLoading(false);
    }
  };

  const handleMainProviderChange = (value: string) => {
    setMainProvider(value);
    const models = modelNamesByProvider[value];
    if (models?.length > 0) llmForm.setFieldsValue({ modelName: models[0].value });
  };

  const handlePlannerProviderChange = (value: string) => {
    setPlannerProvider(value);
    const models = modelNamesByProvider[value];
    if (models?.length > 0) llmForm.setFieldsValue({ plannerModelName: models[0].value });
  };

  const handleMCPUpload = (info: any) => {
    if (info.file.status === 'done') message.success(`${info.file.name} 上传成功`);
    else if (info.file.status === 'error') message.error(`${info.file.name} 上传失败`);
  };

  const tabItems = [
    {
      key: 'agent',
      label: <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Icon icon="mdi:robot" />Agent配置</span>,
      children: (
        <Form form={agentForm} layout="vertical" onFinish={handleSaveAgent} style={{ maxWidth: 900 }}>
          <ConfigCard title="系统提示词" icon="mdi:message-text">
            <Form.Item label="覆盖系统提示词" name="overrideSystemPrompt">
              <TextArea rows={4} placeholder="输入自定义系统提示词..." />
            </Form.Item>
            <Form.Item label="扩展系统提示词" name="extendSystemPrompt">
              <TextArea rows={4} placeholder="输入要追加的系统提示词..." />
            </Form.Item>
          </ConfigCard>

          <ConfigCard title="MCP服务器配置" icon="mdi:puzzle">
            <Form.Item label="MCP配置文件">
              <Upload accept=".json" action="/api/upload/mcp" onChange={handleMCPUpload} maxCount={1}>
                <Button icon={<Icon icon="mdi:upload" />}>选择配置文件</Button>
              </Upload>
            </Form.Item>
          </ConfigCard>

          <ConfigCard title="基础设置" icon="mdi:cog">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="Agent类型" name="agentType" rules={[{ required: true }]}>
                <Select options={agentTypeOptions} placeholder="选择Agent类型" />
              </Form.Item>
              <Form.Item label="最大执行步数" name="maxSteps" rules={[{ required: true }]}>
                <InputNumber min={1} max={1000} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item label="每步最大操作数" name="maxActionsPerStep" rules={[{ required: true }]}>
                <InputNumber min={1} max={50} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item label="Max Input Tokens" name="maxInputTokens" rules={[{ required: true }]}>
                <InputNumber min={1024} max={1000000} step={1024} style={{ width: '100%' }} formatter={(v) => `${v}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')} />
              </Form.Item>
            </div>
          </ConfigCard>

          <ConfigCard title="高级设置" icon="mdi:tune">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="Tool Calling Method" name="toolCallingMethod" rules={[{ required: true }]}>
                <Select options={toolCallingMethodOptions} placeholder="选择Tool Calling方式" />
              </Form.Item>
              <Form.Item label="启用视觉模式" name="useVision" valuePropName="checked">
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
              <Form.Item label="Tool Call in Content" name="toolCallInContent" valuePropName="checked">
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
            </div>
          </ConfigCard>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} size="large" icon={<Icon icon="mdi:content-save" />}>
              保存配置
            </Button>
          </Form.Item>
        </Form>
      ),
    },
    {
      key: 'browser',
      label: <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Icon icon="mdi:web" />Browser配置</span>,
      children: (
        <Form form={browserForm} layout="vertical" onFinish={handleSaveBrowser} style={{ maxWidth: 900 }}>
          <ConfigCard title="浏览器路径" icon="mdi:folder">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="浏览器可执行文件路径" name="browserBinaryPath">
                <Input placeholder="例如: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome" />
              </Form.Item>
              <Form.Item label="用户数据目录" name="browserUserDataDir">
                <Input placeholder="例如: ./chrome_data" />
              </Form.Item>
            </div>
          </ConfigCard>

          <ConfigCard title="窗口设置" icon="mdi:monitor">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="窗口宽度" name="windowWidth" rules={[{ required: true }]}>
                <InputNumber min={800} max={3840} style={{ width: '100%' }} addonAfter="px" />
              </Form.Item>
              <Form.Item label="窗口高度" name="windowHeight" rules={[{ required: true }]}>
                <InputNumber min={600} max={2160} style={{ width: '100%' }} addonAfter="px" />
              </Form.Item>
            </div>
          </ConfigCard>

          <ConfigCard title="录制与保存" icon="mdi:video">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="录制保存路径" name="saveRecordingPath">
                <Input placeholder="例如: ./tmp/recordings" />
              </Form.Item>
              <Form.Item label="Trace保存路径" name="saveTracePath">
                <Input placeholder="例如: ./tmp/traces" />
              </Form.Item>
            </div>
          </ConfigCard>

          <ConfigCard title="行为设置" icon="mdi:toggle-switch">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="使用自有浏览器" name="useOwnBrowser" valuePropName="checked">
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
              <Form.Item label="保持浏览器打开" name="keepBrowserOpen" valuePropName="checked">
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
              <Form.Item label="无头模式 (Headless)" name="headless" valuePropName="checked">
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
              <Form.Item label="禁用安全限制" name="disableSecurity" valuePropName="checked">
                <Switch checkedChildren="启用" unCheckedChildren="禁用" />
              </Form.Item>
            </div>
          </ConfigCard>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} size="large" icon={<Icon icon="mdi:content-save" />}>
              保存配置
            </Button>
          </Form.Item>
        </Form>
      ),
    },
    {
      key: 'llm',
      label: <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Icon icon="mdi:brain" />LLM配置</span>,
      children: (
        <Form form={llmForm} layout="vertical" onFinish={handleSaveLLM} style={{ maxWidth: 900 }}>
          <ConfigCard title="主LLM配置" icon="mdi:robot-outline">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
              <Form.Item label="LLM Provider" name="provider" rules={[{ required: true }]}>
                <Select options={llmProviderOptions} placeholder="选择LLM Provider" onChange={handleMainProviderChange} />
              </Form.Item>
              <Form.Item label="模型名称" name="modelName" rules={[{ required: true }]}>
                <Select options={mainModelOptions} placeholder="选择模型" showSearch filterOption={(i, o) => (o?.label as string)?.toLowerCase().includes(i.toLowerCase()) ?? false} />
              </Form.Item>
              <Form.Item label="Base URL (可选)" name="baseUrl">
                <Input placeholder="https://api.openai.com/v1" />
              </Form.Item>
              <Form.Item label="API Key" name="apiKey">
                <Input.Password placeholder="sk-..." />
              </Form.Item>
              <Form.Item label="Temperature" name="temperature" style={{ gridColumn: 'span 2' }}>
                <Slider min={0} max={2} step={0.1} marks={{ 0: <span style={{color: '#8b95a5'}}>精确</span>, 1: <span style={{color: '#8b95a5'}}>平衡</span>, 2: <span style={{color: '#8b95a5'}}>创意</span> }} />
              </Form.Item>
            </div>
          </ConfigCard>

          <ConfigCard 
            title="Planner LLM配置" 
            icon="mdi:head-lightbulb"
            extra={
              <Form.Item name="plannerEnabled" valuePropName="checked" style={{ margin: 0 }}>
                <Switch checkedChildren="启用" unCheckedChildren="禁用" onChange={(c) => setPlannerEnabled(c)} />
              </Form.Item>
            }
          >
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24, opacity: plannerEnabled ? 1 : 0.5 }}>
              <Form.Item label="Planner Provider" name="plannerProvider">
                <Select options={llmProviderOptions} placeholder="选择Planner Provider" disabled={!plannerEnabled} onChange={handlePlannerProviderChange} />
              </Form.Item>
              <Form.Item label="Planner 模型名称" name="plannerModelName">
                <Select options={plannerModelOptions} placeholder="选择Planner模型" disabled={!plannerEnabled} showSearch />
              </Form.Item>
              <Form.Item label="Planner Base URL (可选)" name="plannerBaseUrl">
                <Input placeholder="https://api.openai.com/v1" disabled={!plannerEnabled} />
              </Form.Item>
              <Form.Item label="Planner API Key" name="plannerApiKey">
                <Input.Password placeholder="留空使用主LLM配置" disabled={!plannerEnabled} />
              </Form.Item>
              <Form.Item label="Planner Temperature" name="plannerTemperature" style={{ gridColumn: 'span 2' }}>
                <Slider min={0} max={2} step={0.1} disabled={!plannerEnabled} marks={{ 0: <span style={{color: '#8b95a5'}}>精确</span>, 0.7: <span style={{color: '#8b95a5'}}>推荐</span>, 2: <span style={{color: '#8b95a5'}}>创意</span> }} />
              </Form.Item>
            </div>
          </ConfigCard>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} size="large" icon={<Icon icon="mdi:content-save" />}>
              保存配置
            </Button>
          </Form.Item>
        </Form>
      ),
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div className="page-header">
        <div className="page-header-title">
          <div className="page-header-icon">
            <Icon icon="mdi:cog" />
          </div>
          <div className="page-header-text">
            <h1>系统配置</h1>
            <p>配置Agent、浏览器和LLM参数</p>
          </div>
        </div>
      </div>

      <Card bodyStyle={{ padding: 24 }}>
        <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} type="card" />
      </Card>
    </div>
  );
}

export default Settings;
