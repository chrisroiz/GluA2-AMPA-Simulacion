# Modelado Computacional del Receptor AMPA-GluA2: Edición Q/R, Integración Dendrítica y Excitotoxicidad

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chrisroiz/GluA2-AMPA-Simulacion/blob/main/notebooks/GluA2_QR_Analisis_Completo.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NEURON](https://img.shields.io/badge/NEURON-8.x-green.svg)](https://neuron.yale.edu/)

> **Asignatura:** Electrofisiología Molecular I · Universidad de Guadalajara (CUCBA)  
> **Modelo neuronal:** Neurona piramidal S1-8, núcleo amigdaloide central humano ([NeuroMorpho.org](https://neuromorpho.org))  
> **Proteína:** GluA2 · UniProt [P42262](https://www.uniprot.org/uniprot/P42262) · PDB [4U2P](https://www.rcsb.org/structure/4U2P)

---

## Pregunta central

> ¿Cómo un **cambio de un solo aminoácido** (Q→R en la posición 607 de GluA2) altera la integración eléctrica de una neurona piramidal real y qué consecuencias tiene para los circuitos de miedo y enfermedad?

La enzima ADAR2 edita post-transcripcionalmente el codón 607 del ARNm de GluA2: reemplaza una **glutamina (Q)** — codificada en el ADN genómico — por una **arginina (R)** cargada positivamente. Este único cambio transforma la permeabilidad del canal al Ca²⁺ de forma dramática.

| Propiedad | Modo R (editado · fisiológico) | Modo Q (no editado · patológico) |
|-----------|-------------------------------|----------------------------------|
| Residuo 607 | Arginina (+) | Glutamina (neutro) |
| P_Ca / P_Na | 0.05 | 1.0 |
| Permeabilidad Ca²⁺ | Baja | **Alta** |
| Relación I-V | Lineal | Rectificadora entrante |
| Estado clínico | Normal (>99% editado) | TEPT · ALS · Alzheimer |

---

## Estructura del proyecto

```
GluA2-AMPA-Simulacion/
│
├── notebooks/
│   └── GluA2_QR_Analisis_Completo.ipynb   # Análisis completo (ejecutable en Colab)
│
├── data/
│   ├── Tabla1_potenciales.csv             # Potenciales Nernst y GHK (Etapa I)
│   ├── Tabla2_NEURON.csv                  # Métricas NEURON R vs Q (Etapa III)
│   ├── Tabla_resumen_completa.csv         # Comparación RC vs NEURON
│   └── trazas_NEURON.csv                  # Series temporales Vm(t) R y Q
│
├── docs/
│   └── Trabajo_Final.pdf                  # Manuscrito completo del proyecto
│
├── figures/                               # Figuras generadas por el notebook
│   └── [generadas al correr el notebook]
│
├── README.md
├── CITATION.cff
├── requirements.txt
└── .gitignore
```

---

## Metodología: tres etapas integradas

### Etapa I — Potenciales de equilibrio (Nernst / GHK)

Se calcularon los potenciales de Nernst individuales (Na⁺, K⁺, Ca²⁺) y el potencial de reversión por la ecuación de Goldman-Hodgkin-Katz para ambos modos:

$$V_{rev} = \frac{RT}{F} \ln \frac{P_{Na}[Na]_o + P_K[K]_o + 4P_{Ca}[Ca]_o}{P_{Na}[Na]_i + P_K[K]_i + 4P_{Ca}[Ca]_i}$$

**Resultado clave:** ΔV_rev = +1.2 mV (modo Q vs R). Aunque pequeño, este corrimiento se amplifica 40–60× por sumación temporal a 50 Hz en 15 sinapsis activas.

| Parámetro | Valor (mV) |
|-----------|-----------|
| E_Na | +66.55 |
| E_K | −94.96 |
| E_Ca | +130.85 |
| V_rev (modo R) | +7.96 |
| V_rev (modo Q) | +9.17 |
| **ΔV_rev** | **+1.21** |

---

### Etapa II — Modelo de circuito RC

La neurona se modeló como un compartimento único (modelo de punto), sirviendo como **límite superior teórico** de amplitud de EPSPs:

$$C_m \frac{dV}{dt} = -g_{pas}(V - E_{pas}) - g_{syn}(t)(V - E_{rev})$$

Con conductancia sináptica de doble exponencial (τ_rise = 0.5 ms, τ_decay = 3.0 ms), 15 sinapsis, tren de 10 pulsos a 50 Hz. Las amplitudes RC representan el caso sin atenuación dendrítica.

---

### Etapa III — Simulación con morfología real (NEURON)

La morfología S1-8 de NeuroMorpho.org se simuló en NEURON resolviendo la **ecuación del cable** en cientos de compartimentos:

$$C_m \frac{\partial V}{\partial t} = \frac{d}{4R_a} \frac{\partial^2 V}{\partial x^2} - g_{pas}(V - E_{pas}) - \sum_i I_{syn,i}$$

**Resultados principales:**

| Métrica | Modo R | Modo Q | Δ (Q−R) | Incremento |
|---------|--------|--------|---------|-----------|
| Baseline (mV) | −67.32 | −67.32 | 0.00 | 0% |
| **Amplitud EPSP (mV)** | **13.17** | **15.15** | **+1.98** | **+15%** |
| Integral mV·ms | 1782 | 1993 | +211 | +11.8% |
| Vm promedio tren (mV) | −59.12 | −58.08 | +1.04 | +1.8% |

La atenuación dendrítica reduce las amplitudes ~50% respecto al modelo RC, confirmando el filtrado espacial de la morfología piramidal. La razón Q/R ≈ 1.15 es conservada entre modelos (validación cruzada).

---

## Resultados y figuras

El notebook genera automáticamente:

| Figura | Descripción |
|--------|-------------|
| **Figura 1** | Curvas I–V del receptor AMPA-GluA2, modo R vs Q |
| **Figura 2** | Trazas RC: tren de 10 EPSPs a 50 Hz y diferencia ΔVm |
| **Figura 3** | Morfología 3D de la neurona piramidal S1-8 |
| **Figura 4** | Trazas somáticas NEURON R vs Q y diferencia Q−R |

---

## Cómo ejecutar

### Opción A — Google Colab (recomendado, sin instalación)

1. Haz clic en el badge **Open in Colab** al inicio de este README
2. En Colab: **Entorno de ejecución → Ejecutar todo** (`Ctrl+F9`)
3. El notebook instala NEURON automáticamente (~2 min) y genera todas las figuras

### Opción B — Local

```bash
# Clonar el repositorio
git clone https://github.com/chrisroiz/GluA2-AMPA-Simulacion.git
cd GluA2-AMPA-Simulacion

# Instalar dependencias
pip install -r requirements.txt

# Abrir el notebook
jupyter notebook notebooks/GluA2_QR_Analisis_Completo.ipynb
```

> **Nota sobre morfología S1-8:** Si la descarga automática de NeuroMorpho.org falla (HTTP 404), el notebook genera automáticamente una morfología sintética de neurona piramidal con geometría equivalente. Los resultados son cualitativamente idénticos.

---

## Dependencias

| Paquete | Versión mínima | Uso |
|---------|---------------|-----|
| numpy | ≥1.21 | Cálculos numéricos |
| matplotlib | ≥3.4 | Visualización |
| scipy | ≥1.7 | ODE para modelo RC |
| pandas | ≥1.3 | Tablas de resultados |
| neuron | ≥8.0 | Simulación con morfología real |

---

## Relevancia clínica

La falla en la edición Q/R está documentada en múltiples patologías:

```
Falla ADAR2  →  GluA2(Q)  →  P_Ca/P_Na: 0.05→1.0  →  ΔV_rev: +1.2 mV
  →  Fuerza impulsora +1.5%  →  Sumación temporal × 40–60
  →  [Ca²⁺]_i > 1 µM (umbral excitotóxico)  →  Atrofia dendrítica
```

| Condición | Mecanismo GluA2 | Correlato clínico |
|-----------|----------------|-------------------|
| TEPT | Hiperexcitabilidad CeA → sobreconsolidación del miedo | Flashbacks, hiperreactividad |
| Ansiedad crónica | Umbral de disparo reducido | Respuesta exagerada a estímulos neutros |
| ELA / FTD | Déficit ADAR2 → GluA2(Q) | Degeneración motoneuronal |
| Alzheimer | Déficit ADAR2 → atrofia dendrítica | Pérdida volumen amigdalino en RM |

---

## Ramas del repositorio

Este repositorio preserva el historial de desarrollo completo para transparencia científica:

- **`main`** — versión final pulida y documentada (esta rama)
- Ramas anteriores — iteraciones, pruebas y versiones de trabajo de los equipos

---

## Citar este trabajo

```bibtex
@misc{rojas2026glua2,
  author       = {Rojas, Christofer and colaboradores},
  title        = {Modelado Computacional del Receptor AMPA-GluA2: Edición Q/R,
                  Integración Dendrítica y Excitotoxicidad en Neurona Piramidal Amigdalina},
  year         = {2026},
  publisher    = {GitHub},
  institution  = {Universidad de Guadalajara, CUCBA},
  url          = {https://github.com/chrisroiz/GluA2-AMPA-Simulacion},
  note         = {Electrofisiología Molecular I — Proyecto Final}
}
```

---

## Referencias

1. Hines, M. L., & Carnevale, N. T. (1997). The NEURON simulation environment. *Neural Computation*, 9(6), 1179–1209.
2. Ascoli, G. A., et al. (2007). NeuroMorpho.Org: a central resource for neuronal morphologies. *Journal of Neuroscience*, 27(35), 9247–9251.
3. Burnashev, N., et al. (1992). Divalent ion permeability of AMPA receptor channels is dominated by the edited form of a single subunit. *Neuron*, 8(1), 189–198.
4. Isaac, J. T. R., et al. (2007). The role of the GluR2 subunit in AMPA receptor function and synaptic plasticity. *Neuron*, 54(6), 859–871.
5. Wright, A., & Vissel, B. (2012). The essential role of AMPA receptor GluR2 subunit RNA editing in the normal and diseased brain. *Frontiers in Molecular Neuroscience*, 5, 34.
6. Goldman, D. E. (1943). Potential, impedance, and rectification in membranes. *Journal of General Physiology*, 27(1), 37–60.
7. Hodgkin, A. L., & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *Journal of Physiology*, 117(4), 500–544.

---

<div align="center">

**Universidad de Guadalajara · CUCBA**  
Electrofisiología Molecular I · 2026  

*"Un solo aminoácido. Miles de consecuencias."*

</div>
