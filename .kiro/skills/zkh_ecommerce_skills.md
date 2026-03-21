# 震坤行电商测试技能库

## 技能概述
本技能库为震坤行（zkh.com）电商平台自动化测试提供结构化、可复用的技能模块。

## 核心技能

### 1. zkh_login_skill - 登录技能
**目标**：完成震坤行网站登录
**输入参数**：
- username: 用户名/手机号
- password: 密码

**执行步骤**：
1. 导航到 zkh.com
2. 等待页面加载完成（检查登录按钮是否可见）
3. 点击登录按钮/链接
4. 输入用户名到用户名输入框
5. 输入密码到密码输入框
6. 点击登录提交按钮
7. 等待登录完成（检查用户信息或退出按钮是否出现）
8. 验证登录状态

**成功标准**：
- 页面URL包含用户中心或首页
- 页面中出现用户名或"退出登录"按钮
- 无错误提示信息

**失败处理**：
- 如果出现验证码，使用 ask_for_assistant 请求人工协助
- 如果登录失败，记录错误信息并返回失败状态
- 最多重试2次

---

### 2. zkh_search_skill - 商品搜索技能
**目标**：在震坤行网站搜索指定商品
**输入参数**：
- search_query: 搜索关键词（如"AIGO/爱国者 鼠标 Q710 黑色"）

**执行步骤**：
1. 定位搜索框元素
2. 清空搜索框（如果有内容）
3. 输入搜索关键词
4. 点击搜索按钮或按Enter键
5. 等待搜索结果页面加载（检查商品列表是否出现）
6. 验证搜索结果是否包含目标商品

**成功标准**：
- 搜索结果页面加载完成
- 商品列表中至少有一个结果
- 页面URL包含搜索关键词或search参数

**失败处理**：
- 如果搜索框未找到，尝试刷新页面重试
- 如果搜索无结果，返回空结果状态
- 如果页面加载超时，使用 mcp.zkh-ecommerce.wait_for_element 工具

---

### 3. zkh_price_extract_skill - 价格提取技能
**目标**：从商品详情或列表中提取未税价格
**输入参数**：
- product_name: 商品名称（用于定位）
- price_type: 价格类型（"untaxed" 或 "taxed"）

**执行步骤**：
1. 定位目标商品元素
2. 查找价格相关元素（优先查找"未税价"、"不含税价格"等标识）
3. 使用 mcp.zkh-ecommerce.extract_price 工具提取价格数值
4. 验证价格格式（必须是数字，可能包含小数点）
5. 返回提取的价格

**成功标准**：
- 成功提取到数字格式的价格
- 价格大于0
- 价格单位为人民币（元）

**失败处理**：
- 如果价格元素未找到，尝试滚动页面后重试
- 如果价格格式异常，记录原始文本并返回错误
- 使用 extract_page_content 提取完整页面内容辅助定位

---

### 4. zkh_add_to_cart_skill - 加购技能
**目标**：将商品添加到购物车
**输入参数**：
- product_name: 商品名称
- quantity: 数量（默认1）

**执行步骤**：
1. 确认当前在商品详情页或列表页
2. 定位"加入购物车"或"立即购买"按钮
3. 如果需要选择规格，先选择规格
4. 设置购买数量（如果quantity > 1）
5. 点击加购按钮
6. 等待加购反馈（弹窗、提示信息或购物车数量变化）
7. 使用 mcp.zkh-ecommerce.verify_cart_status 验证加购成功

**成功标准**：
- 出现"加入购物车成功"提示
- 购物车图标数量增加
- 或弹出购物车确认弹窗

**失败处理**：
- 如果按钮不可点击，检查是否需要登录
- 如果库存不足，记录错误信息
- 如果加购失败，使用 mcp.zkh-ecommerce.capture_network 捕获网络请求分析原因

---

### 5. zkh_verify_skill - 验证技能
**目标**：验证测试用例的预期结果
**输入参数**：
- verification_items: 验证项列表
  - type: 验证类型（"price_match", "cart_success", "element_exists"等）
  - expected: 期望值
  - actual: 实际值

**执行步骤**：
1. 遍历所有验证项
2. 根据验证类型执行对应的验证逻辑
3. 记录每个验证项的结果（通过/失败）
4. 汇总验证结果

**验证类型**：
- **price_match**: 价格匹配验证
  - 比较实际价格与期望价格
  - 支持精确匹配和范围匹配
- **cart_success**: 加购成功验证
  - 检查购物车状态
  - 验证商品是否在购物车中
- **element_exists**: 元素存在验证
  - 检查指定元素是否存在
  - 支持文本内容验证

**成功标准**：
- 所有验证项均通过
- 返回详细的验证报告

**失败处理**：
- 记录失败的验证项及原因
- 返回失败状态和详细报告

---

## 技能使用示例

### 完整测试用例执行流程
```
任务: "打开震坤行官网zkh.com，用账号18614277918，密码test.123登录, 
      搜索'AIGO/爱国者 鼠标 Q710 黑色 1个' 找到未税价格并加购，
      判断未税价格是否是18.50，加购是否成功"

执行步骤:
1. 使用 zkh_login_skill
   - username: "18614277918"
   - password: "test.123"
   
2. 使用 zkh_search_skill
   - search_query: "AIGO/爱国者 鼠标 Q710 黑色"
   
3. 使用 zkh_price_extract_skill
   - product_name: "AIGO/爱国者 鼠标 Q710 黑色"
   - price_type: "untaxed"
   
4. 使用 zkh_add_to_cart_skill
   - product_name: "AIGO/爱国者 鼠标 Q710 黑色"
   - quantity: 1
   
5. 使用 zkh_verify_skill
   - verification_items:
     - {type: "price_match", expected: 18.50, actual: <extracted_price>}
     - {type: "cart_success", expected: true, actual: <cart_status>}
```

---

## 技能编排原则

1. **顺序执行**：技能按依赖关系顺序执行（登录 → 搜索 → 提取 → 加购 → 验证）
2. **状态传递**：前一个技能的输出作为后一个技能的输入
3. **错误隔离**：单个技能失败不影响其他技能的执行（除非有强依赖）
4. **重试机制**：每个技能内部实现重试逻辑，避免Agent层重复重试
5. **可观测性**：每个技能记录详细的执行日志和指标

---

## 与MCP工具的协作

技能层调用MCP工具层的映射关系：
- zkh_price_extract_skill → mcp.zkh-ecommerce.extract_price
- zkh_add_to_cart_skill → mcp.zkh-ecommerce.verify_cart_status
- 所有技能 → mcp.zkh-ecommerce.wait_for_element（智能等待）
- 调试场景 → mcp.zkh-ecommerce.capture_network（网络分析）

---

## 注意事项

1. **动态元素处理**：震坤行网站可能使用动态加载，需要合理使用等待机制
2. **反爬虫应对**：如遇验证码或风控，及时使用 ask_for_assistant
3. **价格格式**：注意区分含税价和未税价，提取时需明确标识
4. **购物车状态**：加购后需等待足够时间让购物车状态更新
5. **网络波动**：使用 mcp.zkh-ecommerce.capture_network 监控网络请求，辅助问题定位
