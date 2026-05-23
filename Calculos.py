import numpy as np


def evaluar_polinomio(coefs, x):
    """Evalúa el polinomio con np.polyval (coefs = [a, b, c, d] para grado 3)."""
    return np.polyval(coefs, x)


def suma_inferior(coefs, a, b, n):
    """Suma de Darboux inferior: usa el mínimo de f(x) en cada subintervalo."""
    dx = (b - a) / n
    total = 0.0
    rectangulos = []
    for i in range(n):
        x_izq = a + i * dx
        x_der = a + (i + 1) * dx
        xs = np.linspace(x_izq, x_der, 100)
        ys = evaluar_polinomio(coefs, xs)
        h = float(np.min(ys))
        total += h * dx
        rectangulos.append((x_izq, h, dx))
    return total, rectangulos


def suma_superior(coefs, a, b, n):
    """Suma de Darboux superior: usa el máximo de f(x) en cada subintervalo."""
    dx = (b - a) / n
    total = 0.0
    rectangulos = []
    for i in range(n):
        x_izq = a + i * dx
        x_der = a + (i + 1) * dx
        xs = np.linspace(x_izq, x_der, 100)
        ys = evaluar_polinomio(coefs, xs)
        h = float(np.max(ys))
        total += h * dx
        rectangulos.append((x_izq, h, dx))
    return total, rectangulos


def suma_riemann(coefs, a, b, n):
    """Suma de Riemann: usa el punto medio de cada subintervalo."""
    dx = (b - a) / n
    total = 0.0
    rectangulos = []
    for i in range(n):
        x_izq = a + i * dx
        x_mid = x_izq + dx / 2
        h = float(evaluar_polinomio(coefs, x_mid))
        total += h * dx
        rectangulos.append((x_izq, h, dx))
    return total, rectangulos


def integral_exacta(coefs, a, b):
    """
    Calcula la integral definida exacta integrando analíticamente el polinomio.
    Antiderivada de a*x^n es a*x^(n+1)/(n+1).
    """
    grado = len(coefs) - 1
    anti_coefs = []
    for i, c in enumerate(coefs):
        exp = grado - i
        anti_coefs.append(c / (exp + 1))
    anti_coefs.append(0.0)  # constante de integración

    def F(x):
        return float(np.polyval(anti_coefs, x))

    return F(b) - F(a)


def polinomio_str(coefs):
    """Devuelve una representación legible del polinomio."""
    grado = len(coefs) - 1
    terminos = []
    letras_exp = ['³', '²', '¹', '⁰']
    offset = 4 - len(coefs)

    for i, c in enumerate(coefs):
        exp = grado - i
        if c == 0:
            continue
        c_str = f"{c:g}"
        if exp == 0:
            terminos.append(c_str)
        elif exp == 1:
            terminos.append(f"{c_str}x")
        else:
            terminos.append(f"{c_str}x{letras_exp[offset + i]}")

    if not terminos:
        return "f(x) = 0"
    return "f(x) = " + " + ".join(terminos).replace("+ -", "- ")