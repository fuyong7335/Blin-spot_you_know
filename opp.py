import streamlit as st
from openai import OpenAI

# --- OpenAI API Key ---
client = OpenAI(api_key=st.secrets["openai_api_key"])

# --- App Title ---
st.title("あなたの知らないあなた 診断アプリ")
st.markdown("### 心のひっかかりから、あなたの死角をAIが優しく見つめます。")

# --- Step 1: 自由記述 ---
st.header("🌀 ステップ1：深層にアクセスする自由記述")
q1 = st.text_input("Q1：最近、誰かに言われた一言で『なぜか心にひっかかった』言葉はありますか？")
q2 = st.text_input("Q2：その言葉を聞いた時、どんな気持ちが一瞬よぎりましたか？")
q3 = st.text_input("Q3：どんな場面だったか、ざっくりでも思い出せますか？")

# --- Step 2: 選択式補足 ---
st.header("🧭 ステップ2：反応傾向の補足")
q4 = st.multiselect("Q4：あなたの反応に近いものを選んでください（複数可）", [
    "言われた相手にムッとした",
    "自分を否定された気がした",
    "少し落ち込んだ",
    "なんとなく心に引っかかっている",
    "『確かにそうかも』と思った",
    "特に気にしていない"
])

# --- Step 3: 自己イメージとギャップ ---
st.header("🪞 ステップ3：現在の自己イメージ")
q5 = st.text_input("Q5：あなたは自分をどんな人だと“思われたい”ですか？（3つまで自由入力）")
q6 = st.radio("Q6：その理想と、言われた言葉とのあいだにギャップは感じましたか？", ["はい", "いいえ", "少しある"])

# --- Submit ---
if st.button("診断する"):
    with st.spinner("AIがあなたの死角を分析中です..."):
        prompt = f"""
あなたはプロの心理カウンセラーです。
以下のユーザー回答から、本人がまだ気づいていない思考の傾向や死角を、
語りかけるような自然な口調で優しく分析し、
【Assumptions（前提）】【Blind Spots（死角）】【Action（次の行動）】の3つの観点でまとめてください。

---
Q1: {q1}
Q2: {q2}
Q3: {q3}
Q4: {', '.join(q4)}
Q5: {q5}
Q6: {q6}
"""
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは共感力の高い心理カウンセラーで、思いやりのあるフィードバックを提供します。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=600
        )
        st.subheader("🧠 AI診断結果")
        st.write(res.choices[0].message.content)
        st.info("この診断はあなた自身を責めるためのものではありません。あなたの中にある思いが、静かに姿を見せてくれただけなのです🌿")
