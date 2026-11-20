# ¿Tiene $N$ un factor en este intervalo?
**Búsqueda vs. verificación · números en binario**  
*USFQ | Universidad San Francisco de Quito | Teoría de la Computación*

---

## 1. Solicitud operativa

> **¿Existe un divisor $d$ de $N$ con $1 < d \le B$?** Usar datos de prueba; $N = 91$, $B = 10$.

---

## 2. Dos tareas distintas

| BUSCAR | VERIFICAR |
| :--- | :--- |
| • Probar candidatos $d = 2, 3, \dots, B$ hasta que $N \bmod d = 0$.<br>• **Para $N = 91$, el primer factor encontrado es $7$.** | • Dado $d = 7$, comprobar: $1 < d \le 10$ y $91 \bmod 7 = 0$.<br>• **Resultado: válido.** |

---

## 3. Código Python

```python
def buscar_divisor(N, B):
    for d in range(2, B + 1):
        if N % d == 0:
            return d
    return None

def verificar_divisor(N, B, d):
    return 1 < d <= B and N % d == 0

N, B = 91, 10
d = buscar_divisor(N, B)
print(d, verificar_divisor(N, B, d))  # 7 True
```

---

## 4. Resultado

```text
7 True
```

> **Encontrado:** $7$ divide a $91$ y está dentro del límite $B = 10$.

---

## 5. Costo / Big O

* **Búsqueda:** hasta $B - 1$ pruebas de divisibilidad. Con $N$ de $L$ bits, costo $O(B \cdot M(L))$; con división escolar $M(L) = O(L^2)$, así $O(BL^2)$.
* **Verificar un divisor dado:** una división y resto, $O(M(L)) = O(L^2)$ con división escolar.

> Como $B$ está codificado en binario, su longitud es $\log_2 B$; recorrer hasta $B$ puede ser exponencial en la longitud de la entrada. Verificar el testigo es polinomial en longitud de entrada.

---

**BFS/DFS no aplica: aquí se evalúan divisores, no se recorren vértices de un grafo.**