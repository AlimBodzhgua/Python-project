import tkinter as tk
import pdfplumber
from gtts import gTTS

from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox


class Window:
    window = tk.Tk()
    window.geometry("400x200")
    window.title("Window")
    window.resizable(False, False)


class Converter:

    @staticmethod
    def extract_pdf_text(path):
        text = ""
        try:
            with pdfplumber.open(path) as pdf:
                pages = pdf.pages
                for page in pages:
                    page_text = page.extract_text()
                    page_text = page_text.replace("\n", ' ')
                    text += page_text
            
            return text
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")

    @staticmethod
    def convert_to_mp3(text, new_file_name,language):
        text = text 
        new_file_name = new_file_name + ".mp3"
        tts = gTTS(text, lang=language)
        tts.save(new_file_name)
        messagebox.showinfo("Info", f"File {new_file_name} successfully saved")


class Application(Window):
    window = Window.window
    app_title = "Convert text to mp3"
    window.title(app_title)

    main_frame = tk.Frame(window)
    main_frame.pack()

    tk.Label(main_frame, text="Choose you file").grid(row=0, column=0)
    path_name_field = tk.Entry(main_frame, width=30)
    path_name_field.grid(row=1, column=0)

    open_button = tk.Button(main_frame, text="open file")
    open_button.grid(row=1, column=1)

    tk.Label(main_frame, text="Choose the name for new file and language").grid(row=2, column=0)
    file_name_field = tk.Entry(main_frame)
    file_name_field.grid(row=3, column=0)

    language_box = ttk.Combobox(main_frame, values=('ru', 'en'), width=3)
    language_box.current(0)
    language_box.grid(row=3, column=1)

    create_button = tk.Button(main_frame, text="create")
    create_button.grid(row=4, column=0)


    def __init__(self, name=app_title):
        self.window.title(name)


    @classmethod
    def run(cls):
        Application.open_button.config(command=Application.select_file)
        Application.create_button.config(command=Application.create)
        Application.window.mainloop()


    @classmethod
    def select_file(cls):
        filetypes = (("pdf files", "*.pdf"),)

        filename = fd.askopenfilename(initialdir='/', filetypes=filetypes)
        
        Application.path_name_field.delete(0, tk.END)
        Application.path_name_field.insert(0, filename)
        Application.path_name_field.config(state=tk.DISABLED)


    @classmethod
    def create(cls):
        file_path = Application.path_name_field.get()
        new_file_name = Application.file_name_field.get()
        if(new_file_name == ''):
            return messagebox.showerror("Error", "Enter the name field")
        language = Application.language_box.get()
        text = Converter.extract_pdf_text(file_path)
        Converter.convert_to_mp3(text, new_file_name, language)
        



if __name__ == "__main__":
    Application.run()




