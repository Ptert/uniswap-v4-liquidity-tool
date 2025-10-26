# GitHub Pages 部署指南

## 部署步骤

### 1. 创建 GitHub 仓库
1. 登录 GitHub 账户
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 仓库名称建议：`uniswap-v4-liquidity-tool`
4. 设置为 Public（GitHub Pages 免费版需要公开仓库）
5. 不要初始化 README、.gitignore 或 license（我们已经有了）

### 2. 推送代码到 GitHub
在项目目录中执行以下命令：

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/uniswap-v4-liquidity-tool.git

# 推送代码到 GitHub
git branch -M main
git push -u origin main
```

### 3. 启用 GitHub Pages
1. 在 GitHub 仓库页面，点击 "Settings" 选项卡
2. 在左侧菜单中找到 "Pages"
3. 在 "Source" 部分选择 "Deploy from a branch"
4. 选择 "main" 分支和 "/ (root)" 文件夹
5. 点击 "Save"

### 4. 访问网站
- GitHub Pages 会在几分钟内部署完成
- 访问地址：`https://YOUR_USERNAME.github.io/uniswap-v4-liquidity-tool/`
- 主页：`https://YOUR_USERNAME.github.io/uniswap-v4-liquidity-tool/index.html`
- 工具页面：`https://YOUR_USERNAME.github.io/uniswap-v4-liquidity-tool/unlock-data-generator.html`

## 文件结构说明

```
/
├── index.html                    # 主页（GitHub Pages 默认页面）
├── unlock-data-generator.html    # UnlockData 生成器工具页面
├── README.md                     # 项目说明文档
├── .gitignore                   # Git 忽略文件配置
└── deploy-instructions.md       # 部署指南（本文件）
```

## 注意事项

1. **HTTPS 要求**：GitHub Pages 强制使用 HTTPS，确保所有外部资源（如 CDN）也使用 HTTPS
2. **缓存问题**：如果更新后没有立即生效，可能是浏览器缓存问题，尝试强制刷新（Ctrl+F5）
3. **自定义域名**：如果需要使用自定义域名，可以在 Pages 设置中配置
4. **更新网站**：只需要推送新的提交到 main 分支，GitHub Pages 会自动重新部署

## 本地测试

在部署前，可以在本地测试：

```bash
# 启动本地服务器
python -m http.server 8000

# 访问 http://localhost:8000
```

## 故障排除

1. **页面 404**：检查文件名是否正确，确保 index.html 存在
2. **JavaScript 错误**：打开浏览器开发者工具查看控制台错误
3. **部署失败**：检查 GitHub Actions 页面查看部署日志