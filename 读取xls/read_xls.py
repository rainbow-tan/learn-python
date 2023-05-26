import os
from typing import List

import xlrd
import xlwt
from xlrd import Book
from xlrd.sheet import Sheet
from xlwt import Workbook


def read_xls(filename: str, sheet_name: str) -> List[list]:
    filename = os.path.abspath(filename)
    assert os.path.isfile(filename), f'{filename} is not file'
    assert filename.lower().endswith('.xls'), f'不是.xls文件:{filename}'
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


def write_xls(filename: str, sheet_name: str, data: List[list]):
    filename = os.path.abspath(filename)
    assert filename.lower().endswith('.xls'), f'不是.xls文件:{filename}'
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    wb: Workbook = xlwt.Workbook(filename)
    sheet: xlwt.Worksheet = wb.add_sheet(sheet_name)
    for row_x, row in enumerate(data):
        for clo_x, clo in enumerate(row):
            sheet.write(row_x, clo_x, clo)
    wb.save(filename)
    print(f"保存到路径:{filename}")


def main():
    all_data = read_xls("SCD_SeriesFolderItemName_ForV1_Before.xls", "Sheet1")
    write_xls("new.xls", "Sheet1", all_data)


if __name__ == '__main__':
    main()
