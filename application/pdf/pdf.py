from decimal import Decimal
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import PDF
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import FixedColumnWidthTable, TableCell
from borb.pdf import Barcode, BarcodeType
from borb.pdf import X11Color
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont

from pathlib import Path


def create_pdf(**params):
    """
    Параметры
    title (str) заголовок
    barcode_data (str) данные для штрихкода,
    table_header (list or tuble) заголовки столбцов
    table_rows (list or tuple) данные строк, каждая строка это список
    output (стр) имя pdf файла
    """
    document = Document()
    page = Page()
    path = Path(__file__).parent / 'fonts' / 'arial.ttf'
    arial_font = TrueTypeFont.true_type_font_from_file(path)
    path = Path(__file__).parent / 'fonts' / 'arialbd.ttf'
    arialbd_font = TrueTypeFont.true_type_font_from_file(path)

    # Layout
    layout = SingleColumnLayout(page)

    if 'title' in params:
        title = params['title']
        # Create and add heading
        layout.add(Paragraph(title, font=arialbd_font, font_size=Decimal(20)))

    if 'barcode_data' in params.keys():
        # Create and add barcode
        layout.add(Barcode(data=params['barcode_data'], type=BarcodeType.QR, width=Decimal(64), height=Decimal(64)))

    # Create and add table
    if 'table_header' in params and 'table_rows' in params:
        table_header = params['table_header']
        table_rows = params['table_rows']
        number_of_colums = len(table_header)
        number_of_rows = len(table_rows)
        table = FixedColumnWidthTable(
            number_of_rows=1+len(table_rows), number_of_columns=number_of_colums
        )
        table01 = FixedColumnWidthTable(
            number_of_rows=1, number_of_columns=4
        )

        # Header row
        for colum_name in table_header:
            table.add(
                TableCell(
                    Paragraph(
                        colum_name,
                        font_color=X11Color('White'),
                        font=arial_font),
                    background_color=X11Color('SlateGray')
                )
            )
    	# Data rows
        for row in table_rows:
            for col in range(number_of_colums):
                val = ''
                if col < len(row):
                    val = row[col]
                table.add(Paragraph(str(val), font=arial_font))

        # Set padding
        table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(table)

    # Append page
    document.add_page(page)

    if 'output' in params:
        # Persist PDF to file
        output = params['output']
        with open(output, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, document)