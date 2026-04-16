# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AWS SAA（Solutions Architect Associate）向けの「AI解説付き問題集アプリ」。  
Python + Streamlit で構築し、Gemini API を使って回答後に解説を生成する。  
ポートフォリオ兼 AWS SAA 学習ツール。ローカル動作のみ想定（MVP）。

## Tech Stack

- **Language**: Python
- **Framework**: Streamlit
- **AI API**: Gemini API (`google-genai` SDK)
- **Data**: JSON file (no DB)
- **Config**: `.env` file for API keys

## Planned File Structure

```
aws-saa-quiz-app/
├── app.py                    # Streamlit main (UI, state, answer logic)
├── data/
│   └── questions.json        # Quiz questions (IAM category, 5 questions)
├── services/
│   └── gemini_client.py      # Gemini API communication & prompt building
├── prompts/
│   └── base_prompt.md        # Project design document & AI base prompt
├── .env                      # GEMINI_API_KEY (not committed)
├── requirements.txt
└── README.md
```

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Development Commands

```bash
# Install dependencies
pip install streamlit google-genai python-dotenv

# Run app
streamlit run app.py
```

## Architecture

**Data flow**: User → Streamlit UI → JSON questions → Answer → Gemini API → Explanation display

**State management** (via `st.session_state`):
- `current_index` — current question number
- `selected_answer` — user's selected choice
- `answered` — whether the question has been submitted

**Question JSON schema**:
```json
{
  "id": 1,
  "question": "問題文",
  "choices": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
  "answerIndex": 0,
  "category": "IAM"
}
```
`answerIndex` is 0-based. No `explanation` field — explanations are generated on-demand via Gemini API.

**`gemini_client.py`** receives question text, choices, correct answer, and user's answer, then builds a prompt asking Gemini to explain the correct answer and why other choices are wrong (初心者向け).

**UI flow**: question display → radio button selection → 回答ボタン → correct/incorrect display → "Geminiで解説を生成中..." → explanation → 次の問題へ button

## Key Constraints

- IAM category only, 5 questions (MVP scope)
- No login, no history persistence, no multi-category support
- API key must be in `.env`, never hardcoded
- API errors must show: `「解説の取得に失敗しました。再試行してください。」`
- JSON load errors must display an error and stop the app

## Target User

初心者（プログラミング・AWS ともに未経験）。説明は初心者向けに、専門用語には補足を入れること。
