# 個人ポートフォリオサイト - 設計書

## 1. サイト構造設計

### 1.1 ページ構成（シングルページ）

```
┌─────────────────────────────────────┐
│           Header                     │
│  [Logo]  [Nav: About|Skills|...]    │
├─────────────────────────────────────┤
│           Hero Section               │
│      写真 + 名前 + キャッチコピー      │
├─────────────────────────────────────┤
│           About Section              │
│      プロフィール + 自己紹介文         │
├─────────────────────────────────────┤
│          Skills Section              │
│    [Skill 1] [Skill 2] [Skill 3]    │
├─────────────────────────────────────┤
│         Projects Section             │
│  [Card 1] [Card 2] [Card 3]         │
├─────────────────────────────────────┤
│         Contact Section              │
│    SNSリンク + メールアドレス          │
├─────────────────────────────────────┤
│            Footer                    │
│      © 2025 Your Name               │
└─────────────────────────────────────┘
```

### 1.2 HTML構造設計

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <!-- メタタグ、タイトル、CSS読み込み -->
</head>
<body>
  <!-- ヘッダー（固定ナビゲーション） -->
  <header>
    <nav>
      <h1>ロゴ/サイト名</h1>
      <ul>ナビゲーションリンク</ul>
    </nav>
  </header>

  <!-- メインコンテンツ -->
  <main>
    <!-- ヒーローセクション -->
    <section id="hero">
      <!-- プロフィール画像、名前、キャッチコピー -->
    </section>

    <!-- Aboutセクション -->
    <section id="about">
      <!-- 自己紹介文 -->
    </section>

    <!-- Skillsセクション -->
    <section id="skills">
      <!-- スキルリスト -->
    </section>

    <!-- Projectsセクション -->
    <section id="projects">
      <!-- プロジェクトカード（複数） -->
    </section>

    <!-- Contactセクション -->
    <section id="contact">
      <!-- SNSリンク、メールアドレス -->
    </section>
  </main>

  <!-- フッター -->
  <footer>
    <!-- 著作権表記、SNSアイコン -->
  </footer>
</body>
</html>
```

## 2. デザイン設計

### 2.1 カラースキーム

```css
/* プライマリカラー（メイン） */
--primary-color: #2c3e50;      /* ダークブルー - ヘッダー、見出し */
--primary-light: #34495e;      /* ライトブルー - ホバー効果 */

/* アクセントカラー */
--accent-color: #3498db;       /* ブルー - リンク、ボタン */
--accent-hover: #2980b9;       /* 濃いブルー - ホバー時 */

/* ニュートラルカラー */
--text-color: #333333;         /* 本文テキスト */
--text-light: #7f8c8d;         /* 補足テキスト */
--bg-color: #ffffff;           /* 背景白 */
--bg-light: #ecf0f1;           /* 背景グレー - セクション区切り */

/* ボーダー */
--border-color: #bdc3c7;       /* 境界線 */
```

### 2.2 タイポグラフィ

```css
/* フォントファミリー */
body {
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

/* フォントサイズ */
h1: 2.5rem (40px)   /* サイトタイトル、名前 */
h2: 2rem (32px)     /* セクション見出し */
h3: 1.5rem (24px)   /* サブ見出し、プロジェクト名 */
p:  1rem (16px)     /* 本文 */
small: 0.875rem (14px) /* 補足テキスト */

/* 行間 */
line-height: 1.6    /* 読みやすさ重視 */
```

### 2.3 スペーシング（余白）

```css
/* セクション間の余白 */
section {
  padding: 80px 0;
}

/* コンテンツ幅 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 要素間のマージン */
--spacing-xs: 8px
--spacing-sm: 16px
--spacing-md: 24px
--spacing-lg: 40px
--spacing-xl: 60px
```

## 3. コンポーネント設計

### 3.1 ヘッダー（ナビゲーション）

**レイアウト**: Flexbox（横並び）
```
[ロゴ]                    [About] [Skills] [Projects] [Contact]
```

**特徴**:
- 固定ヘッダー（スクロールしても表示）
- ロゴは左寄せ、ナビは右寄せ
- ナビリンクにホバー効果（下線アニメーション）

### 3.2 ヒーローセクション

**レイアウト**: Flexbox（中央揃え）
```
     [プロフィール画像]
      あなたの名前
    キャッチコピー文
```

**特徴**:
- 全幅背景（グラデーションまたは単色）
- 縦方向に中央配置
- 高さ: 70vh（ビューポートの70%）

### 3.3 スキルセクション

**レイアウト**: Flexbox（3カラムグリッド風）
```
[HTML/CSS]  [JavaScript]  [Git/GitHub]
  アイコン      アイコン       アイコン
   説明文       説明文        説明文
```

**特徴**:
- 各スキルカードは同じ幅
- ホバー時に少し浮き上がる（box-shadow）
- アイコンは絵文字またはシンプルな図形

### 3.4 プロジェクトカード

**レイアウト**: Flexbox（横並び、3カラム）
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  画像エリア   │ │  画像エリア   │ │  画像エリア   │
├──────────────┤ ├──────────────┤ ├──────────────┤
│プロジェクト名 │ │プロジェクト名 │ │プロジェクト名 │
│  説明文       │ │  説明文       │ │  説明文       │
│[使用技術]     │ │[使用技術]     │ │[使用技術]     │
└──────────────┘ └──────────────┘ └──────────────┘
```

**特徴**:
- カード型デザイン（影付き）
- ホバー時に拡大（transform: scale）
- 画像は固定比率（16:9）

### 3.5 コンタクトセクション

**レイアウト**: Flexbox（中央揃え）
```
      お気軽にご連絡ください

    [GitHub] [Twitter] [Email]
       ↓        ↓        ↓
     アイコン   アイコン   アイコン
```

**特徴**:
- SNSアイコンは横並び
- ホバー時に色変更
- アイコンサイズ: 40px × 40px

## 4. レイアウト手法

### 4.1 Flexboxの使用箇所

1. **ヘッダーナビゲーション**
   ```css
   nav {
     display: flex;
     justify-content: space-between;  /* 左右に配置 */
     align-items: center;             /* 縦方向中央 */
   }
   ```

2. **スキルカード**
   ```css
   .skills-container {
     display: flex;
     gap: 20px;                       /* カード間の間隔 */
     flex-wrap: wrap;                 /* 折り返し許可 */
   }
   ```

3. **プロジェクトカード**
   ```css
   .projects-container {
     display: flex;
     gap: 30px;
     justify-content: space-between;
   }
   ```

### 4.2 中央配置のテクニック

```css
/* ヒーローセクションの中央配置 */
.hero {
  display: flex;
  flex-direction: column;    /* 縦方向に配置 */
  justify-content: center;   /* 縦方向中央 */
  align-items: center;       /* 横方向中央 */
  min-height: 70vh;
}
```

## 5. インタラクション設計

### 5.1 ホバーエフェクト

**ナビゲーションリンク**
```css
nav a:hover {
  color: var(--accent-color);
  border-bottom: 2px solid var(--accent-color);
  transition: all 0.3s ease;
}
```

**プロジェクトカード**
```css
.project-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}
```

**スキルカード**
```css
.skill-card:hover {
  background-color: var(--bg-light);
  transform: scale(1.05);
  transition: all 0.3s ease;
}
```

### 5.2 スムーススクロール

```css
html {
  scroll-behavior: smooth;  /* ページ内リンクをスムーズに */
}
```

## 6. ファイル構成

```
week01-portfolio/
├── index.html          # メインHTMLファイル
├── style.css           # スタイルシート
├── images/             # 画像フォルダ
│   ├── profile.jpg     # プロフィール画像
│   ├── project1.jpg    # プロジェクト画像1
│   ├── project2.jpg    # プロジェクト画像2
│   └── project3.jpg    # プロジェクト画像3
├── requirements.md     # 要件定義書
├── design.md          # この設計書
└── README.md          # プロジェクト説明
```

## 7. 実装の優先順位

### フェーズ1: HTML構造
1. セマンティックタグでページ構造を作成
2. すべてのセクションを配置
3. ダミーコンテンツで動作確認

### フェーズ2: 基本スタイル
1. カラースキームの適用
2. タイポグラフィの設定
3. スペーシングの調整

### フェーズ3: レイアウト
1. Flexboxでヘッダーを配置
2. 各セクションをFlexboxで整形
3. コンテンツ幅の調整

### フェーズ4: 詳細デザイン
1. ホバーエフェクトの追加
2. 影やボーダーの調整
3. 細部の微調整

## 8. 学習ポイント

この設計を通じて学ぶこと：

### HTML
- セマンティックタグの適切な使い分け
- `id`属性でページ内リンクを作成
- 階層構造の論理的な設計

### CSS
- CSS変数（カスタムプロパティ）の使い方
- Flexboxの`justify-content`と`align-items`
- `transition`による滑らかなアニメーション
- `:hover`疑似クラスの活用
- `box-shadow`と`transform`によるエフェクト

### デザイン原則
- 一貫性のあるカラースキーム
- 適切な余白とスペーシング
- 視覚的な階層構造
- ユーザビリティを考慮した設計

---

次のステップは「実装」です。この設計に基づいてHTMLとCSSを書いていきます。
