import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Calculos import evaluar_polinomio, polinomio_str


COLORES = {
    "inferior": ("#4A90D9", "#1a5fa8"),
    "superior": ("#E07B39", "#a84e10"),
    "riemann":  ("#5DBE6E", "#2e7a3c"),
    "exacta":   ("#9B59B6", "#6c3483"),
}


class Graficador:
    def __init__(self, parent):
        plt.style.use("dark_background")
        self.fig, self.axes = plt.subplots(2, 2, figsize=(9, 7))
        self.fig.patch.set_facecolor("#1e1e2e")
        self.fig.subplots_adjust(hspace=0.45, wspace=0.35)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def graficar_todo(self, coefs, a, b, n, resultados):
        """
        resultados = {
            'inferior': (valor, rectangulos),
            'superior': (valor, rectangulos),
            'riemann':  (valor, rectangulos),
            'exacta':   valor,
        }
        """
        titulos = ["Suma Inferior", "Suma Superior", "Suma de Riemann", "Integral Exacta"]
        metodos = ["inferior", "superior", "riemann", "exacta"]

        x_plot = np.linspace(a - abs(b - a) * 0.3, b + abs(b - a) * 0.3, 500)
        y_plot = evaluar_polinomio(coefs, x_plot)
        poly_str = polinomio_str(coefs)

        for idx, (ax, titulo, metodo) in enumerate(zip(self.axes.flat, titulos, metodos)):
            ax.clear()
            ax.set_facecolor("#13131f")

            color_fill, color_edge = COLORES[metodo]

            if metodo != "exacta":
                valor, rectangulos = resultados[metodo]
                for (x0, h, dx) in rectangulos:
                    ax.bar(
                        x0, h, width=dx, align="edge",
                        color=color_fill, alpha=0.55,
                        edgecolor=color_edge, linewidth=0.7
                    )
                ax.set_title(
                    f"{titulo}  |  n={n}\nÁrea ≈ {valor:.6f}",
                    fontsize=9, color="white", pad=6
                )
            else:
                valor = resultados["exacta"]
                x_fill = np.linspace(a, b, 500)
                y_fill = evaluar_polinomio(coefs, x_fill)
                ax.fill_between(x_fill, y_fill, alpha=0.45, color=color_fill)
                ax.set_title(
                    f"{titulo}\nÁrea = {valor:.6f}",
                    fontsize=9, color="white", pad=6
                )

            ax.plot(x_plot, y_plot, color="#ff6b9d", linewidth=2, label=poly_str)
            ax.axhline(0, color="#555577", linewidth=0.8)
            ax.axvline(a, color="#aaaacc", linewidth=0.8, linestyle="--", alpha=0.6)
            ax.axvline(b, color="#aaaacc", linewidth=0.8, linestyle="--", alpha=0.6)

            ax.set_xlim(x_plot[0], x_plot[-1])
            ax.tick_params(colors="#aaaacc", labelsize=7)
            for spine in ax.spines.values():
                spine.set_edgecolor("#333355")

            patch = mpatches.Patch(color="#ff6b9d", label=poly_str)
            ax.legend(handles=[patch], fontsize=7, loc="upper left",
                      facecolor="#1e1e2e", edgecolor="#555577", labelcolor="white")

        self.fig.suptitle(
            f"[a={a}, b={b}]  —  {poly_str}",
            fontsize=10, color="#ccccff", y=1.01
        )
        self.canvas.draw()

    def limpiar(self):
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor("#13131f")
        self.canvas.draw()