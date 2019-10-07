from numbers import Number
import csv
import xlrd


def get_lcia_categories(source_data, version):
    with csv.open(
        source_data / "categoryUUIDs.csv", encoding="latin-1", delimiter=";"
    ) as csv_file:
        next(csv_file)  # Skip header row
        csv_data = [
            {
                "name": (line[0], line[2], line[4]),
                # 'unit': line[6],
                "description": line[7],
            }
            for line in csv_file
        ]

    return csv_data


def get_lcia_cfs(source_data, version):
    sheet = xlrd.open_workbook(
        source_data / version / "LCIA_implementation.xlsx"
    ).sheet_by_name("CFs")

    EXCLUDED = {"selected LCI results, additional", "selected LCI results"}

    cf_data = [
        {
            "method": (
                sheet.cell(row, 0).value,
                sheet.cell(row, 1).value,
                sheet.cell(row, 2).value,
            ),
            "name": sheet.cell(row, 3).value,
            "categories": (sheet.cell(row, 4).value, sheet.cell(row, 5).value),
            "amount": sheet.cell(row, 7).value,
        }
        for row in range(1, sheet.nrows)
        if sheet.cell(row, 0).value not in EXCLUDED
        and isinstance(sheet.cell(row, 7).value, Number)
    ]

    return cf_data


def get_lcia_units(source_data, version):
    sheet = xlrd.open_workbook(
        source_data / version / "LCIA_implementation.xlsx"
    ).sheet_by_name("units")

    units = {
        (
            sheet.cell(row, 0).value,
            sheet.cell(row, 1).value,
            sheet.cell(row, 2).value,
        ): sheet.cell(row, 3).value
        for row in range(1, sheet.nrows)
    }

    return units
