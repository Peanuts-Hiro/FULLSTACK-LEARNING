# DOM（Document Object Model）とは

## 1. DOMの基本概念

### DOMを一言で言うと
**「JavaScriptがHTMLを操作するための仕組み」**

HTMLで書いた画面を、JavaScriptで動的に変更するための橋渡しをするのがDOMです。

---

## 2. なぜDOMが必要なのか

### 静的なHTMLの限界
```html
<!-- これだけでは何も動かない -->
<h1>こんにちは</h1>
<button>クリック</button>
```

HTMLは**静的**（動かない）です。ボタンを押しても何も起こりません。

### JavaScriptで動的にしたい
```javascript
// ボタンを押したら文字を変えたい
// 新しい要素を追加したい
// 要素を削除したい
```

**問題:** JavaScriptはHTMLを直接触れない
**解決:** DOMという仲介者を通して操作する

---

## 3. DOMの仕組み

### HTMLがDOMツリーに変換される

ブラウザがHTMLを読み込むと、自動的に**DOMツリー**という木構造に変換されます。

```html
<!DOCTYPE html>
<html>
  <body>
    <h1>タイトル</h1>
    <ul>
      <li>項目1</li>
      <li>項目2</li>
    </ul>
  </body>
</html>
```

↓ ブラウザが自動変換

```
document (ドキュメント全体)
  └─ html
      └─ body
          ├─ h1 ("タイトル")
          └─ ul
              ├─ li ("項目1")
              └─ li ("項目2")
```

この木構造が**DOM**です。JavaScriptはこの木を操作します。

---

## 4. DOM操作の基本

### 4.1 要素を取得する

```javascript
// IDで取得（一番よく使う）
const input = document.getElementById('taskInput');

// クラス名で取得
const buttons = document.getElementsByClassName('deleteBtn');

// CSSセレクタで取得（最近の主流）
const input = document.querySelector('#taskInput');
const allButtons = document.querySelectorAll('.deleteBtn');
```

**イメージ:**
「HTMLの中から特定の要素を探してきて、JavaScriptの変数に入れる」

### 4.2 要素の内容を変更する

```javascript
// HTMLの<h1>の文字を変更
const title = document.querySelector('h1');
title.textContent = '新しいタイトル';
```

**結果:**
```html
<!-- 変更前 -->
<h1>タイトル</h1>

<!-- 変更後 -->
<h1>新しいタイトル</h1>
```

### 4.3 新しい要素を作成する

```javascript
// 新しい<li>要素を作る
const newItem = document.createElement('li');

// 中身を設定
newItem.textContent = '新しい項目';

// どこかに追加する
const list = document.querySelector('ul');
list.appendChild(newItem);
```

**結果:**
```html
<!-- 変更前 -->
<ul>
  <li>項目1</li>
  <li>項目2</li>
</ul>

<!-- 変更後 -->
<ul>
  <li>項目1</li>
  <li>項目2</li>
  <li>新しい項目</li>  ← 追加された！
</ul>
```

### 4.4 要素を削除する

```javascript
const item = document.querySelector('li');
item.remove();  // その要素が消える
```

---

## 5. ToDoアプリでのDOM操作の具体例

### シナリオ: タスクを追加する

```javascript
// 1. 入力欄の要素を取得
const input = document.getElementById('taskInput');

// 2. 入力された値を取得
const taskText = input.value;  // 例: "買い物に行く"

// 3. 新しい<li>要素を作成
const newTask = document.createElement('li');

// 4. <li>の中身を設定
newTask.textContent = taskText;  // <li>買い物に行く</li>

// 5. <ul>を取得
const taskList = document.getElementById('taskList');

// 6. <ul>に<li>を追加
taskList.appendChild(newTask);
```

**何が起こるか:**
```html
<!-- 実行前 -->
<ul id="taskList">
</ul>

<!-- 実行後 -->
<ul id="taskList">
  <li>買い物に行く</li>  ← DOMに追加された！
</ul>
```

**ブラウザの画面に即座に反映されます！**

---

## 6. DOMとHTMLファイルの違い

### 重要な理解
```
HTMLファイル（.html）
  ↓ ブラウザが読み込む
DOM（メモリ上の木構造）
  ↓ JavaScriptが操作
画面に表示される内容が変わる
```

**ポイント:**
- HTMLファイル自体は変わらない
- DOMが変わることで、画面が変わる
- ページをリロードすると、HTMLファイルから再度DOMが作られる（変更は消える）

### 実験してみよう

1. HTMLファイルに `<h1>元のタイトル</h1>` と書く
2. JavaScriptで `document.querySelector('h1').textContent = '変更後';` を実行
3. 画面は「変更後」と表示される
4. HTMLファイルを開くと「元のタイトル」のまま
5. ブラウザをリロードすると「元のタイトル」に戻る

→ DOMだけが変わっていた証拠

---

## 7. よく使うDOM操作メソッド一覧

| メソッド | 説明 | 例 |
|---------|------|-----|
| `getElementById()` | IDで要素を取得 | `document.getElementById('taskInput')` |
| `querySelector()` | CSSセレクタで取得（1つ） | `document.querySelector('.button')` |
| `querySelectorAll()` | CSSセレクタで取得（全部） | `document.querySelectorAll('li')` |
| `createElement()` | 新しい要素を作成 | `document.createElement('li')` |
| `appendChild()` | 子要素として追加 | `parent.appendChild(child)` |
| `remove()` | 要素を削除 | `element.remove()` |
| `textContent` | テキスト内容を取得/設定 | `element.textContent = 'text'` |
| `value` | input要素の値を取得/設定 | `input.value` |

---

## 8. 実際のコード例（ToDoアプリ風）

```javascript
// ボタンをクリックしたら実行される関数
function addTask() {
  // 1. 入力欄から値を取得（DOM操作）
  const input = document.getElementById('taskInput');
  const taskText = input.value;

  // 2. 空チェック
  if (taskText === '') {
    return;  // 何もしない
  }

  // 3. 新しいタスク要素を作成（DOM操作）
  const li = document.createElement('li');
  li.textContent = taskText;

  // 4. リストに追加（DOM操作）
  const ul = document.getElementById('taskList');
  ul.appendChild(li);

  // 5. 入力欄をクリア（DOM操作）
  input.value = '';
}

// ボタンにイベントを設定（DOM操作）
const button = document.getElementById('addButton');
button.addEventListener('click', addTask);
```

**このコードの流れ:**
1. HTMLの要素をJavaScriptで取得（DOMを通して）
2. 新しい要素を作成（DOMに追加）
3. 画面に即座に反映される

---

## 9. まとめ

### DOMは何か
- ブラウザがHTMLから作る木構造
- JavaScriptが操作できる対象

### なぜ必要か
- 静的なHTMLを動的に変更するため
- ユーザーの操作に反応するため

### どう使うか
1. `document.getElementById()` などで要素を取得
2. `.textContent` や `.value` で内容を変更
3. `createElement()` と `appendChild()` で要素を追加
4. `.remove()` で要素を削除

### ToDoアプリでは
- タスクを追加 → DOM に `<li>` を追加
- タスクを削除 → DOM から `<li>` を削除
- 画面が即座に更新される

---

## 学習のポイント

DOM操作は**Webアプリケーション開発の基礎中の基礎**です。
- ReactやVue.jsなどのモダンなフレームワークも、内部ではDOM操作をしています
- まずはVanilla JavaScriptでDOM操作を理解することで、フレームワークの理解が深まります
- 実際に手を動かして、要素を追加・削除・変更する体験を積むことが重要です
