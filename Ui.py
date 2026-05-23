import tkinter as tk
from tkinter import ttk, messagebox
from Calculos import (
    suma_inferior, suma_superior, suma_riemann,
    integral_exacta, polinomio_str
)
from Graficador import Graficador


# ── Paleta de colores ──────────────────────────────────────────────────────────
BG        = "#1e1e2e"
BG2       = "#13131f"
PANEL     = "#252535"
ACCENT    = "#7c6af7"
ACCENT2   = "#ff6b9d"
FG        = "#e0e0f0"
FG2       = "#9999bb"
ENTRY_BG  = "#2a2a40"
BTN_BG    = "#4f46e5"
BTN_FG    = "#ffffff"
SUCCESS   = "#5dbe6e"
WARNING   = "#e07b39"
INFO      = "#4a90d9"
PURPLE    = "#9b59b6"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Integración Numérica — Sumas e Integrales")
        self.geometry("1280x760")
        self.resizable(True, True)
        self.configure(bg=BG)

        self._aplicar_estilos()
        self._construir_ui()

    # ── Estilos ttk ───────────────────────────────────────────────────────────
    def _aplicar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".",
            background=BG, foreground=FG,
            font=("Consolas", 10))

        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)

        style.configure("TLabel",
            background=BG, foreground=FG, font=("Consolas", 10))
        style.configure("Title.TLabel",
            background=BG, foreground=ACCENT2,
            font=("Consolas", 13, "bold"))
        style.configure("Sub.TLabel",
            background=PANEL, foreground=FG2,
            font=("Consolas", 9))
        style.configure("Panel.TLabel",
            background=PANEL, foreground=FG,
            font=("Consolas", 10))
        style.configure("Res.TLabel",
            background=BG2, foreground=FG,
            font=("Consolas", 10))

        style.configure("TLabelframe",
            background=PANEL, foreground=ACCENT,
            font=("Consolas", 10, "bold"),
            bordercolor=ACCENT, relief="flat")
        style.configure("TLabelframe.Label",
            background=PANEL, foreground=ACCENT,
            font=("Consolas", 10, "bold"))

        style.configure("TCombobox",
            fieldbackground=ENTRY_BG, background=ENTRY_BG,
            foreground=FG, selectbackground=ACCENT,
            font=("Consolas", 10))
        style.map("TCombobox",
            fieldbackground=[("readonly", ENTRY_BG)],
            foreground=[("readonly", FG)])

        style.configure("TEntry",
            fieldbackground=ENTRY_BG, foreground=FG,
            insertcolor=ACCENT2, font=("Consolas", 10))

        style.configure("Exec.TButton",
            background=BTN_BG, foreground=BTN_FG,
            font=("Consolas", 11, "bold"),
            padding=(12, 8), relief="flat")
        style.map("Exec.TButton",
            background=[("active", ACCENT)])

        style.configure("Clear.TButton",
            background="#333355", foreground=FG2,
            font=("Consolas", 9), padding=(8, 4), relief="flat")
        style.map("Clear.TButton",
            background=[("active", "#444466")])

        style.configure("TSeparator", background="#333355")

    # ── Layout principal ───────────────────────────────────────────────────────
    def _construir_ui(self):
        # Título superior
        header = tk.Frame(self, bg=BG, height=50)
        header.pack(fill="x", padx=0, pady=0)
        tk.Label(header, text="∫  INTEGRACIÓN NUMÉRICA",
                 bg=BG, fg=ACCENT2,
                 font=("Consolas", 16, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(header, text="Sumas Inferior · Superior · Riemann · Integral Exacta",
                 bg=BG, fg=FG2,
                 font=("Consolas", 9)).pack(side="left", padx=5, pady=10)

        tk.Frame(self, bg="#333355", height=1).pack(fill="x")

        # Contenedor principal
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=0, pady=0)

        # Panel izquierdo (controles)
        self.panel_izq = tk.Frame(main, bg=PANEL, width=270)
        self.panel_izq.pack(side="left", fill="y", padx=0, pady=0)
        self.panel_izq.pack_propagate(False)
        self._crear_controles(self.panel_izq)

        tk.Frame(main, bg="#333355", width=1).pack(side="left", fill="y")

        # Panel derecho (gráfica)
        panel_der = tk.Frame(main, bg=BG2)
        panel_der.pack(side="left", fill="both", expand=True)
        self.graficador = Graficador(panel_der)

    # ── Panel de controles ─────────────────────────────────────────────────────
    def _crear_controles(self, parent):
        pad = {"padx": 16, "pady": 4}

        # — Sección: Polinomio —
        tk.Label(parent, text="POLINOMIO", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=16, pady=(16, 2))
        tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=16)

        tk.Label(parent, text="Grado del polinomio:",
                 bg=PANEL, fg=FG2, font=("Consolas", 9)).pack(anchor="w", **pad)
        self.grado_var = tk.IntVar(value=2)
        cb = ttk.Combobox(parent, values=[1, 2, 3],
                          textvariable=self.grado_var,
                          state="readonly", width=8)
        cb.pack(anchor="w", padx=16, pady=2)
        cb.bind("<<ComboboxSelected>>", self._actualizar_coeficientes)

        # Vista previa del polinomio (debe crearse ANTES de _actualizar_coeficientes)
        self.preview_var = tk.StringVar(value="f(x) = x²")

        # Frame dinámico para coeficientes
        self.frame_coefs = tk.Frame(parent, bg=PANEL)
        self.frame_coefs.pack(fill="x", padx=16, pady=(4, 0))
        self.entradas_coefs = []
        self._actualizar_coeficientes()
        tk.Label(parent, textvariable=self.preview_var,
                 bg=PANEL, fg=ACCENT2,
                 font=("Consolas", 9, "italic"),
                 wraplength=230).pack(anchor="w", padx=16, pady=(4, 8))

        # — Sección: Parámetros —
        tk.Label(parent, text="PARÁMETROS", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=16, pady=(8, 2))
        tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=16)

        campos = [
            ("Número de rectángulos (n):", "n_var",  "10"),
            ("Límite inferior  a:",         "a_var",  "0"),
            ("Límite superior  b:",         "b_var",  "1"),
        ]
        for label, var_name, default in campos:
            tk.Label(parent, text=label, bg=PANEL, fg=FG2,
                     font=("Consolas", 9)).pack(anchor="w", **pad)
            var = tk.StringVar(value=default)
            setattr(self, var_name, var)
            e = tk.Entry(parent, textvariable=var, width=14,
                         bg=ENTRY_BG, fg=FG, insertbackground=ACCENT2,
                         relief="flat", font=("Consolas", 10))
            e.pack(anchor="w", padx=16, pady=2)

        # — Botones —
        tk.Frame(parent, bg=PANEL, height=12).pack()
        ttk.Button(parent, text="▶  EJECUTAR",
                   style="Exec.TButton",
                   command=self._ejecutar).pack(fill="x", padx=16, pady=4)
        ttk.Button(parent, text="✕  LIMPIAR",
                   style="Clear.TButton",
                   command=self._limpiar).pack(fill="x", padx=16, pady=2)

        # — Resultados —
        tk.Label(parent, text="RESULTADOS", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=16, pady=(14, 2))
        tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=16)

        self.frame_resultados = tk.Frame(parent, bg=BG2)
        self.frame_resultados.pack(fill="x", padx=16, pady=8)

        colores_res = [
            ("Suma Inferior:",  INFO),
            ("Suma Superior:",  WARNING),
            ("Suma Riemann:",   SUCCESS),
            ("Integral Exacta:", PURPLE),
        ]
        self.labels_res = {}
        for nombre, color in colores_res:
            fila = tk.Frame(self.frame_resultados, bg=BG2)
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text=nombre, bg=BG2, fg=color,
                     font=("Consolas", 9, "bold"), width=16, anchor="w").pack(side="left")
            var = tk.StringVar(value="—")
            tk.Label(fila, textvariable=var, bg=BG2, fg=FG,
                     font=("Consolas", 10), anchor="w").pack(side="left")
            self.labels_res[nombre] = var

    # ── Coeficientes dinámicos ─────────────────────────────────────────────────
    def _actualizar_coeficientes(self, event=None):
        for w in self.frame_coefs.winfo_children():
            w.destroy()
        self.entradas_coefs = []

        grado = self.grado_var.get()
        letras = ['a', 'b', 'c', 'd']

        for i in range(grado + 1):
            exp = grado - i
            if exp == 0:
                label = f"{letras[i]}  (constante)"
            elif exp == 1:
                label = f"{letras[i]}  (coef. de x)"
            else:
                sups = {2: '²', 3: '³'}
                label = f"{letras[i]}  (coef. de x{sups[exp]})"

            fila = tk.Frame(self.frame_coefs, bg=PANEL)
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text=label, bg=PANEL, fg=FG2,
                     font=("Consolas", 9), width=18, anchor="w").pack(side="left")
            var = tk.StringVar(value="1")
            e = tk.Entry(fila, textvariable=var, width=8,
                         bg=ENTRY_BG, fg=FG, insertbackground=ACCENT2,
                         relief="flat", font=("Consolas", 10))
            e.pack(side="left", padx=4)
            var.trace_add("write", lambda *_: self._actualizar_preview())
            self.entradas_coefs.append(var)

        self._actualizar_preview()

    def _actualizar_preview(self, *_):
        try:
            coefs = [float(v.get()) for v in self.entradas_coefs]
            from Calculos import polinomio_str
            self.preview_var.set(polinomio_str(coefs))
        except Exception:
            self.preview_var.set("f(x) = ?")

    # ── Ejecutar cálculos ──────────────────────────────────────────────────────
    def _ejecutar(self):
        try:
            coefs = [float(v.get()) for v in self.entradas_coefs]
            n = int(self.n_var.get())
            a = float(self.a_var.get())
            b = float(self.b_var.get())
        except ValueError:
            messagebox.showerror("Error de entrada",
                                 "Verifica que todos los campos tengan valores numéricos válidos.")
            return

        if n <= 0:
            messagebox.showerror("Error", "El número de rectángulos debe ser mayor a 0.")
            return
        if a >= b:
            messagebox.showerror("Error", "El límite 'a' debe ser menor que 'b'.")
            return

        val_inf, rects_inf = suma_inferior(coefs, a, b, n)
        val_sup, rects_sup = suma_superior(coefs, a, b, n)
        val_rie, rects_rie = suma_riemann(coefs, a, b, n)
        val_exa           = integral_exacta(coefs, a, b)

        resultados = {
            "inferior": (val_inf, rects_inf),
            "superior": (val_sup, rects_sup),
            "riemann":  (val_rie, rects_rie),
            "exacta":   val_exa,
        }

        self.labels_res["Suma Inferior:"].set(f"{val_inf:.6f}")
        self.labels_res["Suma Superior:"].set(f"{val_sup:.6f}")
        self.labels_res["Suma Riemann:"].set(f"{val_rie:.6f}")
        self.labels_res["Integral Exacta:"].set(f"{val_exa:.6f}")

        self.graficador.graficar_todo(coefs, a, b, n, resultados)

    # ── Limpiar ────────────────────────────────────────────────────────────────
    def _limpiar(self):
        for v in self.labels_res.values():
            v.set("—")
        self.graficador.limpiar()