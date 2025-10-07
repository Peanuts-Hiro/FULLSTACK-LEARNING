// === ToDoリストアプリ ===
// このファイルでは、タスクの追加・削除機能を実装します

// === DOM要素の取得 ===
// DOM (Document Object Model): HTMLの構造をJavaScriptから操作するための仕組み

// getElementById: IDを指定してHTML要素を取得する
const taskInput = document.getElementById('taskInput');    // 入力欄
const addButton = document.getElementById('addButton');    // 追加ボタン
const taskList = document.getElementById('taskList');      // タスクリスト

// === 関数定義 ===

/**
 * タスク追加関数
 * 入力欄の値を取得して、新しいタスクをリストに追加する
 */
function addTask() {
    // 1. 入力欄の値を取得
    // trim(): 前後の空白を削除する（"  タスク  " → "タスク"）
    const taskText = taskInput.value.trim();

    // 2. 空チェック: 何も入力されていない場合は処理を中止
    if (taskText === '') {
        // returnで関数を終了（以降の処理は実行されない）
        return;
    }

    // 3. 新しい<li>要素を作成
    // createElement: 新しいHTML要素を作成する
    const li = document.createElement('li');

    // 4. タスク名を表示する<span>要素を作成
    const taskSpan = document.createElement('span');
    // textContent: 要素の中のテキストを設定する
    taskSpan.textContent = taskText;

    // 5. 削除ボタンを作成
    const deleteButton = document.createElement('button');
    deleteButton.textContent = '削除';
    // className: 要素にCSSクラスを設定する
    deleteButton.className = 'deleteBtn';

    // 6. 削除ボタンにクリックイベントを設定
    // addEventListener: 要素にイベントを追加する
    // 'click': クリックイベント
    // deleteTask: クリックされたときに実行する関数
    deleteButton.addEventListener('click', deleteTask);

    // 7. <li>にタスク名と削除ボタンを追加
    // appendChild: 子要素として追加する
    li.appendChild(taskSpan);
    li.appendChild(deleteButton);

    // 8. <ul>（タスクリスト）に<li>を追加
    taskList.appendChild(li);

    // 9. 入力欄をクリア（次の入力の準備）
    taskInput.value = '';

    // 10. 入力欄にフォーカスを戻す（すぐに次のタスクを入力できる）
    taskInput.focus();
}

/**
 * タスク削除関数
 * クリックされた削除ボタンに対応するタスクを削除する
 *
 * @param {Event} event - イベントオブジェクト（クリック情報が入っている）
 */
function deleteTask(event) {
    // 1. クリックされた削除ボタンを取得
    // event.target: イベントが発生した要素（この場合は削除ボタン）
    const deleteButton = event.target;

    // 2. 削除ボタンの親要素（<li>）を取得
    // parentElement: 親要素を取得する
    const li = deleteButton.parentElement;

    // 3. <li>を削除
    // remove(): 要素をDOMから削除する
    li.remove();
}

// === イベントリスナーの設定 ===

// 追加ボタンがクリックされたときに addTask 関数を実行
addButton.addEventListener('click', addTask);

// Enterキーでもタスクを追加できるようにする
// 'keypress': キーボードのキーが押されたときのイベント
taskInput.addEventListener('keypress', function(event) {
    // event.key: 押されたキーの名前
    // 'Enter': Enterキー
    if (event.key === 'Enter') {
        // Enterキーが押されたら addTask 関数を実行
        addTask();
    }
});

// === 初期化処理 ===

// ページが読み込まれたときに入力欄にフォーカスを当てる
// （すぐにタスクを入力できる状態にする）
taskInput.focus();
