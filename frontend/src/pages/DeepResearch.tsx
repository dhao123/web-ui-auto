/**
 * DeepResearch - 深度研究页面
 * 专业级设计，无重叠问题
 */
import { useState } from 'react';
import { Button, Input, Card, Steps, Progress, message } from 'antd';
import { Icon } from '@iconify/react';

const { TextArea } = Input;

export function DeepResearch() {
  const [topic, setTopic] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [report, setReport] = useState('');

  const handleStartResearch = async () => {
    if (!topic.trim()) {
      message.warning('请输入研究主题');
      return;
    }

    setCurrentStep(1);
    setProgress(0);
    setReport('');
    message.success('开始深度研究: ' + topic);
    
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setCurrentStep(2);
          setReport(`# ${topic} 研究报告\n\n## 概述\n\n本报告对"${topic}"进行了深入研究...\n\n## 主要发现\n\n1. 发现一\n2. 发现二\n3. 发现三\n\n## 结论\n\n基于以上研究...`);
          return 100;
        }
        return prev + 10;
      });
    }, 1000);
  };

  const handleStopResearch = () => {
    message.info('研究已停止');
  };

  // 步骤配置
  const stepItems = [
    { title: '输入主题', icon: <Icon icon="mdi:text-box-edit" style={{ fontSize: 20 }} /> },
    { title: '执行研究', icon: <Icon icon="mdi:brain" style={{ fontSize: 20 }} /> },
    { title: '生成报告', icon: <Icon icon="mdi:file-check" style={{ fontSize: 20 }} /> },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* 页面标题 */}
      <div className="page-header">
        <div className="page-header-title">
          <div className="page-header-icon">
            <Icon icon="mdi:brain" />
          </div>
          <div className="page-header-text">
            <h1>深度研究</h1>
            <p>AI驱动的深度研究分析，自动生成研究报告</p>
          </div>
        </div>
      </div>

      {/* 主内容卡 */}
      <Card>
        <Steps
          current={currentStep}
          items={stepItems}
          style={{ marginBottom: 40 }}
        />

        {/* 步骤1: 输入主题 */}
        {currentStep === 0 && (
          <div style={{ maxWidth: 800 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
              <div style={{ 
                width: 36, height: 36, borderRadius: 8, 
                background: 'rgba(99, 102, 241, 0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                <Icon icon="mdi:text-box-edit" style={{ color: '#818cf8', fontSize: 18 }} />
              </div>
              <span style={{ fontSize: 16, fontWeight: 600, color: '#ffffff' }}>研究主题</span>
            </div>
            <TextArea
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="请输入研究主题，例如：人工智能在医疗领域的应用现状与发展趋势"
              rows={5}
              style={{ marginBottom: 24, fontSize: 14 }}
            />
            <Button
              type="primary"
              size="large"
              icon={<Icon icon="mdi:rocket-launch" />}
              onClick={handleStartResearch}
              disabled={!topic.trim()}
              style={{ height: 44, padding: '0 28px', fontSize: 15 }}
            >
              开始研究
            </Button>
          </div>
        )}

        {/* 步骤2: 执行中 */}
        {currentStep === 1 && (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 32 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <div style={{ 
                  width: 56, height: 56, borderRadius: 12, 
                  background: 'rgba(99, 102, 241, 0.15)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                  <Icon icon="mdi:brain" style={{ color: '#818cf8', fontSize: 28 }} className="animate-pulse" />
                </div>
                <div>
                  <h3 style={{ fontSize: 18, fontWeight: 600, color: '#ffffff', margin: 0 }}>正在研究: {topic}</h3>
                  <p style={{ fontSize: 14, color: '#8b95a5', margin: '4px 0 0 0' }}>AI正在收集和分析相关信息...</p>
                </div>
              </div>
              <Button danger size="large" icon={<Icon icon="mdi:stop" />} onClick={handleStopResearch} style={{ height: 44 }}>
                停止研究
              </Button>
            </div>

            <div style={{ marginBottom: 32 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <span style={{ fontSize: 14, color: '#8b95a5' }}>研究进度</span>
                <span style={{ fontSize: 16, fontWeight: 700, color: '#818cf8' }}>{progress}%</span>
              </div>
              <Progress 
                percent={progress} 
                status="active"
                showInfo={false}
                strokeColor={{ '0%': '#6366f1', '100%': '#a855f7' }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
              {[
                { icon: 'mdi:web', label: '已搜索网页', value: Math.floor(progress * 0.5), color: '#6366f1' },
                { icon: 'mdi:file-document', label: '已分析文档', value: Math.floor(progress * 0.3), color: '#a855f7' },
                { icon: 'mdi:database', label: '已收集数据', value: Math.floor(progress * 10), color: '#06b6d4' },
              ].map((item, idx) => (
                <div 
                  key={idx}
                  style={{
                    padding: 24,
                    background: '#151b2b',
                    borderRadius: 12,
                    textAlign: 'center',
                    border: '1px solid #2d3748'
                  }}
                >
                  <div style={{ 
                    width: 48, height: 48, borderRadius: 12,
                    background: `${item.color}15`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    margin: '0 auto 12px'
                  }}>
                    <Icon icon={item.icon} style={{ color: item.color, fontSize: 24 }} />
                  </div>
                  <p style={{ fontSize: 13, color: '#8b95a5', margin: 0 }}>{item.label}</p>
                  <p style={{ fontSize: 28, fontWeight: 700, color: '#ffffff', margin: '8px 0 0 0' }}>{item.value}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 步骤3: 报告结果 */}
        {currentStep === 2 && report && (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <div style={{ 
                  width: 56, height: 56, borderRadius: 12, 
                  background: 'rgba(34, 197, 94, 0.15)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                  <Icon icon="mdi:file-check" style={{ color: '#22c55e', fontSize: 28 }} />
                </div>
                <div>
                  <h3 style={{ fontSize: 18, fontWeight: 600, color: '#ffffff', margin: 0 }}>研究报告已生成</h3>
                  <p style={{ fontSize: 14, color: '#8b95a5', margin: '4px 0 0 0' }}>主题: {topic}</p>
                </div>
              </div>
              <div style={{ display: 'flex', gap: 12 }}>
                <Button size="large" icon={<Icon icon="mdi:refresh" />} onClick={() => setCurrentStep(0)} style={{ height: 44 }}>
                  新的研究
                </Button>
                <Button 
                  type="primary" 
                  size="large"
                  icon={<Icon icon="mdi:download" />}
                  style={{ height: 44 }}
                >
                  下载报告
                </Button>
              </div>
            </div>

            <Card style={{ background: '#0f141f', borderColor: '#2d3748' }}>
              <pre style={{ 
                whiteSpace: 'pre-wrap', 
                color: '#b8c0cc', 
                fontFamily: 'JetBrains Mono, monospace',
                fontSize: 14,
                lineHeight: 1.8,
                margin: 0
              }}>
                {report}
              </pre>
            </Card>
          </div>
        )}
      </Card>

      {/* 功能说明 */}
      <Card 
        title={
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ 
              width: 32, height: 32, borderRadius: 8, 
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Icon icon="mdi:book-open" style={{ color: '#818cf8' }} />
            </div>
            <span style={{ fontSize: 15, fontWeight: 600, color: '#ffffff' }}>功能说明</span>
          </div>
        }
      >
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
          {[
            { icon: 'mdi:map-marker-path', title: '智能规划', desc: 'AI自动制定研究计划，分解研究任务' },
            { icon: 'mdi:web-sync', title: '自动搜索', desc: '自动搜索网页、收集信息、分析数据' },
            { icon: 'mdi:file-document-edit', title: '生成报告', desc: '自动生成结构化的研究报告' },
          ].map((item, idx) => (
            <div key={idx} style={{ textAlign: 'center', padding: 24 }}>
              <div style={{ 
                width: 64, height: 64, borderRadius: 16,
                background: 'rgba(99, 102, 241, 0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                margin: '0 auto 16px'
              }}>
                <Icon icon={item.icon} style={{ color: '#818cf8', fontSize: 32 }} />
              </div>
              <h3 style={{ fontSize: 16, fontWeight: 600, color: '#ffffff', margin: '0 0 8px 0' }}>{item.title}</h3>
              <p style={{ fontSize: 14, color: '#8b95a5', margin: 0 }}>{item.desc}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

export default DeepResearch;
