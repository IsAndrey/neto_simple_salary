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
from borb.pdf import Alignment
from pathlib import Path


Russian_Fonts = {
    'arial': TrueTypeFont.true_type_font_from_file(
        Path(__file__).parent / 'fonts' / 'arial.ttf'
    ),
    'arial_bold': TrueTypeFont.true_type_font_from_file(
        Path(__file__).parent / 'fonts' / 'arialbd.ttf'
    ),
}

def create_pdf(**params):
    """
    Параметры
    title (str) заголовок
    barcode_data (str) данные для штрихкода,
    table_header (list or tuple) заголовки столбцов
    table_rows (list or tuple) данные строк, каждая строка это список
    output (стр) имя pdf файла
    """
    document = Document()
    page = Page()
    '''
    path = Path(__file__).parent / 'fonts' / 'arial.ttf'
    arial_font = TrueTypeFont.true_type_font_from_file(path)
    path = Path(__file__).parent / 'fonts' / 'arialbd.ttf'
    arialbd_font = TrueTypeFont.true_type_font_from_file(path)
    '''

    # Layout
    layout = SingleColumnLayout(page)

    if 'title' in params:
        title = params['title']
        # Create and add heading
        layout.add(
            Paragraph(
                title,
                font=Russian_Fonts['arial_bold'],
                font_size=Decimal(20),
                horizontal_alignment=Alignment.CENTERED
            )
        )

    if 'barcode_data' in params.keys():
        # Create and add barcode
        layout.add(Barcode(data=params['barcode_data'], type=BarcodeType.QR, width=Decimal(64), height=Decimal(64)))

    # Create and add table
    if 'table_header' in params and 'table_rows' in params:
        table_header = params['table_header']
        table_rows = params['table_rows']
        number_of_colums = len(table_header)
        number_of_rows = len(table_rows)+1
        table = FixedColumnWidthTable(
            number_of_rows=number_of_rows, number_of_columns=number_of_colums
        )

        # Header row
        alignment = Alignment.CENTERED
        for colum_name in table_header:
            table.add(
                TableCell(
                    Paragraph(
                        colum_name,
                        font_color=X11Color('White'),
                        font=Russian_Fonts['arial'],
                        horizontal_alignment=alignment
                    ),
                    background_color=X11Color('SkyBlue')
                )
            )
    	# Data rows
        for row in table_rows:
            alignment = Alignment.LEFT
            for col in range(number_of_colums):
                val = ''
                if col < len(row):
                    val = row[col]
                if col == len(row)-2:
                    alignment = Alignment.RIGHT
                table.add(Paragraph(str(val), font=Russian_Fonts['arial'], horizontal_alignment=alignment))

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
