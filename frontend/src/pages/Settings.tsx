/**
 * Settings - 配置页面
 */
import { useState, useMemo } from 'react';
import { Form, Input, InputNumber, Switch, Select, Button, Card, Tabs, message, Slider, Divider } from 'antd';
import { Icon } from '@iconify/react';
import type { AgentConfig, BrowserConfig } from '@/types/common';

// =============================================================================
// Provider与模型名称配置 (与后端config.py保持一致)
// =============================================================================

// LLM Provider选项（含ZKH）
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

// 各Provider对应的模型名称列表 (参考 config.py)
const modelNamesByProvider: Record<string, { label: string; value: string }[]> = {
  zkh: [
    { label: 'GPT-4o (ep_20250805_urdq)', value: 'ep_20250805_urdq' },
    { label: 'DeepSeek-V3 推荐 (ep_20251217_i18v)', value: 'ep_20251217_i18v' },
    { label: 'GPT-4o-mini (ep_20250805_4q5l)', value: 'ep_20250805_4q5l' },
    { label: '通义千问VL-Max 视觉 (ep_20250805_ur59)', value: 'ep_20250805_ur59' },
    { label: '通义千问3-235B (ep_20250731_vzaa)', value: 'ep_20250731_vzaa' },
    { label: '通义千问-Max (ep_20250728_izkl)', value: 'ep_20250728_izkl' },
    { label: 'ZKH-LLM (ep_20250718_zoiz)', value: 'ep_20250718_zoiz' },
    { label: 'Qwen-Long (ep_20250904_slsu)', value: 'ep_20250904_slsu' },
  ],
  openai: [
    { label: 'GPT-4o', value: 'gpt-4o' },
    { label: 'GPT-4', value: 'gpt-4' },
    { label: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo' },
    { label: 'o3-mini', value: 'o3-mini' },
  ],
  anthropic: [
    { label: 'Claude 3.5 Sonnet', value: 'claude-3-5-sonnet-20241022' },
    { label: 'Claude 3 Opus', value: 'claude-3-opus-20240229' },
    { label: 'Claude 3 Haiku', value: 'claude-3-haiku-20240307' },
  ],
  gemini: [
    { label: 'Gemini 2.0 Flash', value: 'gemini-2.0-flash' },
    { label: 'Gemini 1.5 Pro', value: 'gemini-1.5-pro' },
    { label: 'Gemini 1.5 Flash', value: 'gemini-1.5-flash' },
  ],
  deepseek: [
    { label: 'DeepSeek Chat', value: 'deepseek-chat' },
    { label: 'DeepSeek Reasoner', value: 'deepseek-reasoner' },
  ],
  ollama: [
    { label: 'Qwen2.5 7B', value: 'qwen2.5:7b' },
    { label: 'Qwen2.5 14B', value: 'qwen2.5:14b' },
    { label: 'Qwen2.5 32B', value: 'qwen2.5:32b' },
    { label: 'Qwen2.5-Coder 14B', value: 'qwen2.5-coder:14b' },
    { label: 'Qwen2.5-Coder 32B', value: 'qwen2.5-coder:32b' },
    { label: 'Llama2 7B', value: 'llama2:7b' },
    { label: 'DeepSeek-R1 14B', value: 'deepseek-r1:14b' },
    { label: 'DeepSeek-R1 32B', value: 'deepseek-r1:32b' },
  ],
};

// =============================================================================
// 其他配置选项
// =============================================================================

const defaultAgentConfig: AgentConfig = {
  agentType: 'custom',
  maxSteps: 100,
  useVision: true,
  maxActionsPerStep: 10,
  toolCallInContent: true,
  maxInputTokens: 128000,
  toolCallingMethod: 'auto',
};

const defaultBrowserConfig: BrowserConfig = {
  headless: false,
  disableSecurity: true,
  windowWidth: 1280,
  windowHeight: 1100,
  saveRecordingPath: './tmp/recordings',
  saveTracePath: './tmp/traces',
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

// =============================================================================
// Settings组件
// =============================================================================

export function Settings() {
  const [agentForm] = Form.useForm();
  const [browserForm] = Form.useForm();
  const [llmForm] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [plannerEnabled, setPlannerEnabled] = useState(false);

  // 主LLM的Provider选择状态
  const [mainProvider, setMainProvider] = useState('openai');
  // Planner LLM的Provider选择状态
  const [plannerProvider, setPlannerProvider] = useState('openai');

  // 根据Provider动态获取模型列表
  const mainModelOptions = useMemo(() => {
    return modelNamesByProvider[mainProvider] || [];
  }, [mainProvider]);

  const plannerModelOptions = useMemo(() => {
    return modelNamesByProvider[plannerProvider] || [];
  }, [plannerProvider]);

  // Provider切换时重置模型选择
  const handleMainProviderChange = (value: string) => {
    setMainProvider(value);
    const models = modelNamesByProvider[value];
    if (models && models.length > 0) {
      llmForm.setFieldsValue({ modelName: models[0].value });
    } else {
      llmForm.setFieldsValue({ modelName: undefined });
    }
  };

  const handlePlannerProviderChange = (value: string) => {
    setPlannerProvider(value);
    const models = modelNamesByProvider[value];
    if (models && models.length > 0) {
      llmForm.setFieldsValue({ plannerModelName: models[0].value });
    } else {
      llmForm.setFieldsValue({ plannerModelName: undefined });
    }
  };

  const handleSaveAgent = async (values: AgentConfig) => {
    setLoading(true);
    try {
      console.log('Agent config:', values);
      message.success('Agent配置保存成功');
    } catch {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveBrowser = async (values: BrowserConfig) => {
    setLoading(true);
    try {
      console.log('Browser config:', values);
      message.success('Browser配置保存成功');
    } catch {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveLLM = async (values: Record<string, unknown>) => {
    setLoading(true);
    try {
      console.log('LLM config:', values);
      message.success('LLM配置保存成功');
    } catch {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const tabItems = [
    {
      key: 'agent',
      label: (
        <span className="flex items-center">
          <Icon icon="mdi:robot" className="mr-2" />
          Agent配置
        </span>
      ),
      children: (
        <Card className="card-shadow">
          <Form
            form={agentForm}
            layout="vertical"
            initialValues={defaultAgentConfig}
            onFinish={handleSaveAgent}
          >
            {/* 基础设置 */}
            <div className="mb-4">
              <h3 className="text-[14px] font-semibold text-[#333] mb-4 flex items-center">
                <Icon icon="mdi:cog" className="mr-2 text-[#676BEF]" />
                基础设置
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <Form.Item
                  label="Agent类型"
                  name="agentType"
                  rules={[{ required: true, message: '请选择Agent类型' }]}
                >
                  <Select options={agentTypeOptions} placeholder="选择Agent类型" />
                </Form.Item>

                <Form.Item
                  label="最大执行步数"
                  name="maxSteps"
                  rules={[{ required: true, message: '请输入最大步数' }]}
                  tooltip="Agent执行任务的最大步数限制"
                >
                  <InputNumber min={1} max={1000} className="w-full" />
                </Form.Item>

                <Form.Item
                  label="每步最大操作数"
                  name="maxActionsPerStep"
                  rules={[{ required: true }]}
                  tooltip="每一步中允许执行的最大操作数量"
                >
                  <InputNumber min={1} max={50} className="w-full" />
                </Form.Item>

                <Form.Item
                  label="Max Input Tokens"
                  name="maxInputTokens"
                  rules={[{ required: true, message: '请输入最大输入Token数' }]}
                  tooltip="模型输入的最大Token数量限制"
                >
                  <InputNumber
                    min={1024}
                    max={1000000}
                    step={1024}
                    className="w-full"
                    formatter={(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  />
                </Form.Item>
              </div>
            </div>

            <Divider className="my-6" />

            {/* 高级设置 */}
            <div className="mb-4">
              <h3 className="text-[14px] font-semibold text-[#333] mb-4 flex items-center">
                <Icon icon="mdi:tune" className="mr-2 text-[#676BEF]" />
                高级设置
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <Form.Item
                  label="Tool Calling Method"
                  name="toolCallingMethod"
                  rules={[{ required: true }]}
                  tooltip="指定LLM调用工具的方式"
                >
                  <Select
                    options={toolCallingMethodOptions}
                    placeholder="选择Tool Calling方式"
                  />
                </Form.Item>

                <Form.Item
                  label="启用视觉模式"
                  name="useVision"
                  valuePropName="checked"
                  tooltip="启用后Agent可以理解页面截图"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  label="Tool Call in Content"
                  name="toolCallInContent"
                  valuePropName="checked"
                  tooltip="将Tool Call内容包含在消息内容中"
                >
                  <Switch />
                </Form.Item>
              </div>
            </div>

            <Form.Item className="mb-0 mt-6">
              <Button type="primary" htmlType="submit" loading={loading} className="w-[160px]">
                保存配置
              </Button>
            </Form.Item>
          </Form>
        </Card>
      ),
    },
    {
      key: 'browser',
      label: (
        <span className="flex items-center">
          <Icon icon="mdi:web" className="mr-2" />
          Browser配置
        </span>
      ),
      children: (
        <Card className="card-shadow">
          <Form
            form={browserForm}
            layout="vertical"
            initialValues={defaultBrowserConfig}
            onFinish={handleSaveBrowser}
          >
            {/* 窗口设置 */}
            <div className="mb-4">
              <h3 className="text-[14px] font-semibold text-[#333] mb-4 flex items-center">
                <Icon icon="mdi:monitor" className="mr-2 text-[#676BEF]" />
                窗口设置
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <Form.Item
                  label="窗口宽度"
                  name="windowWidth"
                  rules={[{ required: true }]}
                >
                  <InputNumber min={800} max={2560} className="w-full" addonAfter="px" />
                </Form.Item>

                <Form.Item
                  label="窗口高度"
                  name="windowHeight"
                  rules={[{ required: true }]}
                >
                  <InputNumber min={600} max={1440} className="w-full" addonAfter="px" />
                </Form.Item>
              </div>
            </div>

            <Divider className="my-6" />

            {/* 录制设置 */}
            <div className="mb-4">
              <h3 className="text-[14px] font-semibold text-[#333] mb-4 flex items-center">
                <Icon icon="mdi:video" className="mr-2 text-[#676BEF]" />
                录制设置
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <Form.Item
                  label="录制保存路径"
                  name="saveRecordingPath"
                  tooltip="浏览器操作录制视频的保存路径"
                >
                  <Input placeholder="例如: ./tmp/recordings" />
                </Form.Item>

                <Form.Item
                  label="Trace保存路径"
                  name="saveTracePath"
                  tooltip="Playwright Trace文件的保存路径"
                >
                  <Input placeholder="例如: ./tmp/traces" />
                </Form.Item>
              </div>
            </div>

            <Divider className="my-6" />

            {/* 安全设置 */}
            <div className="mb-4">
              <h3 className="text-[14px] font-semibold text-[#333] mb-4 flex items-center">
                <Icon icon="mdi:shield" className="mr-2 text-[#676BEF]" />
                安全设置
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <Form.Item
                  label="无头模式 (Headless)"
                  name="headless"
                  valuePropName="checked"
                  tooltip="启用后浏览器将在后台运行，不显示界面"
                >
                  <Switch />
                </Form.Item>

                <Form.Item
                  label="禁用安全限制"
                  name="disableSecurity"
                  valuePropName="checked"
                  tooltip="禁用浏览器安全限制，用于测试环境"
                >
                  <Switch />
                </Form.Item>
              </div>
            </div>

            <Form.Item className="mb-0 mt-6">
              <Button type="primary" htmlType="submit" loading={loading} className="w-[160px]">
                保存配置
              </Button>
            </Form.Item>
          </Form>
        </Card>
      ),
    },
    {
      key: 'llm',
      label: (
        <span className="flex items-center">
          <Icon icon="mdi:brain" className="mr-2" />
          LLM配置
        </span>
      ),
      children: (
        <Card className="card-shadow">
          <Form
            form={llmForm}
            layout="vertical"
            initialValues={{
              provider: 'openai',
              modelName: 'gpt-4o',
              temperature: 1.0,
              baseUrl: '',
              apiKey: '',
              plannerEnabled: false,
              plannerProvider: 'openai',
              plannerModelName: 'gpt-4o-mini',
              plannerTemperature: 0.7,
              plannerBaseUrl: '',
              plannerApiKey: '',
            }}
            onFinish={handleSaveLLM}
          >
            {/* 主LLM配置 */}
            <div className="mb-4">
              <h3 className="text-[14px] font-semibold text-[#333] mb-4 flex items-center">
                <Icon icon="mdi:robot-outline" className="mr-2 text-[#676BEF]" />
                主LLM配置
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <Form.Item
                  label="LLM Provider"
                  name="provider"
                  rules={[{ required: true, message: '请选择Provider' }]}
                >
                  <Select
                    options={llmProviderOptions}
                    placeholder="选择LLM Provider"
                    onChange={handleMainProviderChange}
                  />
                </Form.Item>

                <Form.Item
                  label="模型名称"
                  name="modelName"
                  rules={[{ required: true, message: '请选择模型' }]}
                >
                  <Select
                    options={mainModelOptions}
                    placeholder="选择模型"
                    showSearch
                    filterOption={(input, option) =>
                      (option?.label as string)?.toLowerCase().includes(input.toLowerCase()) ?? false
                    }
                    notFoundContent={
                      <span className="text-[#9297A9] text-[12px]">
                        该Provider暂无预设模型，请手动输入
                      </span>
                    }
                    {...(mainModelOptions.length === 0 ? { mode: undefined } : {})}
                  />
                </Form.Item>

                <Form.Item
                  label="Base URL (可选)"
                  name="baseUrl"
                  tooltip="自定义API端点，留空使用默认"
                >
                  <Input placeholder="https://api.openai.com/v1" />
                </Form.Item>

                <Form.Item
                  label="API Key"
                  name="apiKey"
                  tooltip="留空则使用环境变量中的配置"
                >
                  <Input.Password placeholder="sk-..." />
                </Form.Item>

                <Form.Item
                  label="Temperature"
                  name="temperature"
                  className="col-span-2"
                  tooltip="控制输出的随机性，值越高越有创意"
                >
                  <Slider
                    min={0}
                    max={2}
                    step={0.1}
                    marks={{
                      0: '精确',
                      1: '平衡',
                      2: '创意',
                    }}
                  />
                </Form.Item>
              </div>
            </div>

            <Divider className="my-6" />

            {/* Planner LLM配置 */}
            <div className="mb-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-[14px] font-semibold text-[#333] flex items-center">
                  <Icon icon="mdi:head-lightbulb" className="mr-2 text-[#676BEF]" />
                  Planner LLM配置
                  <span className="ml-2 text-[12px] font-normal text-[#9297A9]">
                    (用于任务规划和分解)
                  </span>
                </h3>
                <Form.Item
                  name="plannerEnabled"
                  valuePropName="checked"
                  className="mb-0"
                >
                  <Switch
                    checkedChildren="启用"
                    unCheckedChildren="禁用"
                    onChange={(checked) => setPlannerEnabled(checked)}
                  />
                </Form.Item>
              </div>

              <div className={`grid grid-cols-2 gap-6 transition-opacity duration-300 ${plannerEnabled ? 'opacity-100' : 'opacity-50 pointer-events-none'}`}>
                <Form.Item
                  label="Planner Provider"
                  name="plannerProvider"
                >
                  <Select
                    options={llmProviderOptions}
                    placeholder="选择Planner Provider"
                    disabled={!plannerEnabled}
                    onChange={handlePlannerProviderChange}
                  />
                </Form.Item>

                <Form.Item
                  label="Planner 模型名称"
                  name="plannerModelName"
                >
                  <Select
                    options={plannerModelOptions}
                    placeholder="选择Planner模型"
                    disabled={!plannerEnabled}
                    showSearch
                    filterOption={(input, option) =>
                      (option?.label as string)?.toLowerCase().includes(input.toLowerCase()) ?? false
                    }
                    notFoundContent={
                      <span className="text-[#9297A9] text-[12px]">
                        该Provider暂无预设模型
                      </span>
                    }
                  />
                </Form.Item>

                <Form.Item
                  label="Planner Base URL (可选)"
                  name="plannerBaseUrl"
                  tooltip="Planner模型的自定义API端点"
                >
                  <Input
                    placeholder="https://api.openai.com/v1"
                    disabled={!plannerEnabled}
                  />
                </Form.Item>

                <Form.Item
                  label="Planner API Key"
                  name="plannerApiKey"
                  tooltip="留空则使用主LLM的API Key"
                >
                  <Input.Password
                    placeholder="留空使用主LLM配置"
                    disabled={!plannerEnabled}
                  />
                </Form.Item>

                <Form.Item
                  label="Planner Temperature"
                  name="plannerTemperature"
                  className="col-span-2"
                  tooltip="Planner模型的Temperature，建议使用较低值以获得更精确的规划"
                >
                  <Slider
                    min={0}
                    max={2}
                    step={0.1}
                    disabled={!plannerEnabled}
                    marks={{
                      0: '精确',
                      0.7: '推荐',
                      2: '创意',
                    }}
                  />
                </Form.Item>
              </div>
            </div>

            <Form.Item className="mb-0 mt-6">
              <Button type="primary" htmlType="submit" loading={loading} className="w-[160px]">
                保存配置
              </Button>
            </Form.Item>
          </Form>
        </Card>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center">
        <Icon icon="mdi:cog" className="text-[24px] text-[#676BEF] mr-3" />
        <h1 className="text-[20px] font-bold text-[#333]">系统配置</h1>
      </div>

      {/* 配置选项卡 */}
      <Tabs
        defaultActiveKey="agent"
        items={tabItems}
        className="bg-white rounded-[8px] p-4"
      />
    </div>
  );
}

export default Settings;
