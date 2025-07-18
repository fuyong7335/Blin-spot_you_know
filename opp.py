import streamlit as st
from openai import OpenAI

# --- Configuration ---
client = OpenAI(api_key=st.secrets["openai_api_key"])

# --- App Title ---
st.title("あなたの死角はなんだ？！")
st.markdown("簡単な質問に答えることで、あなたの盲点（死角）をAIが分析します。")

# --- Data Definitions ---
KEYWORDS = [
    "明るい", "穏やか", "活発", "真面目", "社交的", "自由奔放", "論理的", "感情的",
    "嫉妬深い", "自己中心的", "ネガティブ思考", "打算的", "依存", "秘密主義", "臆病",
    "優柔不断", "短気", "冷淡", "執着心", "被害妄想的", "完璧主義", "八方美人",
    "腹黒い", "負けず嫌い", "自己否定的", "人見知り", "ナルシスト", "流されやすい",
    "責任転嫁", "裏表", "心配性", "過干渉", "マイペース", "サボり癖"
]
REACTIONS = [
    "イラつく", "嫌悪感がある", "違和感がある", "むずむずする",
    "関係ないと思う", "なんとなくだが気になる", "あまりピンとこない", "周りにはいないタイプだ"
]
SCENARIOS = [
    ("会議で発言後、同僚から『〇〇なんだね』と意外な評価をされた",
     ["強く驚いた", "少し戸惑った", "あまり気にしていない"]),
    ("SNS投稿時、フォロワーから思いがけないリアクションが返ってきた",
     ["強く驚いた", "少し戸惑った", "あまり気にしていない"]),
    ("プライベートで友人に『意外だね』と言われ、言葉に詰まった",
     ["強く驚いた", "少し戸惑った", "あまり気にしていない"])
]
ASSOCIATIONS = ["上司", "休日", "期限", "チーム"]

# --- Word Selection Phase ---
selected_words = st.multiselect(
    "次の中から最も自分にしっくりこないと直感で感じる言葉を3つ選んでください",
    KEYWORDS,
    max_selections=3
)
if len(selected_words) < 3:
    st.info("3つ選んでください")
    st.stop()

# --- Reaction Phase ---
st.header("選んだワードに対する最初の反応を直感で選んでください")
user_reactions = {}
for w in selected_words:
    user_reactions[w] = st.radio(f"{w} に対して感じたことは？", REACTIONS, key=w)

# --- Scenario Recall Phase ---
st.header("次のシチュエーションであなたはどう感じましたか？（直感で選択）")
scenario_text, scenario_opts = SCENARIOS[0]
scenario_choice = st.radio(scenario_text, scenario_opts, key="scenario")

# --- Association Phase ---
st.header("以下の言葉を見て、直感で思い浮かんだ一語を入力してください")
assoc_input = st.text_input(
    f"{ASSOCIATIONS[0]}, {ASSOCIATIONS[1]}, {ASSOCIATIONS[2]}, {ASSOCIATIONS[3]} の中から直感で一つ"
)
if not assoc_input:
    st.info("一語入力してください")
    st.stop()

# --- Association Reaction Phase ---
st.header("その言葉に対する感情を一つ選んでください")
assoc_reactions = st.radio(
    "感じた感情は？", ["驚き", "安堵感", "違和感", "無関心"], key="assoc_react"
)

# --- Build Prompt ---
def build_prompt():
    few_shot = """
# 例示フォーマット
ユーザー回答
シナリオ："チームミーティングで発言後、同僚から『そこまで分析的だったとは驚いた』と言われ、とても驚いた"
連想ワード："客観性"

AI分析結果
Assumptions
- Aさんは自身をあまり分析的だと認識していない。

Blind Spots
◉ 死角1：自分の“観察眼”を過小評価している
◉ 死角2：“情報の裏を読む”姿勢への抵抗

Action
- ミーティング後に「どのデータを重視したか」をメモする。
"""
    user_section = "ユーザー回答\n"
    user_section += "選択ワードと反応: " + ", ".join(
        [f"{w}（{user_reactions[w]}）" for w in selected_words]
    ) + "\n"
    user_section += f"シチュエーション反応: {scenario_choice}\n"
    user_section += f"連想ワード: {assoc_input}（{assoc_reactions}）\n"
    return few_shot + "\nUSER:\n" + user_section + "\nAI:"

prompt = build_prompt()

# --- Call OpenAI API ---
with st.spinner('AIが死角を分析中...'):
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたはプロの心理カウンセラーです。ユーザーの回答から独自の死角を抽出し、Assumptions, Blind Spots, Actionの形式で回答してください。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )

# --- Display Result ---
st.subheader("AI分析結果")
st.write(res.choices[0].message.content)

# --- Final Note ---
st.markdown("---")
st.info("ここからはあなた自身の時間です。診断で得た気づきをもとに、ご自身でじっくり考えてみてください。あなたの中にある答えは、きっとあなた自身が一番知っています。")
