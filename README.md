---

项目名称：PDF自动复习助手

简介：  
本项目是一个基于 Streamlit 的 AI 应用，支持上传 PDF 文档，自动生成复习大纲、典型考题和交互式思维导图，帮助用户高效梳理和复习知识。核心功能依赖 Google Gemini 大模型和 Markmap 思维导图可视化。

主要功能：
- 支持 PDF 文件上传，自动提取文本内容。
- 调用 Gemini API 智能生成分层级的复习大纲（Markdown 格式）。
- 自动生成覆盖重点知识点的典型考题及标准答案。
- 生成结构化思维导图，并用 Markmap 交互式渲染，支持 Markdown 下载。
- 支持用户自定义 Gemini API Key，默认使用部署者环境变量，安全不泄露。

使用方法：
1. 克隆项目并安装依赖：
   - `git clone https://github.com/你的用户名/pdf-mindmap-app.git`
   - `cd pdf-mindmap-app`
   - `pip install -r requirements.txt`

2. 配置 Gemini API Key（两种方式，推荐第一种）：
   - 在本地环境变量中设置 GEMINI_API_KEY（推荐，安全）：
     - Windows：`set GEMINI_API_KEY=你的APIKEY`
     - Linux/Mac：`export GEMINI_API_KEY=你的APIKEY`
   - 或在页面输入框手动填写（不会被保存）。

3. 启动应用：
   - `streamlit run app.py`
   - 默认本地访问地址：http://localhost:8501

云端部署（Streamlit Community Cloud）：
- 将代码上传到 GitHub。
- 登录 [Streamlit Cloud](https://streamlit.io/cloud)，新建 App，选择你的仓库和 app.py。
- 在“Settings”→“Secrets”中添加 GEMINI_API_KEY。
- 部署后即可获得公网访问链接。

依赖说明：
- streamlit
- google-generativeai
- pdfplumber
- 详见 requirements.txt

安全说明：
- 请勿在代码中明文写入 API Key。
- 推荐用环境变量或 Streamlit secrets 管理 Key，页面输入框仅作临时使用。

免责声明：
- 本项目仅供学习与交流，API Key 使用请遵守 Google Gemini 官方政策。

贡献说明：
- 欢迎提交 Issue 或 PR 共同完善项目。

---

如需进一步精简、英文版或带示例图片的说明，请随时告知！