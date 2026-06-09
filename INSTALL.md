# セットアップ手順

## 1. ターミナルを開く

**Macの場合**
Spotlight（⌘+スペース）で「ターミナル」と検索して開いてください。

**Windowsの場合**
スタートメニューで「cmd」と検索して「コマンドプロンプト」を開いてください。

---

## 2. 作業フォルダを作る

**Macの場合**
```
mkdir ~/my-workspace
cd ~/my-workspace
```

**Windowsの場合**
```
mkdir %USERPROFILE%\my-workspace
cd %USERPROFILE%\my-workspace
```

すでに `my-workspace` がある場合は `cd ~/my-workspace` だけでOKです。

---

## 3. Claude Codeを起動する

Claude Codeがインストールされていない場合は、先に[公式サイト](https://claude.ai/code)からインストールしてください。

```
claude
```

---

## 4. スキルをインストールする

ターミナルで以下のコマンドを実行してください。

```bash
curl -fsSL https://raw.githubusercontent.com/mitsuko-chee/manga-png-to-paperback/main/install.sh | bash
```

`✓ スキルをインストールしました` と表示されれば完了です。

---

## 5. 使い方

インストール後は以下のコマンドで起動できます。

```
/manga-png-to-paperback
```

---

## PNGフォルダのパスを調べる

**Macの場合**
FinderでPNGフォルダを右クリック →「情報を見る」→「場所」に表示されるパスをコピー。
またはフォルダをターミナルにドラッグ＆ドロップするとパスが入力されます。

**Windowsの場合**
エクスプローラーでPNGフォルダを右クリック →「パスのコピー」を選択。

---

## 📋 ご利用規約

リソースのファイルはご自身のKDP出版作業でのご利用に限ります。再配布・転載はご遠慮ください。
