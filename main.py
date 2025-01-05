import itertools
import pathlib
from decimal import Decimal
from tkinter import filedialog

from PyPDF2 import PdfReader, PdfWriter, Transformation
import tkinter as tk
from tkinter import ttk

def make_writer_from_reader(reader):
    ret = PdfWriter()
    for page in reader.pages:
        ret.add_page(page)
    return ret


def align_length(pdf_file, mod=4, insert_position=-1):
    length = len(pdf_file.pages)
    if insert_position < 0:
        insert_position += length + 1

    while len(pdf_file.pages) % mod != 0:
        if insert_position >= length:
            pdf_file.add_blank_page()
        else:
            pdf_file.insert_blank_page(index=insert_position)

def arrange_pages_for_print(pdf_file):
    assert len(pdf_file.pages) % 4 == 0, "The number of Pages must be a multiple of 4"

    number_of_pages = len(pdf_file.pages)
    def translate_page(page):
        if page >= 0:
            return page
        else:
            return number_of_pages + page

    pages = []

    for page in range(number_of_pages // 2):
        pages.append(page)
        pages.append(translate_page(-page - 1))

    ret = PdfWriter()

    for page in pages:
        ret.add_page(pdf_file.pages[page])

    return ret


def combine_pages(pdf_file):
    assert len(pdf_file.pages) % 2 == 0, "The number of pages must be even"

    ret = PdfWriter()

    width = pdf_file.pages[0].mediabox.width
    height = pdf_file.pages[0].mediabox.height
    scale_factor = width / height

    op1 = (
        Transformation()
        .scale(sx=scale_factor, sy=scale_factor)
        .rotate(90)
        .translate(float(width), 0)
    )
    op2 = (
        Transformation()
        .scale(sx=scale_factor, sy=scale_factor)
        .rotate(90)
        .translate(float(width), float(width / Decimal("1.5")))
    )

    for page1, page2 in itertools.batched(pdf_file.pages, 2):

        page1.add_transformation(op1)
        page1.rotate(90)
        page2.add_transformation(op2)
        page1.merge_page(page2)

        ret.add_page(page1)

    return ret

def main():
    def open_input_file():
        filename = filedialog.askopenfilename(title="Select a PDF file",
                                              filetypes=(("PDF files", "*.pdf"), ("All Files", "*.*")))
        input_file_path.delete(0, tk.END)
        input_file_path.insert(0, filename)

    def open_output_file():
        filename = filedialog.asksaveasfilename(title="How should the output File be called", initialfile=f"{input_file_path.get()}-book.pdf", defaultextension=".pdf", filetypes=(("PDF files", "*.pdf"), ("All Files", "*.*")))

        path = pathlib.Path(filename)
        if path.is_file():
            answer = tk.messagebox.askyesno(title="File Override Confirmation",
                                            message=f"Do you really want to override `{path.name}`?")
        else:
            answer = True

        if answer:
            output_file_path.delete(0, tk.END)
            output_file_path.insert(0, filename)

    def run():
        base_file = make_writer_from_reader(PdfReader(input_file_path.get()))
        align_length(base_file, insert_position=-2 if leave_last_page.get() else -1)
        arranged_file = arrange_pages_for_print(base_file)
        output_file = combine_pages(arranged_file)
        output_file.write(output_file_path.get())

        tk.messagebox.showinfo(message="Finished!")


    root = tk.Tk()

    # Input File
    tk.Label(root, text="Input File Path").grid(row=0, column=0)
    input_file_path = tk.Entry(root)
    input_file_path.grid(row=0, column=1)
    open_button = tk.Button(root, text="Open Input File", command=open_input_file)
    open_button.grid(row=0, column=2)

    # Output File
    tk.Label(root, text="Output File Path").grid(row=1, column=0)
    output_file_path = tk.Entry(root)
    output_file_path.grid(row=1, column=1)
    open_button = tk.Button(root, text="Open Output File", command=open_output_file)
    open_button.grid(row=1, column=2)

    # Settings
    leave_last_page = tk.BooleanVar()
    ttk.Checkbutton(root, text="Last Page on Back", onvalue=True, offvalue=False, variable=leave_last_page).grid(row=2, column=1)

    # Run Button
    tk.Button(root, text="Go", command=run).grid(row=3, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    main()
