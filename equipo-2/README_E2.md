# Equipo 2 — Circuito RC de membrana

## Objetivo

Modelar la membrana de una dendrita como circuito RC en paralelo con corriente sináptica AMPAR. Simular el EPSP generado por un único evento glutamatérgico y un tren de estímulos bajo los dos modos.

## Dependencia

> Necesitas **V_rev_R** y **V_rev_Q** del Equipo 1 antes de la semana 2.  
> Actualiza las constantes en el notebook cuando las recibas.

## Entregables

- [ ] `equipo2_rc_membrana.ipynb` — notebook comentado
- [ ] `figura3_EPSP.png` — EPSP único y tren 50 Hz R vs Q (300 dpi)
- [ ] `tabla2_EPSP.csv` — amplitud, tiempo al pico, τ, integral
- [ ] Párrafo de Metodología (~150 palabras)

## Tu output para el Equipo 3

> **Amplitud máxima** y **τ de decaimiento** del EPSP teórico.  
> El Equipo 3 debe obtener valores del mismo orden en NEURON (aunque menores por filtrado dendrítico).

## Ecuaciones

```
EDO RC:    C_m * dV/dt = -g_pas*(V - E_pas) - g_syn(t)*(V - V_rev)

g_syn(t):  g_max * [exp(-t/τ_decay) - exp(-t/τ_rise)]

τ_m:       R_m * C_m
```

## Parámetros

| Variable | Valor |
|----------|-------|
| g_max | 0.5 nS × 15 sinapsis = 7.5 nS |
| τ subida | 0.5 ms |
| τ bajada | 3.0 ms |
| Tren | 10 estímulos a 50 Hz |

## Herramientas

```bash
pip install numpy scipy matplotlib jupyter
```
