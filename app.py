import json
import streamlit as st
from services.gemini_client import generate_explanation


# ── データ読み込み ──────────────────────────────────────────────────────────────

def load_questions():
    try:
        with open("data/questions.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"問題データの読み込みに失敗しました: {e}")
        st.stop()


# ── セッション状態の初期化 ────────────────────────────────────────────────────

def init_state():
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "selected" not in st.session_state:
        st.session_state.selected = None
    if "explanation" not in st.session_state:
        st.session_state.explanation = None


# ── メイン ────────────────────────────────────────────────────────────────────

def main():
    st.title("AWS SAA 問題集")

    questions = load_questions()
    init_state()

    idx = st.session_state.index
    total = len(questions)

    # 全問終了画面
    if idx >= total:
        st.success(f"全 {total} 問が完了しました！お疲れさまでした。")
        if st.button("最初からやり直す"):
            st.session_state.index = 0
            st.session_state.answered = False
            st.session_state.selected = None
            st.session_state.explanation = None
            st.rerun()
        return

    q = questions[idx]

    # カテゴリ・進捗
    st.caption(f"カテゴリ：{q['category']}")
    st.write(f"**問題 {idx + 1} / {total}**")
    st.progress((idx) / total)

    # 問題文
    st.markdown(f"### {q['question']}")

    # 選択肢（回答済みなら無効化）
    selected = st.radio(
        "選択肢を選んでください",
        options=q["choices"],
        index=None,
        disabled=st.session_state.answered,
        key=f"radio_{idx}",
    )
    if selected is not None:
        st.session_state.selected = selected

    # 回答ボタン
    if not st.session_state.answered:
        if st.button("回答する", disabled=(st.session_state.selected is None)):
            st.session_state.answered = True
            st.session_state.explanation = None
            st.rerun()

    # 回答済み：正誤 + 解説
    if st.session_state.answered:
        correct_choice = q["choices"][q["answerIndex"]]
        user_choice = st.session_state.selected

        if user_choice == correct_choice:
            st.success("正解です！")
        else:
            st.error(f"不正解です。正解は「{correct_choice}」でした。")

        # 解説（未取得なら生成）
        if st.session_state.explanation is None:
            with st.spinner("Geminiで解説を生成中..."):
                user_index = q["choices"].index(user_choice)
                st.session_state.explanation = generate_explanation(
                    question=q["question"],
                    choices=q["choices"],
                    answer_index=q["answerIndex"],
                    user_index=user_index,
                )
            st.rerun()

        st.markdown("---")
        st.markdown("#### AI解説")
        st.markdown(st.session_state.explanation)

        # 次の問題へ
        st.markdown("---")
        label = "結果を見る" if idx + 1 >= total else "次の問題へ"
        if st.button(label):
            st.session_state.index += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.session_state.explanation = None
            st.rerun()


if __name__ == "__main__":
    main()
