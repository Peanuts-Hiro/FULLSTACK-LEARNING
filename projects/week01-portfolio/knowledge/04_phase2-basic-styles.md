# フェーズ2: 基本スタイルの実装 - 思考と学習ポイント

## 実装時の思考プロセス

### 1. CSS変数を「デザインシステムの基盤」として設計

**思考**: 色や余白をその場で決めると、後で統一感がなくなる。最初にシステムを作る。

#### なぜCSS変数なのか？

**悪い例（変数なし）**:
```css
header { background: #2c3e50; }
.button { background: #3498db; }
footer { background: #2c3e50; }  /* 同じ色をコピペ */
.link { color: #3498db; }        /* また同じ色をコピペ */

/* 後で色を変えたい... */
/* → すべて手作業で変更 */
/* → 変更漏れが発生 */
```

**良い例（CSS変数）**:
```css
:root {
  --primary-color: #2c3e50;
  --accent-color: #3498db;
}

header { background: var(--primary-color); }
.button { background: var(--accent-color); }
footer { background: var(--primary-color); }
.link { color: var(--accent-color); }

/* 後で色を変えたい... */
/* → :rootの値を1箇所変更するだけ！ */
```

**メリット**:
1. **一貫性**: 同じ色が確実に同じ
2. **保守性**: 変更が簡単（1箇所変えるだけ）
3. **可読性**: 色の「意味」が分かる（`--primary-color`）
4. **拡張性**: 新しい色を追加しやすい

---

### 2. カラースキームを「役割」で分類

**思考**: 色には「役割」がある。ランダムに選ばない。

#### カラースキームの設計思想

```css
:root {
    /* プライマリ（主要色）: ブランドカラー */
    --primary-color: #2c3e50;      /* ヘッダー、見出し */
    --primary-light: #34495e;      /* ホバー時 */

    /* アクセント（強調色）: 行動を促す */
    --accent-color: #3498db;       /* ボタン、リンク */
    --accent-hover: #2980b9;       /* ホバー時 */

    /* テキスト色: 可読性重視 */
    --text-color: #333333;         /* メインテキスト */
    --text-light: #7f8c8d;         /* 補足テキスト */

    /* 背景色: コントラスト確保 */
    --bg-color: #ffffff;           /* メイン背景 */
    --bg-light: #ecf0f1;           /* セクション区切り */

    /* ボーダー色: 視覚的な区切り */
    --border-color: #bdc3c7;
}
```

#### 各色の役割

**プライマリカラー（主要色）**:
- 用途: ブランドの顔、ヘッダー、フッター、見出し
- 特徴: 落ち着いた色、全体の印象を決める
- 面積: 多め（30-40%）

**アクセントカラー（強調色）**:
- 用途: ボタン、リンク、CTA（行動喚起）
- 特徴: 目立つ色、クリックを促す
- 面積: 少なめ（10-20%）

**テキストカラー**:
- 用途: 本文、説明文
- 特徴: 読みやすさ重視、コントラスト比確保
- ルール: 白背景なら濃い色（#333等）

**背景カラー**:
- 用途: セクションの背景
- 特徴: テキストが読みやすい色
- パターン: 白と薄いグレーを交互に

---

### 3. スペーシングを「8の倍数」で統一

**思考**: 余白も「システム」。ランダムな数値を使わない。

#### スペーシングシステムの設計

```css
:root {
    --spacing-xs: 8px;    /* 最小 */
    --spacing-sm: 16px;   /* 小 */
    --spacing-md: 24px;   /* 中 */
    --spacing-lg: 40px;   /* 大 */
    --spacing-xl: 60px;   /* 最大 */
}
```

#### なぜ8の倍数なのか？

**理由1: 視覚的にバランスが良い**
- 8, 16, 24, 32, 40...
- 人間の目に心地よく映る比率

**理由2: デザインの黄金比**
- デザイナーとエンジニアの共通言語
- 多くのデザインシステムで採用

**理由3: 計算しやすい**
- 半分: 8 → 4
- 2倍: 8 → 16
- 3倍: 8 → 24

#### 使い分けの基準

| サイズ | 用途 | 具体例 |
|--------|------|--------|
| xs (8px) | タグ間、小さな要素間 | タグ同士の間隔 |
| sm (16px) | 段落間、カード内の余白 | テキストと画像の間 |
| md (24px) | セクション内の要素間 | 見出しと本文の間 |
| lg (40px) | セクション間の余白 | カード間の距離 |
| xl (60px) | セクション自体のpadding | セクションの上下余白 |

**悪い例（バラバラ）**:
```css
.header { padding: 17px; }
.section { margin: 23px; }
.card { padding: 19px; }
```

**良い例（システム化）**:
```css
.header { padding: var(--spacing-md); }   /* 24px */
.section { margin: var(--spacing-lg); }   /* 40px */
.card { padding: var(--spacing-sm); }     /* 16px */
```

---

### 4. リセットCSSで「ゼロベース」を作る

**思考**: ブラウザのデフォルトスタイルは邪魔。まっさらから始める。

#### なぜリセットCSSが必要なのか？

**問題**: ブラウザごとにデフォルトスタイルが違う
- Chrome: marginが8px
- Firefox: marginが8px
- Safari: marginが異なる場合がある

**解決**: すべてをリセット

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

#### 各プロパティの意味

**`margin: 0; padding: 0;`**:
- すべての要素の余白をゼロにする
- 「まっさら」な状態から始められる

**`box-sizing: border-box;`**:
- 超重要！幅の計算方法を変更

**デフォルト（content-box）の問題**:
```css
.box {
  width: 300px;
  padding: 20px;
  border: 2px solid black;
}
/* 実際の幅: 300 + 20×2 + 2×2 = 344px */
/* 意図と違う！ */
```

**border-boxの解決**:
```css
.box {
  width: 300px;
  padding: 20px;
  border: 2px solid black;
  box-sizing: border-box;
}
/* 実際の幅: 300px（パディングとボーダー含む） */
/* 意図通り！ */
```

**覚え方**: 「border-box = 幅にすべて含む」

---

### 5. タイポグラフィを「階層」で設計

**思考**: 文字サイズは「重要度」を表す。階層を作る。

#### フォントサイズの階層

```css
h1 { font-size: 2.5rem; }  /* 40px - 最も重要 */
h2 { font-size: 2rem; }    /* 32px - セクション見出し */
h3 { font-size: 1.5rem; }  /* 24px - サブ見出し */
p  { font-size: 1rem; }    /* 16px - 本文 */
small { font-size: 0.875rem; } /* 14px - 補足 */
```

#### remとpxの違い

**px（ピクセル）**:
- 固定サイズ
- ユーザーの設定を無視
- アクセシビリティが低い

**rem（ルート em）**:
- 相対サイズ（ルート要素の文字サイズが基準）
- ユーザーの設定を尊重
- アクセシビリティが高い

**計算方法**:
- デフォルト: 1rem = 16px
- 2rem = 32px
- 0.875rem = 14px

**なぜremを使うのか？**:
- ユーザーがブラウザで文字サイズを変更できる
- 視覚障害者への配慮
- モダンな開発のベストプラクティス

#### 行間（line-height）の重要性

```css
body {
  line-height: 1.6;  /* 160% */
}
```

**良い行間の基準**:
- 本文: 1.5〜1.8（読みやすさ重視）
- 見出し: 1.2〜1.4（引き締まった印象）

**なぜ1.6なのか？**:
- 行間が狭い（1.0-1.3）: 読みにくい
- 行間が適切（1.5-1.8）: 読みやすい
- 行間が広い（2.0以上）: 間延びして見える

---

### 6. コメントを「教科書」として書く（CSS版）

**思考**: CSSも初学者が見返したとき、意味が分かるように。

#### コメントの3つのレベル

**レベル1: セクションコメント**
```css
/* ===== ヘッダー ===== */
header {
  ...
}
```

**レベル2: プロパティの説明**
```css
header {
    /* background-color: 背景色 */
    background-color: var(--primary-color);

    /* padding: 内側の余白（上下 左右） */
    padding: var(--spacing-md) 0;
}
```

**レベル3: 技術的な補足**
```css
header {
    /* position: 要素の配置方法 */
    /* sticky: スクロールしても画面に固定 */
    position: sticky;

    /* top: 固定する位置（上から0px） */
    top: 0;
}
```

---

## 学習者がくみ取るべき内容

### 1. CSS変数（カスタムプロパティ）の使い方

#### 基本構文

```css
/* 定義: :root内で変数を定義 */
:root {
  --変数名: 値;
}

/* 使用: var()で変数を使用 */
.要素 {
  プロパティ: var(--変数名);
}
```

#### 実例

```css
/* 定義 */
:root {
  --primary-color: #2c3e50;
  --spacing-md: 24px;
}

/* 使用 */
header {
  background: var(--primary-color);
  padding: var(--spacing-md);
}

footer {
  background: var(--primary-color);  /* 同じ色を再利用 */
  padding: var(--spacing-md);        /* 同じ余白を再利用 */
}
```

#### 命名規則

**良い命名**:
- `--primary-color`: 役割が分かる
- `--spacing-md`: サイズが分かる
- `--text-color`: 用途が分かる

**悪い命名**:
- `--color1`: 何に使うか分からない
- `--blue`: 色は変わるかもしれない
- `--x`: 意味不明

---

### 2. CSSセレクタの基本

#### 主要なセレクタ

**要素セレクタ**:
```css
h1 { color: blue; }        /* すべてのh1 */
p { font-size: 16px; }     /* すべてのp */
```

**クラスセレクタ**:
```css
.skill-card { border: 1px solid gray; }  /* class="skill-card" */
.hero-tagline { font-size: 20px; }       /* class="hero-tagline" */
```

**IDセレクタ**:
```css
#hero { background: blue; }    /* id="hero" */
#about { padding: 60px; }      /* id="about" */
```

**子孫セレクタ**:
```css
nav a { color: white; }        /* nav内のすべてのa */
footer p { font-size: 14px; }  /* footer内のすべてのp */
```

#### セレクタの優先順位

優先度（高い順）:
1. インラインスタイル（HTML内の`style="..."`）
2. IDセレクタ（`#hero`）
3. クラスセレクタ（`.skill-card`）
4. 要素セレクタ（`h1`）

**実例**:
```css
h1 { color: blue; }            /* 優先度: 低 */
.title { color: red; }         /* 優先度: 中 */
#main-title { color: green; }  /* 優先度: 高 */
```

```html
<h1 id="main-title" class="title">タイトル</h1>
<!-- 結果: 緑色（IDセレクタが最優先） -->
```

---

### 3. ボックスモデルの理解

#### ボックスモデルとは？

すべてのHTML要素は「箱」として扱われる。

```
┌─────────────────── margin（外側の余白）
│ ┌───────────────── border（境界線）
│ │ ┌─────────────── padding（内側の余白）
│ │ │ ┌──────────── content（内容）
│ │ │ │
│ │ │ │   テキスト
│ │ │ │
│ │ │ └────────────
│ │ └───────────────
│ └─────────────────
└───────────────────
```

#### 各要素の役割

**content（内容）**:
- テキストや画像などの実際の内容
- `width`と`height`で指定

**padding（内側の余白）**:
- 内容とボーダーの間の余白
- 背景色が適用される領域

**border（境界線）**:
- 要素の境界線
- 太さ、スタイル、色を指定可能

**margin（外側の余白）**:
- 他の要素との間の余白
- 背景色は適用されない

#### 実例

```css
.box {
  /* 内容の幅 */
  width: 300px;

  /* 内側の余白 */
  padding: 20px;

  /* 境界線 */
  border: 2px solid black;

  /* 外側の余白 */
  margin: 10px;
}
```

**box-sizing: border-box の場合**:
- 幅300pxの中に、padding と border が含まれる
- 実際のコンテンツ幅: 300 - (20×2) - (2×2) = 256px

---

### 4. marginとpaddingの使い分け

#### 基本ルール

**paddingを使う場合**:
- 要素の**内側**に余白が欲しい
- 背景色やボーダーを含めたい

**marginを使う場合**:
- 要素の**外側**に余白が欲しい
- 他の要素との距離を空けたい

#### 実例で理解

**padding の例**:
```css
.card {
  background: lightblue;
  padding: 20px;  /* 内側に余白 */
}
```
```
┌─────────────────┐
│ [背景色]         │ ← 背景色がpadding領域まで適用
│                  │
│   テキスト      │
│                  │
│ [背景色]         │
└─────────────────┘
```

**margin の例**:
```css
.card {
  background: lightblue;
  margin: 20px;  /* 外側に余白 */
}
```
```
  [余白]           ← 背景色なし
┌─────────────────┐
│[背景色]          │
│  テキスト       │
│[背景色]          │
└─────────────────┘
  [余白]           ← 背景色なし
```

---

### 5. 色の指定方法

#### 4つの方法

**1. カラーネーム**:
```css
color: red;
color: blue;
color: white;
```
- メリット: 分かりやすい
- デメリット: 選択肢が少ない

**2. HEXコード（16進数）**:
```css
color: #FF0000;  /* 赤 */
color: #0000FF;  /* 青 */
color: #333333;  /* ダークグレー */
```
- メリット: 正確な色指定
- デメリット: 直感的でない

**3. RGB**:
```css
color: rgb(255, 0, 0);  /* 赤 */
color: rgb(0, 0, 255);  /* 青 */
```
- R（赤）、G（緑）、B（青）の値を0-255で指定

**4. RGBA（透明度付き）**:
```css
color: rgba(255, 0, 0, 0.5);  /* 半透明の赤 */
```
- 最後の値（0.5）が透明度（0=透明、1=不透明）

#### どれを使うべきか？

- **CSS変数**: 最優先（保守性が高い）
- **HEXコード**: CSS変数の値として使う
- **RGBA**: 影や透明度が必要な時

**推奨パターン**:
```css
:root {
  --primary-color: #2c3e50;  /* HEXで定義 */
}

header {
  background: var(--primary-color);  /* 変数で使用 */
}

.shadow {
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* 影にはRGBA */
}
```

---

### 6. transitionの基礎

#### 基本構文

```css
transition: プロパティ 時間 タイミング関数;
```

#### 実例

```css
.button {
  background: blue;
  transition: all 0.3s ease;
}

.button:hover {
  background: red;
}
```

**効果**: マウスを乗せると、0.3秒かけて青から赤に変化

#### パラメータの意味

**プロパティ**:
- `all`: すべてのプロパティ
- `background`: 背景色のみ
- `transform`: 変形のみ

**時間**:
- `0.3s`: 0.3秒
- `300ms`: 300ミリ秒（同じ）

**タイミング関数**:
- `ease`: 開始と終了がゆっくり
- `linear`: 一定速度
- `ease-in`: 開始がゆっくり
- `ease-out`: 終了がゆっくり

---

## 実践的なチェックリスト

CSSを書く際に確認すべきこと：

### CSS変数
- [ ] `:root`でカラースキームを定義しているか？
- [ ] スペーシングシステムを定義しているか？
- [ ] 変数名は意味が分かるか？

### リセットCSS
- [ ] `*`セレクタでmargin/paddingをリセットしているか？
- [ ] `box-sizing: border-box`を設定しているか？

### タイポグラフィ
- [ ] フォントサイズをremで指定しているか？
- [ ] line-heightを1.5〜1.8に設定しているか？
- [ ] 見出しの階層は適切か？

### 色とコントラスト
- [ ] テキストと背景のコントラストは十分か？
- [ ] CSS変数を使っているか？

### スペーシング
- [ ] 8の倍数を使っているか？
- [ ] marginとpaddingを適切に使い分けているか？

---

## よくある間違いと解決策

### 間違い1: ハードコードされた色

**悪い例**:
```css
header { background: #2c3e50; }
button { background: #3498db; }
footer { background: #2c3e50; }  /* 同じ色をコピペ */
```

**修正**:
```css
:root {
  --primary-color: #2c3e50;
  --accent-color: #3498db;
}

header { background: var(--primary-color); }
button { background: var(--accent-color); }
footer { background: var(--primary-color); }
```

---

### 間違い2: pxだらけのフォントサイズ

**悪い例**:
```css
h1 { font-size: 40px; }
h2 { font-size: 32px; }
p { font-size: 16px; }
```

**修正**:
```css
h1 { font-size: 2.5rem; }  /* 40px相当 */
h2 { font-size: 2rem; }    /* 32px相当 */
p { font-size: 1rem; }     /* 16px相当 */
```

---

### 間違い3: box-sizingを設定し忘れ

**悪い例**:
```css
.box {
  width: 300px;
  padding: 20px;
}
/* 実際の幅: 340px（意図と違う） */
```

**修正**:
```css
* {
  box-sizing: border-box;  /* 最初に設定 */
}

.box {
  width: 300px;
  padding: 20px;
}
/* 実際の幅: 300px（意図通り） */
```

---

## 次のステップ

基本スタイルが完成したら：

1. **ブラウザで確認**
   - 色は適用されているか？
   - 文字サイズは適切か？
   - 余白は十分か？

2. **次のフェーズへ**
   - フェーズ3: Flexboxレイアウトの実装
   - 要素を正しく配置する

---

**最も重要な学び**:

CSSは「その場しのぎ」ではなく、「システム」として設計する。

CSS変数を使うことで、保守性の高いコードが書ける。

色や余白は、統一されていることが美しさの条件。
