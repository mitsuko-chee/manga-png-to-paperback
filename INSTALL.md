# セットアップ手順

## 1. ターミナルを開く

**Macの場合**
Spotlight（⌘+スペース）で「ターミナル」と検索して開いてください。

**Windowsの場合**
スタートメニューで「cmd」と検索して「コマンドプロンプト」を開いてください。

---

## 2. 作業フォルダを作る

すでにClaude Codeで使っているご自身の作業フォルダがある方は、新しく作らずそちらに `cd` していただいてOKです。

以下は一例（フォルダ名は `my-workspace` でなくても構いません）です。

**Macの場合（例）**
```
mkdir ~/my-workspace
cd ~/my-workspace
```

**Windowsの場合（例）**
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

## アップデート方法

すでにインストール済みの方が最新版に更新したい場合は、インストール時と**同じコマンドをもう一度実行**してください。

```bash
curl -fsSL https://raw.githubusercontent.com/mitsuko-chee/manga-png-to-paperback/main/install.sh | bash
```

`/manga-png-to-paperback アップデートして` のようにチャットで指示しても更新されません。スラッシュコマンドはローカルに保存済みのファイルを実行するだけで、GitHubの最新版を自動で取りに行く仕組みがないためです。上記コマンドを再実行してファイルを上書きしてください。

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
