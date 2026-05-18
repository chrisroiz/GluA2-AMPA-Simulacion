# Equipo 1 — Potenciales de equilibrio (Nernst) y GHK

## Objetivo

Calcular los potenciales de equilibrio iónicos (Nernst) y el potencial de inversión del receptor AMPA-GluA2 (GHK) en los modos R y Q. Generar la curva I-V comparativa.

## Entregables

- [ ] `equipo1_nernst_ghk.ipynb` — notebook comentado
- [ ] `figura2_curva_IV.png` — curva I-V R vs Q (300 dpi)
- [ ] `tabla1_potenciales.csv` — E_Na, E_K, E_Ca, V_rev_R, V_rev_Q, ΔV_rev
- [ ] Párrafo de Metodología (~150 palabras)

## Output crítico para los demás equipos

> **V_rev_R** y **V_rev_Q** — compartir tan pronto estén listos (primeros 3 días).

## Ecuaciones

```
Nernst (37°C):   E_ion = (61.5 / z) * log10([ion]_o / [ion]_i)

GHK V_rev:  V_rev = (RT/F) * ln[(P_Na*[Na]o + P_K*[K]o + 4*P_Ca*[Ca]o) /
                                 (P_Na*[Na]i + P_K*[K]i + 4*P_Ca*[Ca]i)]

Corriente:  I = g * (V_m - V_rev)
```

## Pasos

1. Calcular E_Na, E_K, E_Ca → verificar vs. valores esperados
2. Implementar GHK como función Python (argumento: P_Ca/P_Na)
3. Calcular V_rev para modo R y modo Q → reportar ΔV_rev
4. Curva I-V: V_m de −100 a +60 mV, paso 5 mV, ambos modos
5. Tabla final lista para el manuscrito

## Herramientas

```bash
pip install numpy matplotlib jupyter
```
