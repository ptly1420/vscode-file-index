import streamlit as st
from googletrans import Translator, LANGUAGES

def translate_text(text, src_lang, dest_lang):
    translator = Translator(service_urls=['translate.google.com'])
    try:
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception as e:
        return f"Translation error: {str(e)}"

def get_languages():
    return LANGUAGES.keys()

def main():
    st.set_page_config(layout="wide")
    st.title("Responsive Translation Tool")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Input")
        input_text = st.text_area("Enter text to translate:", height=200, key="input_text")
        src_lang = st.selectbox("Select source language:", options=get_languages(), index=list(LANGUAGES.keys()).index('zh-cn'), key="src_lang")
        dest_lang = st.selectbox("Select target language:", options=get_languages(), index=list(LANGUAGES.keys()).index('en'), key="dest_lang")
        if 'translated_text' not in st.session_state and st.button("Translate", key="translate_button"):
            translated_text = translate_text(input_text, src_lang, dest_lang)
            st.session_state.translated_text = translated_text

    with col2:
        st.header("Output")
        if 'translated_text' in st.session_state:
            st.write("Translation result:")
            st.write(st.session_state.translated_text, unsafe_allow_html=True, key="translated_output")

if __name__ == "__main__":
    main()
