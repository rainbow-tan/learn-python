import os.path
from typing import List

import openpyxl
from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def read_xlsx(filename: str, sheet_name: str) -> List[list]:
    filename = os.path.abspath(filename)
    assert os.path.isfile(filename)
    wb: Workbook = openpyxl.load_workbook(filename)
    assert sheet_name in wb.sheetnames, "sheet name error"
    ws: Worksheet = wb[sheet_name]
    all_data = []
    for row in ws.rows:
        data_row = []
        for data in row:
            cell: Cell = data
            data_row.append(cell.value)
        all_data.append(data_row)
    print("all data".center(50, '*'))
    for one in all_data:
        print(one)
    return all_data


def main():
    filename = "SCD_SeriesFolderItemName_ForV1_Before.xlsx"
    sheet_name = "Sheet1"
    all_data = read_xlsx(filename, sheet_name)


if __name__ == '__main__':
    main()
