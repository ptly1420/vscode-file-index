import streamlit as st
from googletrans import Translator, LANGUAGES

# 定义翻译函数，接收文本、源语言和目标语言作为参数
def translate_text(text, src_lang, dest_lang):
    # 创建翻译器对象，指定翻译服务的URL
    translator = Translator(service_urls=['translate.google.com'])
    try:
        # 使用翻译器对象进行翻译，返回翻译结果
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception as e:
        # 如果翻译过程中出现异常，返回错误信息
        return f"Translation error: {str(e)}"

# 获取所有支持的语言
def get_languages():
    return LANGUAGES.keys()

# 主函数
def main():
    # 设置页面布局为宽屏
    st.set_page_config(layout="wide")
    st.title("Responsive Translation Tool")
    
# 创建两列，分别为col1和col2
    col1, col2 = st.columns([1, 2])

    # 在col1中添加标题和文本输入框
    with col1:
        st.header("Input")
        input_text = st.text_area("Enter text to translate:", height=200, key="input_text")
        # 从LANGUAGES字典中获取语言列表，并设置默认值为中文
        src_lang = st.selectbox("Select source language:", options=get_languages(), index=list(LANGUAGES.keys()).index('zh-cn'), key="src_lang")
        # 从LANGUAGES字典中获取语言列表，并设置默认值为英文
        dest_lang = st.selectbox("Select target language:", options=get_languages(), index=list(LANGUAGES.keys()).index('en'), key="dest_lang")
        # 如果session_state中没有translated_text，并且点击了Translate按钮，则调用translate_text函数进行翻译
        if 'translated_text' not in st.session_state and st.button("Translate", key="translate_button"):
            translated_text = translate_text(input_text, src_lang, dest_lang)
            st.session_state.translated_text = translated_text

    # 在col2中添加标题和翻译结果输出框
    with col2:
        st.header("Output")
        # 如果session_state中有translated_text，则输出翻译结果
        if 'translated_text' in st.session_state:
            st.write("Translation result:")
            st.write(st.session_state.translated_text, unsafe_allow_html=True, key="translated_output")

if __name__ == "__main__":
    main()
