import PySimpleGUI as sg

from forming_act import creation_of_acts


def main():
    layout = [[sg.Text("Выберите акт списания:")],
              [sg.Input(), sg.FileBrowse(key="-ACT-")],
              [sg.Text("Выберите остатки:")],
              [sg.Input(), sg.FileBrowse(key="-OST-")],
              [sg.Text("Выберите путь сохранения:")],
              [sg.Input(), sg.FolderBrowse(key="-SAVE-")],
              [sg.Button("Сформировать акт")]]

    window = sg.Window("Acts_EGAIS", layout)

    result = None

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == "Сформировать акт":
            file_path1 = values["-ACT-"]
            file_path2 = values["-OST-"]
            save_path = values["-SAVE-"]

            result = creation_of_acts(file_path1, file_path2, save_path)

        if result is not None:
            layout_result = [[sg.Text(result)],
                             [sg.Button('Ок')]]

            window_result = sg.Window('Результат',
                                      layout_result,
                                      size=(320, 80))

            while True:
                event_result, values_result = window_result.read()
                if event_result == sg.WINDOW_CLOSED or event_result == 'Ок':
                    result = None
                    break

            window_result.close()

    window.close()


if __name__ == "__main__":
    main()
