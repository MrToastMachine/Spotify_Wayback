import PySimpleGUI as sg

def main():
    # Define the layout
    layout = [
        [sg.Text("Title:"), sg.InputText(key="title")],
        [sg.Text("Description:"), sg.InputText(key="description")],
        [sg.Text("Date Format:"), sg.Radio("MM/DD/YYYY", "date_format", default=True), sg.Radio("DD/MM/YYYY", "date_format")],
        [sg.Text("Singles:"), sg.Checkbox("Yes", key="singles")],
        [sg.Text("Number (1-10):"), sg.Slider(range=(1, 10), orientation="h", key="number")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    # Create the window
    window = sg.Window("Input Form", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Submit":
            title = values["title"]
            description = values["description"]
            date_format = "MM/DD/YYYY" if values[0] else "DD/MM/YYYY"
            singles = values["singles"]
            number = int(values["number"])

            # You can do something with the inputs here, like printing them
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Date Format: {date_format}")
            print(f"Singles: {singles}")
            print(f"Number: {number}")

            window.close()

    window.close()

if __name__ == "__main__":
    main()
