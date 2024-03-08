import json
import sys
import os
import subprocess
import time
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Alignment, Border, Side

sys.path.append("/".join(__file__.split("/")[0:-2]))
# pylint: disable-next=wrong-import-position
from lib.aux import orange, purple


components_keys = [
    "abastecimento-de-agua",
    "esgotamento-sanitario",
    "manejo-das-aguas-pluviais",
    "manejo-de-residuos-solidos",
]
components_uppercase = [
    "ABASTECIMENTO DE ÁGUA",
    "ESGOTAMENTO SANITÁRIO",
    "MANEJO DAS ÁGUAS PLUVIAIS",
    "MANEJO DE RESÍDUOS SÓLIDOS",
]


def merge_and_center(tab, start_row, end_row, start_column, end_column=None):
    tab.merge_cells(
        start_row=start_row,
        start_column=start_column,
        end_row=end_row,
        end_column=end_column if end_column else start_column,
    )
    tab.cell(row=start_row, column=start_column).alignment = Alignment(
        vertical="center", horizontal="center"
    )


def paint_cells(tab, color, row, column):
    fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    cell = tab.cell(row=row, column=column)
    cell.fill = fill


def set_border(tab, row, column):
    border = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000"),
    )
    cell = tab.cell(row=row, column=column)
    cell.border = border


def set_header_to_tab_3_3(tab, aux, key):

    component_uppercase = components_uppercase[components_keys.index(key)]

    tab.cell(row=aux + 3, column=1).value = "COMPONENTE: " + component_uppercase
    tab.cell(row=aux + 4, column=1).value = "OBJETIVO"
    tab.cell(row=aux + 4, column=2).value = "PROJETO"
    tab.cell(row=aux + 4, column=3).value = "DESCRIÇÃO DA AÇÃO PROPOSTA"
    tab.cell(row=aux + 4, column=4).value = "HORIZONTE DO PMSB (anos)"

    merge_and_center(tab, aux + 3, aux + 3, 1, 23)
    merge_and_center(tab, aux + 4, aux + 5, 1)
    merge_and_center(tab, aux + 4, aux + 5, 2)
    merge_and_center(tab, aux + 4, aux + 5, 3)
    merge_and_center(tab, aux + 4, aux + 4, 4, 23)

    paint_cells(tab, "8EAADB", aux + 3, 1)
    paint_cells(tab, "B4C6E7", aux + 4, 1)
    paint_cells(tab, "B4C6E7", aux + 4, 2)
    paint_cells(tab, "B4C6E7", aux + 4, 3)
    paint_cells(tab, "B4C6E7", aux + 4, 4)

    set_border(tab, aux + 3, 1)
    set_border(tab, aux + 4, 1)
    set_border(tab, aux + 4, 2)
    set_border(tab, aux + 4, 3)
    set_border(tab, aux + 4, 4)

    for i in range(20):
        tab.cell(row=aux + 5, column=i + 4).value = i + 1
        paint_cells(tab, "B4C6E7", aux + 5, i + 4)
        set_border(tab, aux + 5, i + 4)


def get_actions_index(deadline):

    if "Imediato" in deadline or "Emergencial" in deadline:
        return 1
    elif "Curto" in deadline:
        return 2
    elif "Médio" in deadline:
        return 3
    elif "Longo" in deadline:
        return 4
    else:
        # TODO: Veriricar outras strings como Ano menor q o atual, etc...
        print(
            f"Prazo {orange(deadline)} não identificado, assumindo como {purple('Imediato')}"
        )
        return 1


def generate_tab_3_1(data_json, tab):

    aux = 0

    for key in components_keys:
        component_uppercase = components_uppercase[components_keys.index(key)]
        for i, value in enumerate(data_json[key]):

            deadline = value.get("deadline")
            objective = value.get("objective")
            count_objectives = len(data_json[key])
            start_row = aux + 2
            end_row = aux + 1 + len(data_json[key])
            row = i + start_row

            tab.cell(row=row, column=1).value = component_uppercase
            tab.cell(row=row, column=2).value = count_objectives
            tab.cell(row=row, column=3).value = objective

            if deadline:
                tab.cell(row=row, column=4).value = deadline

        merge_and_center(tab, start_row, end_row, 1)
        merge_and_center(tab, start_row, end_row, 2)
        aux += len(data_json[key])


def generate_tab_3_2(data_json, tab):

    header_rows = 4  # rows on header plus 1

    for key in components_keys:

        row = components_keys.index(key) + header_rows
        count_actions_splited = [0, 0, 0, 0, 0]

        for _, value in enumerate(data_json[key]):

            actions = value.get("actions")
            deadline = value.get("deadline")

            if not actions or not deadline:
                continue

            index = get_actions_index(deadline)
            count_actions_splited[0] += len(actions)
            count_actions_splited[index] += len(actions)

        tab.cell(row=row, column=2).value = count_actions_splited[0]
        for i in range(4):
            tab.cell(row=row, column=(i * 2) + 3).value = count_actions_splited[i + 1]


def generate_tab_3_3(data_json, tab):

    aux = -2
    header_rows = 4  # rows on header plus 1

    for key in components_keys:

        set_header_to_tab_3_3(tab, aux, key)
        aux += header_rows

        for i, value in enumerate(data_json[key]):

            actions = value["actions"]

            if not actions:
                continue

            start_row = aux + i + 2
            end_row = aux + i + 1 + len(actions)

            for j, action in enumerate(actions):

                row = j + start_row
                objective = value.get("objective")

                tab.cell(row=row, column=1).value = objective
                tab.cell(row=row, column=3).value = action

                set_border(tab, row, 1)
                set_border(tab, row, 2)
                set_border(tab, row, 3)

                for k in range(20):
                    set_border(tab, row, header_rows + k)

            merge_and_center(tab, start_row, end_row, 1)
            aux += len(actions) - 1

        aux += len(data_json[key])


if __name__ == "__main__":

    with open("data/funasa.json", encoding="utf-8") as file:
        funasa = json.load(file)
    with open("cfg.json", encoding="utf-8") as f:
        excel_file_path = json.load(f)["excel_file_path"]

    workbook = load_workbook(excel_file_path)

    generate_tab_3_1(funasa, workbook["Quadro3.1"])
    generate_tab_3_2(funasa, workbook["Quadro3.2"])
    generate_tab_3_3(funasa, workbook["Quadro3.3"])

    workbook.save("tmp/sheet.xlsx")

    try:
        # fecha o LibreOffice se já estiver aberto
        subprocess.Popen(["pkill", "soffice"])
        # sleep para dar tempo de fechar o LibreOffice
        time.sleep(1)
        with open(os.devnull, "w", encoding="utf-8") as devnull:
            # TODO: Usar excel no lugar do libreoffice
            subprocess.Popen(
                ["libreoffice", "tmp/sheet.xlsx"], stdout=devnull, stderr=devnull
            )
    except Exception as e:
        print("Erro ao abrir o LibreOffice:", e)
