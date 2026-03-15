# 贡献指南

欢迎为 AI Agent Builder Lite 项目做出贡献！本指南将帮助你开始贡献。

## 🎯 贡献方式

### 1. 报告问题
- 使用 [GitHub Issues](https://github.com/TikatAK/ai-agent-builder-lite/issues) 报告bug
- 在创建issue前，请先搜索是否已有类似问题
- 提供清晰的问题描述、重现步骤和环境信息

### 2. 功能请求
- 描述你想要的功能
- 解释为什么这个功能有用
- 提供使用场景示例

### 3. 代码贡献
- Fork项目仓库
- 创建功能分支
- 提交更改
- 创建Pull Request

## 🛠️ 开发环境设置

### 前提条件
- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- Git

### 步骤1：克隆仓库
```bash
git clone https://github.com/TikatAK/ai-agent-builder-lite.git
cd ai-agent-builder-lite
```

### 步骤2：设置后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 步骤3：设置前端
```bash
cd frontend
npm install
```

### 步骤4：启动服务
```bash
# 启动数据库和消息队列
docker-compose up -d postgres redis rabbitmq

# 启动后端
cd backend
uvicorn app.main:app --reload

# 启动前端
cd frontend
npm run dev
```

## 📝 代码规范

### Python代码
- 使用Black进行代码格式化
- 使用isort进行导入排序
- 遵循PEP 8规范
- 类型提示（Type Hints）

```bash
# 格式化Python代码
black .
isort .
```

### TypeScript/JavaScript代码
- 使用Prettier进行代码格式化
- 使用ESLint进行代码检查
- 遵循Airbnb代码风格

```bash
# 格式化前端代码
npm run format
npm run lint
```

### 提交信息规范
使用[Conventional Commits](https://www.conventionalcommits.org/)规范：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

示例：
```
feat(agent): 添加Agent创建功能

- 实现Agent创建API
- 添加Agent模型验证
- 更新相关测试

Closes #123
```

## 🧪 测试

### 运行测试
```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

### 测试覆盖率
```bash
# 后端测试覆盖率
cd backend
pytest --cov=app --cov-report=html

# 打开覆盖率报告
open htmlcov/index.html
```

## 📚 文档

### 更新文档
- API文档：更新OpenAPI规范
- 用户文档：更新README和docs/
- 开发文档：更新CONTRIBUTING.md

### 文档格式
- 使用Markdown格式
- 包含代码示例
- 添加必要的截图或图表

## 🔧 架构指南

### 添加新技能
1. 在 `backend/app/services/skills/` 创建新文件
2. 继承 `BaseSkill` 类
3. 实现必要的方法
4. 注册到技能管理器
5. 添加测试

### 添加新AI模型
1. 在 `backend/app/core/llm/` 创建新文件
2. 继承 `BaseLLM` 类
3. 实现必要的方法
4. 添加到模型工厂
5. 添加测试

### 数据库迁移
```bash
# 创建新迁移
cd backend
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 🚀 发布流程

### 版本号
使用[语义化版本](https://semver.org/)：
- `MAJOR`: 不兼容的API修改
- `MINOR`: 向下兼容的功能性新增
- `PATCH`: 向下兼容的问题修正

### 发布步骤
1. 更新版本号
2. 更新CHANGELOG.md
3. 创建发布分支
4. 运行完整测试
5. 创建GitHub Release
6. 更新部署配置

## 🤝 行为准则

### 沟通准则
- 保持尊重和友好
- 提供建设性反馈
- 耐心帮助新贡献者
- 使用包容性语言

### 代码审查
- 及时审查PR
- 提供具体、有建设性的反馈
- 感谢贡献者的工作
- 保持专业态度

## 📞 获取帮助

### 问题解决
1. 查看文档和现有issue
2. 在Discussions中提问
3. 联系维护者

### 联系方式
- GitHub Issues: 技术问题
- GitHub Discussions: 讨论和问题
- Email: 项目维护者

## 🙏 致谢

感谢所有贡献者的努力！你的每一份贡献都让这个项目变得更好。

---

**让我们一起构建更好的AI Agent平台！** 🚀