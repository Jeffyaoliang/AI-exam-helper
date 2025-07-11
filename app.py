import streamlit as st
import google.generativeai as genai
import pdfplumber
import os
import json

# 推荐用环境变量管理 API Key
API_KEY = os.environ.get("GEMINI_API_KEY", "你的_Gemini_API_Key")

def extract_text_from_pdf(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"PDF解析失败: {str(e)}"

def call_gemini(prompt, model="gemini-2.5-flash", api_key=API_KEY):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_outline(text, api_key=API_KEY):
    prompt = (
        "请根据以下内容，提炼出结构化的复习大纲，分层级展示，使用有条理的短语或句子：\n"
        f"{text}\n"
        "请用Markdown格式输出，主标题用#，二级用##，三级用###，不要有多余解释。"
    )
    return call_gemini(prompt, api_key=api_key)

def generate_qa(text, max_questions=5, api_key=API_KEY):
    prompt = (
        f"请根据以下内容，生成{max_questions}道典型考题及标准答案，题型以简答题为主，内容覆盖重点知识点：\n"
        f"{text}\n"
        "请用如下格式输出：\n"
        "【问题】xxx\n【答案】xxx\n"
    )
    return call_gemini(prompt, api_key=api_key)

def generate_mindmap(text, api_key=API_KEY):
    prompt = (
        "请根据以下内容，生成结构化的思维导图，使用Markdown格式，主标题用#，二级用##，三级用###，"
        "内容要分层、条理清晰，突出知识点之间的关系。只输出Markdown，不要有多余解释。\n"
        f"{text}"
    )
    return call_gemini(prompt, api_key=api_key)

def create_markmap_html(markdown_content):
    # 防止 Markdown 里的反引号和 ${ 导致 JS 语法错误
    markdown_content = markdown_content.replace('`', '\\`').replace('${', '\\${')
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            #mindmap {{
                width: 100%;
                height: 600px;
                margin: 0;
                padding: 0;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.14.3/dist/browser/index.min.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            window.onload = async () => {{
                try {{
                    const markdown = `{markdown_content}`;
                    const transformer = new markmap.Transformer();
                    const {{root}} = transformer.transform(markdown);
                    const mm = new markmap.Markmap(document.querySelector('#mindmap'), {{
                        maxWidth: 300,
                        color: (node) => {{
                            const level = node.depth;
                            return ['#2196f3', '#4caf50', '#ff9800', '#f44336'][level % 4];
                        }},
                        paddingX: 16,
                        autoFit: true,
                        initialExpandLevel: 2,
                        duration: 500,
                    }});
                    mm.setData(root);
                    mm.fit();
                }} catch (error) {{
                    console.error('Error rendering mindmap:', error);
                    document.body.innerHTML = '<p style="color: red;">Error rendering mindmap. Please check the console for details.</p>';
                }}
            }};
        </script>
    </body>
    </html>
    """
    return html_content
st.set_page_config(page_title="PDF自动复习助手", layout="wide")
st.title("📚 PDF自动复习助手：大纲 + 考题 + 思维导图 (Gemini)")

uploaded_file = st.file_uploader("上传PDF文件", type=["pdf"])
max_questions = st.slider("考题数量", 3, 20, value=5)
api_key = st.text_input("Gemini API Key（建议用环境变量，不建议明文填写）", value=API_KEY, type="password")

if uploaded_file is not None:
    with st.spinner("正在解析PDF并生成内容..."):
        text = extract_text_from_pdf(uploaded_file)
        if not text or text.startswith("PDF解析失败"):
            st.error(text)
        else:
            outline_md = generate_outline(text, api_key)
            qa_md = generate_qa(text, max_questions, api_key)
            mindmap_md = generate_mindmap(text, api_key)
            st.subheader("📝 复习大纲")
            st.text_area("大纲 Markdown", outline_md, height=200)
            st.subheader("📚 考题与答案")
            st.text_area("考题 Markdown", qa_md, height=200)
            st.subheader("🌳 思维导图 Markdown")
            st.text_area("思维导图 Markdown", mindmap_md, height=200)
            st.download_button("⬇️ 下载思维导图 Markdown", mindmap_md, file_name="mindmap.md", mime="text/markdown")
            st.subheader("🌳 交互式思维导图")
            st.components.v1.html(create_markmap_html(mindmap_md), height=700, scrolling=True)