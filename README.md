# KirbyIntegrales
## Main
El arranque:
App() construye toda la ventana. mainloop() es un bucle infinito de Tkinter que mantiene la ventana viva, escuchando eventos (clics, teclas, etc.) hasta que el usuario la cierra.

## Calculos
El cerebro matemático:
Aquí vive toda la matemática. No sabe nada de interfaz, solo recibe números y devuelve números.

¿Cómo representa el polinomio?
Usa una lista de coeficientes, el mismo formato que NumPy llama polyval:
f(x) = 3x² + 2x + 1  →  coefs = [3, 2, 1]
f(x) = x³ - 5x + 4   →  coefs = [1, 0, -5, 4]
El índice 0 es siempre el coeficiente de mayor grado.

### Suma Inferior
Divide [a, b] en n subintervalos iguales de ancho dx. En cada uno evalúa 100 puntos de la función y toma el mínimo como altura del rectángulo. Multiplica altura × ancho y acumula. El resultado siempre subestima el área real (por eso se llama inferior).

def suma_inferior(coefs, a, b, n):
    dx = (b - a) / n
    for i in range(n):
        x_izq = a + i * dx
        x_der  = a + (i + 1) * dx
        xs = np.linspace(x_izq, x_der, 100)  # 100 puntos en el subintervalo
        h = min(f(xs))                         # altura = mínimo de f en ese tramo
        total += h * dx

### Suma Superior
Idéntica a la inferior pero toma el máximo de cada subintervalo como altura. Siempre sobreestima el área real.
La relación matemática garantizada es:

Suma Inferior  ≤  Integral Exacta  ≤  Suma Superior

### Suma de Riemann
No busca mínimo ni máximo, simplemente evalúa la función en el punto medio de cada subintervalo. Es mucho más precisa que las otras dos porque los errores positivos y negativos se cancelan entre sí. Con n grande converge rapidísimo a la integral exacta.

x_mid = x_izq + dx / 2          # punto medio del subintervalo
h = f(x_mid)                     # altura = f evaluada en el centro
total += h * dx

### Integral Exacta
def integral_exacta(coefs, a, b):
    # Integra analíticamente: ax^n → ax^(n+1)/(n+1)
    for cada coeficiente c con exponente exp:
        anti_coef = c / (exp + 1)
    
    return F(b) - F(a)   # Teorema Fundamental del Cálculo

No aproxima nada. Construye la antiderivada exacta término a término:

f(x)  = 3x² + 2x + 1
F(x)  = x³  + x² + x   (antiderivada)
∫₀¹ f = F(1) - F(0) = 3 - 0 = 3

Esto solo es posible porque el problema garantiza que los polinomios son de grado 1, 2 o 3 — tipos que tienen antiderivada analítica trivial.

### ¿Por qué devuelve también los rectángulos?
pythonreturn total, rectangulos   # rectangulos = [(x0, altura, ancho), ...]
Cada método de suma devuelve dos cosas: el valor numérico del área y la lista de rectángulos con su posición y altura. Esto se lo pasa al graficador para que sepa exactamente dónde dibujar cada barra.

## UI
La interfaz.

### Coeficientes dinámicos
Cuando cambias el grado en el Combobox, se dispara _actualizar_coeficientes():
pythoncb.bind("<<ComboboxSelected>>", self._actualizar_coeficientes)
Este método destruye todos los campos de coeficientes existentes y crea los nuevos según el grado elegido. Grado 1 → 2 campos, grado 2 → 3 campos, grado 3 → 4 campos.
Cada campo tiene un trace que llama a _actualizar_preview() cada vez que el usuario escribe algo, actualizando la vista previa en tiempo real.
El botón EJECUTAR
_ejecutar() hace 5 cosas en orden:
1. Lee y valida todos los inputs
2. Llama a suma_inferior()
3. Llama a suma_superior()
4. Llama a suma_riemann()
5. Llama a integral_exacta()
6. Actualiza los labels de resultados
7. Le pasa todo al graficador
Validaciones
Antes de calcular verifica:

Que todos los campos sean números válidos (try/except ValueError)
Que n > 0
Que a < b

Si algo falla, muestra un messagebox.showerror() y no continúa.

## Graficador
### ¿Cómo se embebe Matplotlib en Tkinter?

self.fig, self.axes = plt.subplots(2, 2)       # crea figura con 4 subgráficas
self.canvas = FigureCanvasTkAgg(self.fig, master=parent)  # la envuelve en un widget Tkinter
self.canvas.get_tk_widget().pack(...)          # la integra a la ventana

FigureCanvasTkAgg es el puente entre Matplotlib y Tkinter. Convierte la figura de Matplotlib en un widget que Tkinter puede mostrar.
### ¿Cómo dibuja los rectángulos?
pythonax.bar(x0, h, width=dx, align='edge', ...)
ax.bar() de Matplotlib dibuja barras. Los parámetros clave son:

x0 — dónde empieza la barra (borde izquierdo con align='edge')
h — la altura (puede ser negativa para funciones bajo el eje)
width=dx — el ancho exacto del subintervalo

Se llama una vez por cada rectángulo en un bucle, construyendo toda la suma visualmente.
Las 4 subgráficas
plt.subplots(2, 2) crea una grilla 2×2. self.axes.flat las itera en orden: superior-izquierda, superior-derecha, inferior-izquierda, inferior-derecha. Cada una recibe un método diferente y su propio color:
Azul   → Suma Inferior
Naranja → Suma Superior
Verde  → Suma Riemann
Morado → Integral Exacta (área rellena, sin rectángulos)
La integral exacta usa fill_between() en lugar de barras porque no tiene rectángulos, solo el área continua bajo la curva.

### Flujo completo de una ejecución
Usuario llena campos y presiona EJECUTAR
        │
        ▼
ui.py :: _ejecutar()
  ├─ Valida inputs
  ├─ Llama calculos.py :: suma_inferior()   → (0.285, [(x0,h,dx), ...])
  ├─ Llama calculos.py :: suma_superior()   → (0.385, [(x0,h,dx), ...])
  ├─ Llama calculos.py :: suma_riemann()    → (0.332, [(x0,h,dx), ...])
  ├─ Llama calculos.py :: integral_exacta() → 0.333
  ├─ Actualiza los 4 labels de resultados
  └─ Llama graficador.py :: graficar_todo()
              │
              ▼
        Para cada una de las 4 subgráficas:
          · ax.clear()  (borra la anterior)
          · ax.bar()    (dibuja cada rectángulo)
          · ax.plot()   (dibuja la curva roja encima)
          · ax.fill_between() (solo para integral exacta)
        canvas.draw()   (renderiza todo en pantalla)