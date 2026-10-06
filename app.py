import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONFIGURACIÓN DE FONEMAS EXACTA SEGÚN LA IMAGEN ---
FILA_1_VOCALES = ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"]
FILA_2_CONSONANTES_1 = ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"]
FILA_3_CONSONANTES_2 = ["/g/", "/ñ/", "/y/", "/j/", "/s/"]
FILA_4_SINFONES_1 = ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"]
FILA_5_SINFONES_2 = ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"]
FILA_6_SINFONES_EDAD = ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]

SINFONES_HOMOSILABICOS = {"/bl/", "/cl/", "/fl/", "/gl/", "/pl/", "/tl/", "/br/", "/cr/", "/dr/", "/fr/", "/tr/", "/pr/", "/gr/", "/kl/", "/kr/"}
SINFONES_HETEROSILABICOS = {"/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/", "/nd/", "/nt/", "/ns/"}

ESTADOS = {
    "LOGRA": {"bg": "#DCFCE7", "border": "#86EFAC", "text": "#065F46"},
    "NO_LOGRA": {"bg": "#FEE2E2", "border": "#FCA5A5", "text": "#881337"},
    "NO_VALORADO": {"bg": "#FFFFFF", "border": "#CBD5E1", "text": "#475569"},
    "NO_ESPERADO": {"bg": "#E2E8F0", "border": "#94A3B8", "text": "#334155"}
}

ORDEN_ESTADOS = ["LOGRA", "NO_LOGRA", "NO_VALORADO", "NO_ESPERADO"]
T_LETRA_CUADROS = ("Century Gothic", 10, "bold")
T_LEYENDA = ("Century Gothic", 10, "bold")

class EvaluadorGraficoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurador de Evaluación Fonológica")
        self.root.geometry("1480x920")
        self.root.configure(bg="#FFFFFF")
        
        self.respuestas = {}
        
        todos_elementos = (FILA_1_VOCALES + FILA_2_CONSONANTES_1 + FILA_3_CONSONANTES_2 + 
                          FILA_4_SINFONES_1 + FILA_5_SINFONES_2 + FILA_6_SINFONES_EDAD)
        
        for s in todos_elementos:
            if s in FILA_1_VOCALES or s in FILA_2_CONSONANTES_1 or s in FILA_3_CONSONANTES_2:
                self.respuestas[s] = "LOGRA"
            else:
                self.respuestas[s] = "NO_LOGRA"
        
        self.crear_widgets()

    def crear_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        tab_grafico = tk.Frame(notebook, bg="#FFFFFF")
        notebook.add(tab_grafico, text="1. Matriz Fonológica")

        tab_analisis = tk.Frame(notebook, bg="#FFFFFF")
        notebook.add(tab_analisis, text="2. Análisis y Niveles del Lenguaje")

        self.construir_tab_grafico(tab_grafico)
        self.construir_tab_analisis(tab_analisis)

    def construir_tab_grafico(self, parent):
        main_frame = tk.Frame(parent, bg="#FFFFFF")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Leyenda superior
        leyenda_frame = tk.Frame(main_frame, bg="#FFFFFF")
        leyenda_frame.pack(fill=tk.X, pady=(0, 15))
        
        items_leyenda = [
            ("Logra", "LOGRA"),
            ("No Logra", "NO_LOGRA"),
            ("No valorado", "NO_VALORADO"),
            ("No esperado para su edad", "NO_ESPERADO")
        ]
        
        for txt, est in items_leyenda:
            f = tk.Frame(leyenda_frame, bg="#FFFFFF")
            f.pack(side=tk.LEFT, padx=12)
            tk.Label(f, text="  ", bg=ESTADOS[est]["bg"], bd=1, relief=tk.SOLID, width=3).pack(side=tk.LEFT, padx=4)
            tk.Label(f, text=txt, font=T_LEYENDA, bg="#FFFFFF", fg="#1E293B").pack(side=tk.LEFT)

        self.grid_container = tk.Frame(main_frame, bg="#FFFFFF")
        self.grid_container.pack(fill=tk.BOTH, expand=True)

        filas = [
            FILA_1_VOCALES,
            FILA_2_CONSONANTES_1,
            FILA_3_CONSONANTES_2,
            FILA_4_SINFONES_1,
            FILA_5_SINFONES_2,
            FILA_6_SINFONES_EDAD
        ]

        for i, fila in enumerate(filas):
            self.crear_fila_botones(fila, i)

        btn_generar = tk.Button(main_frame, text="GENERAR GRÁFICO (PNG)", font=("Century Gothic", 11, "bold"), 
                                bg="#2563EB", fg="white", activebackground="#1D4ED8", activeforeground="white",
                                padx=20, pady=8, cursor="hand2", command=self.generar_imagen)
        btn_generar.pack(pady=(15, 0))

    def crear_fila_botones(self, simbolos, fila_idx):
        fila_frame = tk.Frame(self.grid_container, bg="#FFFFFF")
        fila_frame.grid(row=fila_idx, column=0, sticky="w", pady=4)
        
        for col_idx, simbolo in enumerate(simbolos):
            cfg = ESTADOS[self.respuestas[simbolo]]
            btn = tk.Button(fila_frame, text=simbolo, font=T_LETRA_CUADROS, width=5, height=2, bd=1, 
                            relief=tk.SOLID, cursor="hand2", bg=cfg["bg"], fg=cfg["text"])
            btn.config(command=lambda b=btn, s=simbolo: self.rotar_estado(b, s))
            btn.grid(row=0, column=col_idx, padx=2)

    def rotar_estado(self, boton, simbolo):
        actual = self.respuestas[simbolo]
        nuevo = ORDEN_ESTADOS[(ORDEN_ESTADOS.index(actual) + 1) % len(ORDEN_ESTADOS)]
        self.respuestas[simbolo] = nuevo
        cfg = ESTADOS[nuevo]
        boton.config(bg=cfg["bg"], fg=cfg["text"])

    def construir_tab_analisis(self, parent):
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        btn_analizar = tk.Button(frame, text="🔄 Actualizar Análisis desde la Matriz", font=("Century Gothic", 10, "bold"),
                                 bg="#059669", fg="white", activebackground="#047857", activeforeground="white",
                                 padx=10, pady=5, cursor="hand2", command=self.generar_analisis_texto)
        btn_analizar.pack(anchor="w", pady=(0, 10))

        self.txt_informe = tk.Text(frame, font=("Century Gothic", 10), wrap=tk.WORD, bd=1, relief=tk.SOLID)
        self.txt_informe.pack(fill=tk.BOTH, expand=True)

        self.generar_analisis_texto()

    def generar_analisis_texto(self):
        no_logrados = [s for s, est in self.respuestas.items() if est in ["NO_LOGRA", "NO_ESPERADO"]]
        
        homo = [s for s in no_logrados if s in SINFONES_HOMOSILABICOS]
        hetero = [s for s in no_logrados if s in SINFONES_HETEROSILABICOS]
        
        texto = "INFORME DE EVALUACIÓN FONOLÓGICA Y DEL LENGUAJE\n"
        texto += "=================================================\n\n"
        texto += "1. NIVEL FONOLÓGICO\n"
        texto += "Presenta dificultad en los siguientes sonidos:\n"
        
        if "/r/" in no_logrados:
            texto += "• Vibrante alveolar simple /r/ en posición media de palabra.\n"
        if "/rr/" in no_logrados:
            texto += "• Vibrante alveolar múltiple /rr/ en posición inicial, media y final de palabra.\n"
        if homo:
            texto += f"• Grupos consonánticos homosilábicos: {', '.join(homo)}. Realizando distorsión o sustitución de los sonidos.\n"
        if hetero:
            texto += f"• Grupos consonánticos heterosilábicos: {', '.join(hetero)}, realizando distorsión de los sonidos.\n"
        if not no_logrados:
            texto += "• No se observan dificultades en los fonemas evaluados.\n"
            
        texto += "\n2. NIVEL SEMÁNTICO\n"
        texto += "• Vocabulario limitado.\n"
        texto += "• Dificultades para recuperar palabras conocidas.\n"
        texto += "• Con apoyo identifica campos semánticos y elementos relacionados.\n\n"

        texto += "3. NIVEL MORFOSINTÁCTICO\n"
        texto += "• Expresa concordancia de género y número.\n"
        texto += "• Utiliza tiempos verbales en presente.\n"
        texto += "• Dificultad con el uso y comprensión de pronombres personales y posesivos.\n\n"

        texto += "4. NIVEL PRAGMÁTICO\n"
        texto += "• Predominio de gestos.\n"
        texto += "• Usa el lenguaje para funciones pragmáticas básicas como pedir o mostrar algo.\n\n"

        texto += "5. CONCLUSIONES Y SUGERENCIAS\n"
        texto += "El alumno muestra desfase a nivel fonológico, semántico y morfosintáctico. De acuerdo a su edad cronológica ya debería haber consolidado la mayoría de los fonemas. Se estimulará a través de terapia de lenguaje."

        self.txt_informe.delete("1.0", tk.END)
        self.txt_informe.insert(tk.END, texto)

    def generar_imagen(self):
        fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
        ax.set_xlim(0, 1600)
        ax.set_ylim(0, 900)
        ax.axis("off")

        # Leyenda superior en Matplotlib
        x_ley, y_ley = 50, 850
        leyenda_items = [
            ("Logra", "LOGRA"),
            ("No Logra", "NO_LOGRA"),
            ("No valorado", "NO_VALORADO"),
            ("No esperado para su edad", "NO_ESPERADO")
        ]

        for txt, est in leyenda_items:
            cfg = ESTADOS[est]
            ax.add_patch(patches.Circle((x_ley, y_ley), radius=10, facecolor=cfg["bg"], edgecolor=cfg["border"], linewidth=2, zorder=2))
            ax.text(x_ley + 20, y_ley, txt, fontfamily="Century Gothic", fontsize=11, fontweight="bold", va="center", color="#1E293B", zorder=2)
            x_ley += 220

        box_w, box_h = 70, 70
        gap_x = 18

        def draw_card(text, x, y, est_key):
            cfg = ESTADOS[est_key]
            box = patches.FancyBboxPatch(
                (x, y), box_w, box_h,
                boxstyle="round,pad=0.2,rounding_size=8",
                linewidth=1.5, edgecolor=cfg["border"], facecolor=cfg["bg"], zorder=2
            )
            ax.add_patch(box)
            
            font_size = 13 if len(text) <= 4 else 10
            
            # Tipografía Century Gothic especificada explícitamente para el texto generado en PNG
            ax.text(
                x + box_w / 2, y + box_h / 2, text,
                color=cfg["text"], fontfamily="Century Gothic", fontsize=font_size, fontweight="bold",
                ha="center", va="center", zorder=3
            )

        filas = [
            (FILA_1_VOCALES, 730),
            (FILA_2_CONSONANTES_1, 620),
            (FILA_3_CONSONANTES_2, 510),
            (FILA_4_SINFONES_1, 400),
            (FILA_5_SINFONES_2, 290),
            (FILA_6_SINFONES_EDAD, 180)
        ]

        for simbolos, y_pos in filas:
            for idx, symbol in enumerate(simbolos):
                draw_card(symbol, 50 + idx * (box_w + gap_x), y_pos, self.respuestas[symbol])

        plt.tight_layout()
        
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("Imagen PNG", "*.png"), ("Todos los archivos", "*.*")]
        )
        
        if nombre_archivo:
            plt.savefig(nombre_archivo, bbox_inches="tight", dpi=300)
            messagebox.showinfo("✅ Éxito", f"La imagen se ha guardado correctamente en:\n{nombre_archivo}")
        
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = EvaluadorGraficoApp(root)
    root.mainloop()
