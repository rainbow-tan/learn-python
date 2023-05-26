import os
from typing import List

import xlrd
from xlrd import Book
from xlrd.sheet import Sheet


def read_xlsx(filename: str, sheet_name: str) -> List[list]:
    filename = os.path.abspath(filename)
    assert os.path.isfile(filename), f'{filename} is not file'
    wb: Book = xlrd.open_workbook(filename)
    sheet_names = wb.sheet_names()
    assert sheet_name in sheet_names, 'sheet name error'
    sheet: Sheet = wb.sheet_by_name(sheet_name)
    all_data = []
    for row_x in range(sheet.nrows):
        row = []
        for col_x in range(sheet.ncols):
            row.append(sheet.cell(row_x, col_x).value)
        all_data.append(row)
    print("all data".center(50, '*'))
    for one in all_data:
        print(one)
    return all_data


def main():
    read_xlsx("SCD_SeriesFolderItemName_ForV1_Before.xls", "Sheet1")


if __name__ == '__main__':
    main()
