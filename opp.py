import streamlit as st
from openai import OpenAI

# --- Configuration ---
client = OpenAI(api_key=st.secrets["openai_api_key"])

# --- App Title ---
st.title("あなたの死角はなんだ？！")
st.markdown("""
以下の質問に直感でお答えください。<br>
書きながら、自分でも気づかなかった感情に出会えるかもしれません。
""", unsafe_allow_html=True)

# --- Step 1: 言われて引っかかった言葉 ---
st.header("Step 1: 言われてひっかかった一言")
trigger_word = st.text_input("誰かに言われて、なぜか心にひっかかった一言を教えてください")

# --- Step 2: その時の反応 ---
st.header("Step 2: その時の気持ち")
reaction = st.text_area("その言葉を聞いたとき、どんな気持ちがよぎりましたか？")

# --- Step 3: シチュエーション ---
st.header("Step 3: どんな場面だったか")
context = st.text_area("その一言が出た場面や状況を、ざっくり教えてください")

# --- Step 4: 自分の反応傾向 ---
st.header("Step 4: 反応の傾向")
st.write("あなたの反応に近いものを選んでください（複数可）")
selected_reactions = st.multiselect("反応の傾向", [
    "言われた相手にムッとした",
    "自分を否定された気がした",
    "少し落ち込んだ",
    "なんとなく心に引っかかっている",
    "『確かにそうかも』と思った",
    "特に気にしていない"
])

# --- Step 5: 理想像とギャップ ---
st.header("Step 5: 自分の理想像")
ideal_self = st.text_input("あなたはどんな人だと思われたいですか？（3つまで）")
gap = st.radio("その理想と、言われた言葉とのあいだにギャップを感じましたか？", ["はい", "いいえ", "少しある"])

# --- Analysis Trigger ---
if st.button("AIに分析してもらう"):
    with st.spinner("AIがあなたの死角を分析中..."):
        prompt = f"""
あなたはプロの心理カウンセラーです。
以下のユーザー回答から、その人がまだ気づいていない死角（思考の盲点）を、
Assumptions（思い込み）、Blind Spots（死角）、Action（次の行動）の3つに分けて分析してください。

# ユーザー回答
- 言われた一言: {trigger_word}
- そのときの気持ち: {reaction}
- シチュエーション: {context}
- 反応の傾向: {', '.join(selected_reactions)}
- 理想像: {ideal_self}
- ギャップの有無: {gap}

返答はやさしい語り口でお願いします。
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは共感力の高いカウンセラーです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )

        st.subheader("AI分析結果")
        st.write(response.choices[0].message.content)
        st.markdown("---")
        st.info("この分析をヒントに、あなた自身と静かに向き合う時間を大切にしてくださいね。")
