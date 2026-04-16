# AWS SAA AI解説付き問題集アプリ

AWS Solutions Architect Associate（SAA）の試験対策として、AIが解説を生成する問題集アプリです。

---

## 📌 概要

- AWS SAA の IAM カテゴリの問題を解ける
- 回答後に Gemini API がリアルタイムで解説を生成
- Streamlit で動作するローカルアプリ

---

## 🖼️ スクリーンショット

> ※ 動作画面のスクリーンショットをここに追加してください

---

## 🛠️ 技術スタック

| 項目 | 内容 |
|------|------|
| 言語 | Python 3.11 |
| フレームワーク | Streamlit |
| AI API | Gemini API（google-genai） |
| データ管理 | JSON |
| APIキー管理 | .env（python-dotenv） |

---

## 📁 ファイル構成

```
aws-saa-quiz-app/
├── app.py                    # Streamlitメインアプリ
├── data/
│   └── questions.json        # 問題データ（IAM 5問）
├── services/
│   └── gemini_client.py      # Gemini API連携処理
├── prompts/
│   └── base_prompt.md        # AIへのベースプロンプト
├── .env                      # APIキー（GitHubに上げない）
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 セットアップ・起動手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/yusakadev-eng/aws-saa-quiz-app.git
cd aws-saa-quiz-app
```

### 2. ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 3. Gemini APIキーを取得

[Google AI Studio](https://aistudio.google.com/app/apikey) でAPIキーを取得します。

### 4. .envファイルを作成

```
GEMINI_API_KEY=your_api_key_here
```

### 5. アプリを起動

```bash
streamlit run app.py
# または
python -m streamlit run app.py
```

ブラウザで `http://localhost:8501` を開くと起動します。

---

## 📝 問題データについて

`data/questions.json` に問題を追加することで問題数を増やせます。

```json
{
  "id": 1,
  "question": "問題文",
  "choices": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
  "answerIndex": 0,
  "category": "IAM"
}
```

※ `answerIndex` は0始まりです。

---

## 🤖 AI活用について

このアプリは以下の用途でAIを活用しています。

- **解説生成**：Gemini APIが問題・選択肢・正解・ユーザーの回答をもとに初心者向け解説を生成
- **開発支援**：Claude・ChatGPTを使って設計・実装・ドキュメント作成を進めました

開発プロセスの記録はZennで公開しています。

- [【構想編】](https://zenn.dev/yusaka_devlog)
- [【要件定義編】](https://zenn.dev/yusaka_devlog)
- [【基本設計編】](https://zenn.dev/yusaka_devlog)
- [【環境構築・実装編】](https://zenn.dev/yusaka_devlog)

---

## ⚠️ 注意事項

- `.env` ファイルはGitHubに上げないでください（APIキーが含まれます）
- Gemini APIは無料枠（1,500回/日）の範囲内で使用しています

---

## 📄 ライセンス

MIT License
