# 问题与修复记录

## 问题追踪：避免重复犯错

---

### 1. MiniMax API 端点错误
**问题**：Humanize 和 Detect 接口返回 404
**原因**：代码中 API 端点 URL 有空格 `/v1/text detection` 和 `/v1/text generation`
**解决方案**：修正为 `/v1/text/chatcompletion_v2`
**涉及文件**：`backend/app/services/ai_provider/minimax.py`

---

### 2. 前端 API 响应解析错误
**问题**：配额显示 0/5，前端报错 "Daily quota exhausted"
**原因**：后端返回裸 JSON（无包装），但前端代码期望 `response.data.data`
**解决方案**：修改前端 `api.ts`，所有接口返回 `response.data` 而非 `response.data.data!`
**涉及文件**：`frontend/src/services/api.ts`

---

### 3. Humanize 语言丢失问题
**问题**：输入中文，输出变成英文
**原因**：MiniMax 模型未强制保持输入语言
**解决方案**：
- 添加 `_detect_language()` 方法自动检测输入语言
- 在 API 请求中强制指定输出语言
**涉及文件**：`backend/app/services/ai_provider/minimax.py`

---

### 4. AI 检测结果不准确（第一版）
**问题**：检测结果过于简单，只有概率数字，没有分析原因
**原因**：检测提示词不够精确，缺乏中文 AI 特征指导
**解决方案**：优化 `_build_detection_prompt()`，添加：
- 中文 AI 常见模式识别（"深刻改变"、"赋能"、"生态"等）
- 人类写作特征指导
- 更客观的评估规则
**涉及文件**：`backend/app/services/ai_provider/minimax.py`

---

### 9. AI 检测分析粒度不足
**问题**：检测结果缺乏语义分析和具体原因，只显示概率数字
**原因**：
- 提示词不够简洁，导致响应被截断（finish_reason: "length"）
- 缺乏对具体 AI 特征模式的识别
**解决方案**：
- 简化提示词，减少 token 使用
- 添加 `chunks` 数组，每块包含语义文本、概率、级别、分析原因
- 添加 `ai_markers` 和 `human_markers` 列表
- 添加 `summary` 总结
- 更新解析逻辑 `_parse_detection_result()` 支持新格式
- 更新数据结构（DetectResult、DetectResponse、SentenceAnalysis）
- 更新前端 SentenceCard 组件显示 reason
- 更新前端 DetectView 显示 patterns 标签
**涉及文件**：
- `backend/app/services/ai_provider/minimax.py`
- `backend/app/services/ai_provider/base.py`
- `backend/app/routers/detect.py`
- `backend/app/schemas/detect.py`
- `frontend/src/types/index.ts`
- `frontend/src/components/SentenceCard.vue`
- `frontend/src/views/DetectView.vue`

---

### 5. Humanize 跳转按钮无反应
**问题**：Detect 页面点击 "Humanize High-Probability Sentences" 按钮没反应
**原因**：`goToHumanize()` 函数只处理 `level === "high"` 的句子，如果没有则不跳转
**解决方案**：修改为获取所有句子进行 humanize
**涉及文件**：`frontend/src/views/DetectView.vue`

---

### 6. 语言自动检测缺失
**问题**：粘贴中文文本，语言标签仍显示英文
**原因**：前端 `lang` 变量默认值是 "en"，没有自动检测
**解决方案**：
- 添加 `detectLanguage()` 函数，基于中文字符比例检测语言
- 添加 `watch` 监听文本变化自动更新语言
- 在 `onMounted` 中初始化语言检测
**涉及文件**：`frontend/src/views/DetectView.vue`、`frontend/src/views/HumanizeView.vue`

---

### 7. Redis 配额被测试请求消耗
**问题**：测试过程中配额耗尽，无法测试功能
**原因**：curl 测试调用消耗了每日配额
**解决方案**：测试前执行 `docker exec unbot_redis redis-cli FLUSHDB` 重置配额
**注意**：开发测试时注意配额消耗

---

### 8. Vite 热更新未生效
**问题**：修改后端代码后 API 行为未变化
**原因**：Python 模块缓存
**解决方案**：执行 `docker restart unbot_backend` 重启容器

---

### 10. 句子被错误分割，版本号被拆分
**问题**：如 "2026.3.22" 被拆成 "2026"、"3"、"22"，编号 "1. 2. 3." 被单独成句
**原因**：
- MiniMax 模型倾向于按标点符号分割，导致版本号被错误拆分
- 提示词中的规则不足以阻止模型分割版本号
**解决方案**：
- 放弃让模型分割句子的方案
- 简化提示词，只让模型返回整体 AI 概率、AI特征词、人类特征词
- 在后端用 Python 的 `_split_sentences()` 方法按中文句号、感叹号、问号、换行符分割句子
- 这种方式确保句子完整，版本号、数字编号不会被拆分
**涉及文件**：`backend/app/services/ai_provider/minimax.py`
**经验教训**：
- 大模型不适合做精确的文本分割任务
- 将复杂任务拆分为"模型做判断 + 代码做处理"的模式更可靠

---

### 12. DetectView.vue 语法错误
**问题**：`goToHumanize()` 函数后出现重复闭合括号 `}`, 导致组件解析失败
**原因**：编辑时多余复制了 `}` 符号
**解决方案**：删除重复的闭合括号
**涉及文件**：`frontend/src/views/DetectView.vue`

---

### 11. URL 文本传递安全隐患
**问题**：长文本通过 URL query 参数传递，导致 URL 过长且文本内容暴露在浏览器历史中
**原因**：使用 `router.push({ name: "detect", query: { text: ... } })` 传递文本
**解决方案**：
- 创建 Pinia Store `useTextStore` 管理待处理文本
- `HomeView.vue` 使用 `textStore.setText()` 存储文本
- `DetectView.vue` 和 `HumanizeView.vue` 在 `onMounted` 时从 store 读取并清空
- 页面跳转不再携带 URL 参数
**涉及文件**：
- `frontend/src/stores/text.ts`（新建）
- `frontend/src/views/HomeView.vue`
- `frontend/src/views/DetectView.vue`
- `frontend/src/views/HumanizeView.vue`

---

### 13. bcrypt 与 passlib 版本不兼容
**问题**：用户注册时返回 "服务器内部错误"
**原因**：`bcrypt 5.0.0` 与 `passlib 1.7.4` 存在兼容性问题
**解决方案**：在 `requirements.txt` 中固定 `bcrypt==4.1.2`
**涉及文件**：`backend/requirements.txt`

---

### 14. Pydantic 无法验证 SQLAlchemy 模型
**问题**：注册接口返回 ValidationError
**原因**：`UserResponse` 需要 `from_attributes = True` 才能从 ORM 模型创建
**解决方案**：在 `backend/app/schemas/auth.py` 的 `UserResponse` 配置中添加 `"from_attributes": True`
**涉及文件**：`backend/app/schemas/auth.py`

---

### 15. /me 接口无法获取 Authorization Header
**问题**：登录成功后，调用 `/me` 接口返回 "令牌无效或已过期"
**原因**：`get_current_user` 函数的 `authorization` 参数未使用 `Header()` 声明，无法从请求头获取
**解决方案**：
- 导入 `Header` 和 `Optional`
- 将 `authorization: str = None` 改为 `authorization: Optional[str] = Header(None)`
**涉及文件**：`backend/app/routers/auth.py`

---

## 自我纠错检查清单

修改代码前，先检查：
1. 查看本文件确认是否为已知问题
2. 确认修改涉及前端还是后端
3. 后端修改需要重启 Docker 容器
4. 测试前确保 Redis 配额已重置
5. 检查前端缓存，必要时强制刷新
