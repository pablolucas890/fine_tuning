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
components_upper = [
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

    component_upper = components_upper[components_keys.index(key)]

    tab.cell(row=aux + 3, column=1).value = "COMPONENTE: " + component_upper
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


def generate_tab_3_1(data_json, tab):

    aux = 0

    for key in components_keys:
        component_upper = components_upper[components_keys.index(key)]
        for index, value in enumerate(data_json[key]):
            number_of_objectives = len(data_json[key])
            tab.cell(row=index + aux + 2, column=1).value = component_upper
            tab.cell(row=index + aux + 2, column=2).value = number_of_objectives
            tab.cell(row=index + aux + 2, column=3).value = value["objective"]
            if value.get("deadline"):
                tab.cell(row=index + aux + 2, column=4).value = value["deadline"]
        merge_and_center(tab, aux + 2, aux + 1 + len(data_json[key]), 1)
        merge_and_center(tab, aux + 2, aux + 1 + len(data_json[key]), 2)
        aux += len(data_json[key])


def generate_tab_3_2(data_json, tab):

    for key in components_keys:

        index = components_keys.index(key)
        len_actions = [0, 0, 0, 0, 0]

        for _, value in enumerate(data_json[key]):
            if not value.get("actions"):
                continue
            len_actions[0] += len(value["actions"])
            if "Imediato" in value["deadline"] or "Emergencial" in value["deadline"]:
                len_actions[1] += len(value["actions"])
            elif "Curto" in value["deadline"]:
                len_actions[2] += len(value["actions"])
            elif "Médio" in value["deadline"]:
                len_actions[3] += len(value["actions"])
            elif "Longo" in value["deadline"]:
                len_actions[4] += len(value["actions"])
            else:
                # TODO: Veriricar outras strings como Ano menor q o atual, etc...
                print(
                    f"Prazo {orange( value['deadline'])} não identificado, assumindo como {purple('Imediato')}"
                )
                len_actions[1] += len(value["actions"])
        tab.cell(row=index + 4, column=2).value = len_actions[0]
        tab.cell(row=index + 4, column=3).value = len_actions[1]
        tab.cell(row=index + 4, column=5).value = len_actions[2]
        tab.cell(row=index + 4, column=7).value = len_actions[3]
        tab.cell(row=index + 4, column=9).value = len_actions[4]


def generate_tab_3_3(data_json, tab):

    aux = -2
    for key in components_keys:
        set_header_to_tab_3_3(tab, aux, key)
        aux += 4
        for i, value in enumerate(data_json[key]):
            if not value.get("actions"):
                continue
            actions = value["actions"]
            for j, data in enumerate(actions):
                tab.cell(row=i + j + aux + 2, column=3).value = data
                tab.cell(row=i + j + aux + 2, column=1).value = value["objective"]
                set_border(tab, i + j + aux + 2, 1)
                set_border(tab, i + j + aux + 2, 2)
                set_border(tab, i + j + aux + 2, 3)
                for k in range(20):
                    set_border(tab, i + j + aux + 2, k + 4)
            merge_and_center(tab, aux + i + 2, aux + i + 1 + len(actions), 1)
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
