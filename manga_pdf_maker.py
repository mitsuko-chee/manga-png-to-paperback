#!/usr/bin/env python3
"""
KDP ペーパーバック用PDF変換スクリプト
PNG画像フォルダ → KDP入稿用PDF

Claude Codeへの指示例：
  このフォルダのPNG画像をKDP用PDFにして
"""

import sys
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

SIZES = {
    "A5": (148 * mm, 210 * mm),
    "B6": (128 * mm, 182 * mm),
}

BLEED_MM = 3
MARGIN_MM = 10


def get_page_size(size_name: str, bleed: bool):
    w, h = SIZES[size_name]
    if bleed:
        b = BLEED_MM * mm
        return w + b * 2, h + b * 2
    return w, h


def _natural_key(p: Path):
    import re
    parts = re.split(r'(\d+)', p.name)
    return [int(x) if x.isdigit() else x.lower() for x in parts]

def get_png_files(input_dir: Path) -> list[Path]:
    files = sorted(input_dir.glob("*.png"), key=_natural_key)
    if not files:
        files = sorted(input_dir.glob("*.PNG"), key=_natural_key)
    return files


def check_resolution(input_dir: Path):
    png_files = get_png_files(input_dir)
    print(f"\n=== 解像度チェック ({len(png_files)}ファイル) ===")
    for png_path in png_files:
        img = Image.open(png_path)
        w_px, h_px = img.size
        dpi_info = img.info.get("dpi", None)
        dpi = round(dpi_info[0]) if dpi_info else "不明"
        warning = " ⚠️ 300dpi未満" if isinstance(dpi, int) and dpi < 300 else ""
        dpi_str = f"{dpi}dpi" if dpi != "不明" else "不明（メタデータなし）"
        print(f"  {png_path.name}: {w_px}×{h_px}px / {dpi_str}{warning}")
    print()


def get_brightness(img: Image.Image) -> float:
    gray = img.convert("L")
    pixels = list(gray.getdata())
    return sum(pixels) / len(pixels)


def draw_numbering(c, page_num: int, page_w: float, page_h: float,
                   dark_page: bool, bleed: bool):
    b = BLEED_MM * mm if bleed else 0
    font_size = 10
    margin_bottom = 8 * mm
    x = page_w / 2
    y = b + margin_bottom
    c.setFillColorRGB(1, 1, 1) if dark_page else c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", font_size)
    c.drawCentredString(x, y, str(page_num))
    c.setFillColorRGB(0, 0, 0)


def ask(question: str, choices: list[str]) -> str:
    while True:
        answer = input(f"{question} [{'/'.join(choices)}]: ").strip()
        if answer in choices:
            return answer
        print(f"  → {'/'.join(choices)} のいずれかを入力してください")


def make_pdf(input_dir, output_path, size_name, bleed, numbering,
             skip_pages, dark_threshold, add_margin,
             skip_filenames=None, white_filenames=None, all_white=False):
    png_files = get_png_files(input_dir)
    page_w, page_h = get_page_size(size_name, bleed)
    b = BLEED_MM * mm if bleed else 0
    c = canvas.Canvas(str(output_path), pagesize=(page_w, page_h))
    numbering_counter = 0
    skip_stems = set(skip_filenames) if skip_filenames else set()
    white_stems = set(white_filenames) if white_filenames else set()

    for i, png_path in enumerate(png_files):
        print(f"  処理中: {png_path.name} ({i+1}/{len(png_files)})")
        img = Image.open(png_path).convert("RGB")
        img_w_px, img_h_px = img.size

        if add_margin:
            m = MARGIN_MM * mm
            draw_area_w = page_w - b * 2 - m * 2
            draw_area_h = page_h - b * 2 - m * 2
            scale = min(draw_area_w / img_w_px, draw_area_h / img_h_px)
            scaled_w = img_w_px * scale
            scaled_h = img_h_px * scale
            x_offset = b + m + (draw_area_w - scaled_w) / 2
            y_offset = b + m + (draw_area_h - scaled_h) / 2
        else:
            scale = min(page_w / img_w_px, page_h / img_h_px)
            scaled_w = img_w_px * scale
            scaled_h = img_h_px * scale
            x_offset = (page_w - scaled_w) / 2
            y_offset = (page_h - scaled_h) / 2

        tmp_path = output_path.parent / f"_tmp_{i:04d}.jpg"
        img.save(str(tmp_path), "JPEG", quality=95)
        c.drawImage(str(tmp_path), x_offset, y_offset, width=scaled_w, height=scaled_h)

        if numbering and i >= skip_pages:
            numbering_counter += 1
            stem = png_path.stem
            if stem not in skip_stems:
                if all_white or stem in white_stems:
                    dark_page = True
                else:
                    dark_page = get_brightness(img) < dark_threshold
                draw_numbering(c, numbering_counter, page_w, page_h, dark_page, bleed)

        c.showPage()
        tmp_path.unlink(missing_ok=True)

    c.save()


def main():
    # フォルダの指定
    if len(sys.argv) > 1:
        input_dir = Path(sys.argv[1])
    else:
        path_str = input("PNG画像が入ったフォルダのパスを入力してください: ").strip()
        input_dir = Path(path_str)

    if not input_dir.is_dir():
        print(f"エラー: フォルダが見つかりません: {input_dir}")
        sys.exit(1)

    png_files = get_png_files(input_dir)
    if not png_files:
        print(f"エラー: {input_dir} にPNGファイルが見つかりません")
        sys.exit(1)

    # 解像度チェック
    check_resolution(input_dir)

    # 設定を対話で確認
    print("=== 設定を確認します ===\n")

    size_name = ask("判型を選んでください", ["A5", "B6"])
    bleed_ans = ask("裁ち落としはありますか", ["あり", "なし"])
    bleed = bleed_ans == "あり"

    numbering_ans = ask("ノンブル（ページ番号）を入れますか", ["あり", "なし"])
    numbering = numbering_ans == "あり"

    skip_pages = 0
    skip_filenames = []
    white_filenames = []
    all_white = False
    if numbering:
        stems = [p.stem for p in png_files]
        print("  ヒント: 番号をつけたい最初のファイル名（例: 001）を入力してください")
        while True:
            val = input("何番目のファイルからページ番号を開始しますか？（ファイル名の数字部分、例: 001）: ").strip()
            if not val:
                val = stems[0]
            if val in stems:
                skip_pages = stems.index(val)
                break
            else:
                print(f"  → ファイル名が見つかりません。{stems[0]}〜{stems[-1]} の範囲で入力してください")

        print("  ヒント: 番号を表示しないページのファイル名をドット区切りで入力してください（例: 001.024.059）")
        print("  不要な場合はそのままEnterを押してください")
        skip_input = input("スキップするページ（ファイル名、ドット区切り）: ").strip()
        if skip_input:
            skip_filenames = [s.strip() for s in skip_input.split(".") if s.strip()]

        all_white = False
        print("  ヒント: ファイル名をドット区切りで入力してください（例: 005.010）")
        print("  不要な場合はそのままEnterを押してください")
        white_input = input("白抜きにしたい特定のページはありますか？（ファイル名、ドット区切り）: ").strip()
        white_filenames = [s.strip() for s in white_input.split(".") if s.strip()] if white_input else []

    print("\nペーパーバックではページの端から10mm程度の余白があると読みやすくなります。")
    margin_ans = ask("あなたの画像にすでに余白がある場合はn、余白がない場合はy", ["y", "n"])
    add_margin = margin_ans == "y"

    # 出力ファイル名
    bleed_tag = "裁ち落としあり" if bleed else "裁ち落としなし"
    num_tag = "_ノンブルあり" if numbering else ""
    margin_tag = "_余白あり" if add_margin else ""
    output_path = input_dir.parent / f"KDP_{size_name}_{bleed_tag}{num_tag}{margin_tag}.pdf"

    print(f"\n=== KDP PDF変換開始 ===")
    print(f"  フォルダ  : {input_dir}")
    print(f"  判型      : {size_name}")
    print(f"  裁ち落とし: {bleed_ans}")
    print(f"  ノンブル  : {numbering_ans}")
    if numbering and skip_pages > 0:
        print(f"  ページ番号: {skip_pages + 1}枚目のファイルから開始")
    if skip_filenames:
        print(f"  番号スキップ: {', '.join(skip_filenames)}")
    if all_white:
        print(f"  白抜き     : すべて白文字")
    elif white_filenames:
        print(f"  白抜き強制 : {', '.join(white_filenames)}")
    print(f"  余白追加  : {'あり（10mm）' if add_margin else 'なし'}")
    print(f"  出力先    : {output_path}\n")

    make_pdf(
        input_dir=input_dir,
        output_path=output_path,
        size_name=size_name,
        bleed=bleed,
        numbering=numbering,
        skip_pages=skip_pages,
        dark_threshold=100.0,
        add_margin=add_margin,
        skip_filenames=skip_filenames,
        white_filenames=white_filenames,
        all_white=all_white,
    )

    print(f"\n✓ 完成: {output_path}")
    print(f"  ページ数: {len(png_files)}ページ")


if __name__ == "__main__":
    main()
