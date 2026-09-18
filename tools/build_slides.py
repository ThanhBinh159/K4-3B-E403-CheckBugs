"""Build a 6-page landscape PDF from editable content, with Vietnamese fonts."""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
# Workspace-local optional authoring packages; backend itself has no dependencies.
bundled = ROOT.parent / '.tools' / 'python-packages'
if bundled.is_dir():
    sys.path.insert(0, str(bundled))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

W, H, M = 1280, 720, 70
INK, MUTED, ACCENT = HexColor('#193331'), HexColor('#60736e'), HexColor('#246550')


def paragraph(c, text, x, top, width, size=24, color=INK, bold=False):
    style = ParagraphStyle('body', fontName='ArialBold' if bold else 'Arial', fontSize=size,
                           leading=size * 1.35, textColor=color)
    p = Paragraph(escape(text), style)
    _, height = p.wrap(width, 900)
    p.drawOn(c, x, top - height)
    return height


def main():
    import os
    font_root = Path(os.getenv('WINDIR', 'C:/Windows')) / 'Fonts'
    pdfmetrics.registerFont(TTFont('Arial', str(font_root / 'arial.ttf')))
    pdfmetrics.registerFont(TTFont('ArialBold', str(font_root / 'arialbd.ttf')))
    slides = json.loads((ROOT / 'slides' / 'content.json').read_text(encoding='utf-8'))
    if len(slides) != 6:
        raise ValueError('CP5 requires exactly 6 pages.')
    c = canvas.Canvas(str(ROOT / 'demo-slides.pdf'), pagesize=(W, H))
    c.setTitle('VLearn Grounded Tutor - CP5')
    c.setAuthor('VLearn Grounded Tutor - nhóm sẽ điền thông tin')
    for index, slide in enumerate(slides, 1):
        c.setFillColor(HexColor('#f8faf5'))
        c.rect(0, 0, W, H, stroke=0, fill=1)  # Page background, not illustration.
        top = H - 65
        title_height = paragraph(c, slide['title'], M, top, W - 2 * M, size=44, bold=True)
        top -= title_height + 25
        if slide.get('subtitle'):
            top -= paragraph(c, slide['subtitle'], M, top, W - 2 * M, size=21, color=ACCENT) + 24
        if slide.get('body') and index != 3:
            top -= paragraph(c, slide['body'], M, top, W - 2 * M, size=25) + 34
        cols = len(slide['table'][0])
        widths = ([440, 360, 340] if cols == 3 else [480, 660])
        cells = []
        for row_index, row in enumerate(slide['table']):
            style = ParagraphStyle('cell', fontName='ArialBold' if row_index == 0 else 'Arial',
                                   fontSize=22 if row_index == 0 else 23, leading=30, textColor=INK)
            cells.append([Paragraph(escape(text), style) for text in row])
        table = Table(cells, colWidths=widths)
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 26),
            ('TOPPADDING', (0, 0), (-1, -1), 15), ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, ACCENT),
            ('LINEBELOW', (0, 1), (-1, -1), .5, HexColor('#dbe4db')),
        ]))
        _, height = table.wrap(W - 2 * M, 600)
        if top - height < 140:
            raise ValueError(f'Slide {index} table overflows: reduce content, not fonts.')
        table.drawOn(c, M, top - height)
        top -= height + 26
        if index == 3:
            top -= paragraph(c, slide['body'], M, top, W - 2 * M, size=23) + 10
        note_height = paragraph(c, slide['note'], M, 105, W - 2 * M - 65, size=17, color=MUTED)
        if note_height > 70 or top < 116:
            raise ValueError(f'Slide {index} footer/content overlap.')
        c.setFont('Arial', 17)
        c.setFillColor(MUTED)
        c.drawRightString(W - M, 45, f'{index} / 6')
        c.showPage()
    c.save()
    print('Created demo-slides.pdf: 6 landscape pages.')
    try:
        import pymupdf as fitz
        output = ROOT / 'tmp' / 'slide-review'
        output.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(ROOT / 'demo-slides.pdf')
        for i, page in enumerate(doc, 1):
            page.get_pixmap(matrix=fitz.Matrix(1, 1)).save(output / f'slide-{i}.png')
        print('Rendered 6 pages for visual review.')
    except ImportError:
        print('Install pymupdf or render with Poppler for visual review.')


if __name__ == '__main__':
    main()
