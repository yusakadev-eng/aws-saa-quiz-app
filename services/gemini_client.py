import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None


def _get_client():
    """Gemini APIクライアントをシングルトンで返す"""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        _client = genai.Client(api_key=api_key)
    return _client


def generate_explanation(question: str, choices: list[str], answer_index: int, user_index: int) -> str:
    """
    問題・選択肢・正解・ユーザーの回答をもとに、Gemini APIで初心者向け解説を生成して返す。

    Args:
        question:     問題文
        choices:      選択肢のリスト（例: ["A", "B", "C", "D"]）
        answer_index: 正解の選択肢番号（0始まり）
        user_index:   ユーザーが選んだ選択肢番号（0始まり）

    Returns:
        生成された解説テキスト。エラー時はエラーメッセージ文字列。
    """
    correct_choice = choices[answer_index]
    user_choice = choices[user_index]
    choices_text = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(choices))

    prompt = f"""あなたはAWS認定ソリューションアーキテクト（SAA）の試験対策を教える講師です。
プログラミングもAWSも未経験の初心者に向けて、やさしく丁寧に解説してください。
専門用語を使う場合は、必ず補足説明を加えてください。

## 問題
{question}

## 選択肢
{choices_text}

## 正解
{correct_choice}

## ユーザーの回答
{user_choice}

## 解説してほしいこと
1. なぜ「{correct_choice}」が正解なのか、理由をわかりやすく説明してください。
2. 他の選択肢がなぜ不正解なのかも、それぞれ簡潔に説明してください。
3. この問題で覚えておくべきポイントを1〜2行でまとめてください。

解説は読みやすいように、見出しや箇条書きを使って整理してください。"""

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception:
        return "解説の取得に失敗しました。再試行してください。"
