# Equipo 3 — Acoplamiento con la neurona en NEURON

## Objetivo

Importar la morfología real (.swc) de la neurona piramidal amigdalina S1-8, configurar propiedades pasivas y activas, distribuir sinapsis AMPAR y simular la respuesta integrada en el soma. Comparar modos R y Q.

## Dependencias

> - **V_rev_R** y **V_rev_Q** del Equipo 1 → actualizar en el script
> - **Amplitud y τ del EPSP** del Equipo 2 → usar como punto de validación

## Entregables

- [ ] `glua2_amigdala_simulacion.py` — script de simulación NEURON
- [ ] `S1-8-pyramidal.swc` — morfología descargada de NeuroMorpho.org
- [ ] `figura1_morfologia.png` — morfología 3D con sinapsis marcadas
- [ ] `figura4_trazas_somaticas.png` — trazas somáticas R vs Q
- [ ] `tabla3_resultados.csv` — amplitud somática, integral EPSP, atenuación
- [ ] Párrafo de Metodología (~200 palabras)

## Pasos

1. `pip install neuron`
2. `python glua2_amigdala_simulacion.py --modo_prueba` (validar instalación)
3. Descargar S1-8-pyramidal.swc de [neuromorpho.org](https://neuromorpho.org)
4. `python glua2_amigdala_simulacion.py --swc S1-8-pyramidal.swc`
5. Reemplazar `E_REV_R` y `E_REV_Q` con valores del Equipo 1
6. Verificar: amplitud somática < amplitud RC del Equipo 2 (filtrado dendrítico)

## Validación cruzada

El EPSP somático en NEURON debe ser **menor** que el del Equipo 2 (circuito RC), porque el filtrado dendrítico atenúa la señal. La constante de tiempo τ debe ser **mayor**. Si no es así, revisar parámetros.

## Herramientas

```bash
pip install neuron numpy matplotlib
```

Ver [NEURON documentation](https://www.neuron.yale.edu/neuron/)
