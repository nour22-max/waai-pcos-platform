import streamlit as st
from google import genai

st.set_page_config(
    page_title="وعي | صحة المرأة",
    page_icon="🌿",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #F5F8F7;
}
h1, h2, h3, p, label {
    text-align: right;
}
[data-testid="stChatMessage"] {
    direction: rtl;
}
[data-testid="stChatInput"] {
    direction: rtl;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 وعي")
st.subheader("مساحة للتوعية بتكيس المبايض ومقاومة الإنسولين")

st.info(
    "منصة للتثقيف الصحي، وليست بديلًا عن التشخيص أو "
    "استشارة الطبيب."
)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(
        api_key=api_key,
        http_options={"timeout": 120000}
    )
except Exception as error:
    st.error(
        "تعذّر تحميل إعدادات الاتصال. "
        "تأكدي من ملف .streamlit/secrets.toml."
    )
    st.stop()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("اكتبي سؤالك الصحي هنا...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("جاري إعداد الإجابة..."):
            try:
                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=(
                        "أنت مساعد للتثقيف الصحي باللغة العربية. "
                        "قدّم معلومات عامة عن تكيس المبايض "
                        "ومقاومة الإنسولين. لا تشخّص الحالات "
                        "ولا تصف علاجًا شخصيًا.\n\n"
                        f"سؤال المستخدم: {question}"
                    )
                )
                answer = response.output_text or "لم تصل إجابة من النموذج."

            except Exception as error:
                answer = (
                    "تعذّر الحصول على إجابة من Gemini.\n\n"
                    f"تفاصيل الخطأ: {error}"
                )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })