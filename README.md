# GluA2-AMPA-Simulacion

**Proyecto Final — Electrofisiología Molecular I**  
*Modelado computacional del impacto de la edición Q/R del receptor AMPA-GluA2 sobre la integración dendrítica y la excitotoxicidad en una neurona piramidal de la amígdala humana*

Universidad de Guadalajara · CUTLAJO · 6.° semestre

---

## Descripción

Este repositorio contiene las simulaciones electrofisiológicas del receptor AMPA-GluA2 en dos condiciones:

- **Modo R (editado, fisiológico):** residuo 607 = Arginina → no permeable a Ca²⁺
- **Modo Q (no editado, patológico):** residuo 607 = Glutamina → permeable a Ca²⁺

El contexto biológico es la neurona piramidal del núcleo amigdaloide central, relevante en trastornos de ansiedad y TEPT.

---

## Estructura del repositorio

| Rama | Equipo | Contenido |
|------|--------|-----------|
| `main` | Todos | Parámetros compartidos, documentación general |
| `equipo-1-nernst-ghk` | Equipo 1 | Potenciales de Nernst y GHK, curva I-V |
| `equipo-2-circuito-rc` | Equipo 2 | Circuito RC de membrana, EPSPs |
| `equipo-3-neuron` | Equipo 3 | Simulación en NEURON con morfología real .swc |

---

## Parámetros compartidos

Ver archivo [`shared/parametros_compartidos.py`](shared/parametros_compartidos.py).

Todos los equipos **deben usar exactamente los mismos valores**. Si alguno necesita cambiar un parámetro, debe avisar a los demás antes.

| Parámetro | Modo R | Modo Q |
|-----------|--------|--------|
| Temperatura | 37 °C | 37 °C |
| [Na⁺]o / [Na⁺]i (mM) | 145 / 12 | 145 / 12 |
| [K⁺]o / [K⁺]i (mM) | 4 / 140 | 4 / 140 |
| [Ca²⁺]o / [Ca²⁺]i (mM) | 1.8 / 0.0001 | 1.8 / 0.0001 |
| P_Ca / P_Na (relativa) | **0.05** | **1.0** |
| Conductancia unitaria | ≈10 pS | ≈10 pS |
| τ subida / bajada AMPAR | 0.5 / 3.0 ms | 0.5 / 3.0 ms |
| R_a (resistividad axial) | 150 Ω·cm | 150 Ω·cm |
| C_m (capacitancia) | 1 µF/cm² | 1 µF/cm² |
| R_m (resistencia membrana) | 30 kΩ·cm² | 30 kΩ·cm² |
| V_reposo | −70 mV | −70 mV |

---

## Cronograma

| Semana | Equipo 1 | Equipo 2 | Equipo 3 |
|--------|----------|----------|----------|
| **1** | Nernst + GHK → entregar V_rev | RC con valores genéricos | Instalar NEURON, descargar .swc |
| **2** | Curva I-V, Tabla 1, párrafo metodología | EPSP único + tren, Figura 3 + Tabla 2 | Morfología real, primera corrida |
| **3** | Apoyo en Discusión | Validación cruzada con Equipo 3 | Figura final + Tabla 3 + Resultados |

---

## Dependencias entre equipos

```
Equipo 1 → V_rev_R, V_rev_Q → Equipos 2 y 3
Equipo 2 → amplitud y τ del EPSP → Equipo 3 (validación)
Equipo 3 → Integración final
```

---

## Cómo contribuir

1. Haz `git checkout` a tu rama correspondiente
2. Trabaja solo en tu carpeta (`equipo-1/`, `equipo-2/` o `equipo-3/`)
3. Haz commits descriptivos: `git commit -m "E1: agrega cálculo V_rev modo R"`
4. Cuando tengas un resultado listo para compartir, avisa por el grupo

---

## Referencias clave

- Burnashev et al. (1992). *Science*, 257, 1415–1419.
- Sommer et al. (1991). *Cell*, 67, 11–19.
- NeuroMorpho.org — morfología S1-8-pyramidal

---

*Proyecto académico — UdeG · CUTlajo· 2026*
