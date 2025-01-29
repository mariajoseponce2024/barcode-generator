import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter

def generar_codigo_barras(codigo, nombre_archivo_imagen):
    writer = ImageWriter()
    writer.set_options({"module_height": 5.0})
    codigo_barras = Code128(codigo, writer=writer)
    codigo_barras.save(nombre_archivo_imagen)

def crear_pdf_con_codigos_barras(nombre_archivo_pdf, codigos):
    c = canvas.Canvas(nombre_archivo_pdf)
    x, y = 100, 750

    for codigo in codigos:
        nombre_archivo_imagen = f"codigo_barras_{codigo}"
        generar_codigo_barras(codigo, nombre_archivo_imagen)
        c.drawString(x, y, f"Código: {codigo}")
        c.drawImage(nombre_archivo_imagen + ".png", x, y - 70, width=150, height=60)
        y -= 120

        if y < 100:
            c.showPage()
            y = 750

    c.save()

def generar_pdf():
    inicio = entry_inicio.get()
    fin = entry_fin.get()
    archivo_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

    if not archivo_pdf:
        return

    try:
        inicio = int(inicio)
        fin = int(fin)
        codigos = [str(i) for i in range(inicio, fin + 1)]
        crear_pdf_con_codigos_barras(archivo_pdf, codigos)
        messagebox.showinfo("Éxito", f"PDF generado: {archivo_pdf}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresá números válidos para el rango.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

ventana = tk.Tk()
ventana.title("Generador de Códigos de Barras")
ventana.geometry("500x300")
ventana.configure(bg="#f0f0f0")

frame = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=30)

tk.Label(frame, text="Generador de Códigos de Barras", font=("Helvetica", 16), bg="#ffffff").pack(pady=10)
tk.Label(frame, text="Inicio del rango:", bg="#ffffff").pack(anchor="w")
entry_inicio = tk.Entry(frame)
entry_inicio.pack(pady=5, fill="x")

tk.Label(frame, text="Fin del rango:", bg="#ffffff").pack(anchor="w")
entry_fin = tk.Entry(frame)
entry_fin.pack(pady=5, fill="x")

tk.Button(frame, text="Generar PDF", command=generar_pdf, bg="#4CAF50", fg="white").pack(pady=20, ipadx=10)

ventana.mainloop()
