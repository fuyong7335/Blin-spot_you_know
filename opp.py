import streamlit as st
import random
from openai import OpenAI

# --- APIキーの設定（streamlit secretsを利用） ---
client = OpenAI(api_key=st.secrets["openai_api_key"])

# --- タイトルと説明 ---
st.set_page_config(page_title="アナタの知らないあなたを診断・本音版", layout="centered")
st.title("アナタの知らないあなたを診断・本音版")
st.markdown("あなたの“無意識の声”に、ちょっと耳をすませてみませんか？")

# --- 質問項目 ---
q1 = st.text_input("Q1：最近、誰かに言われた一言で「なぜか心にひっかかった」言葉はありますか？\n（例：「真面目だね」「冷たいところもあるよね」）")
q2 = st.text_input("Q2：その言葉を聞いた時、どんな気持ちが一瞬よぎりましたか？\n（例：「え、そんなつもりないのに…」「ちょっとドキッとした」）")
q3 = st.text_input("Q3：どんな場面だったか、ざっくりでも思い出せますか？\n（例：「会議のあと」「SNSでやり取り中」）")

st.markdown("---")
st.markdown("### 傾向把握（感情の動き）")
q4 = st.text_input("Q4：その言葉の『何が』引っかかったのだと思いますか？\n（例：「自分ではそう思っていなかった」「図星を突かれた気がした」）")
q5 = st.text_input("Q5：その瞬間、心の中でどんな“つぶやき”がありましたか？\n（例：「それは違うって」「やっぱりそう思われてたか…」）")

st.markdown("---")
st.markdown("### 自己イメージとギャップ")
ideal1 = st.text_input("Q6：あなたはどんな人だと“思われたい”ですか？（1つ目）")
ideal2 = st.text_input("（2つ目）")
ideal3 = st.text_input("（3つ目）")
q7 = st.radio("Q7：その理想と、言われた言葉とのあいだにギャップは感じましたか？", ["はい", "いいえ", "少しある"])

# --- 診断実行ボタン ---
if st.button("診断する"):
    prompt = f"""
あなたは人の心の奥深くを見つめる心理学者でもありカウンセラーでもあります。
次に紹介するユーザーの回答を読んで、その人自身も気づいていないかもしれない一面について、コメントをしてください。
思わず心に響くような、読み手が「深読み」したくなる内容だとうれしいです。
ただし、事実と異なることは言わず、理解しやすい言葉を使ってください。
難しい表現やわかりにくい単語は避けて、親しみやすい話し方でお願いします。
また、自然な日本語で回答してください。
ユーザーの中に見えるもう一人のユーザーを見つけ出し指摘してその性質を生かすためのヒントを丁寧にかつ端的に答えてください。
ユーザーの回答から見えにくい思考や感情のパターンを丁寧に読み取り、
・Assumptions（本人が気づいていない前提）
・Blind Spots（見えにくくなっている死角）
・Action（小さく試せる行動と、その先の可能性）
を日本語で、温かみのある語り口で長くならないようわかりやすく伝えてください。

単に分析結果を伝えるのではなく、
相手が「自分を否定せず、少し前向きに捉え直せる」ような、
安心感とやさしさを込めた言葉で語ってください。


【記述内容】
Q1：{q1}
Q2：{q2}
Q3：{q3}
Q4：{q4}
Q5：{q5}
理想の人物像：{ideal1}, {ideal2}, {ideal3}
ギャップの有無：{q7}
"""

    with st.spinner("診断中..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは優秀な心理カウンセラーで、ユーザーの変化の芽を大切に扱う人物です。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )

    result = response.choices[0].message.content
    st.markdown("---")
    st.subheader("診断結果")
    st.markdown(f"🌀 {result}")
    st.markdown("---")
    final_comments = [
        "いかがでしたか？アナタの自覚していない部分の先端がみえましたか？",
        "あなたの中に、まだ言葉になっていない願いがあるのかもしれませんね。",
        "気づいた“ひとこと”が、明日の行動を変えるヒントになるかもしれません。"
    ]
    st.caption(random.choice(final_comments))
