"""
glua2_amigdala_simulacion.py
============================
Simulación del receptor AMPA-GluA2 en la neurona piramidal amigdalina S1-8.
Compara Modo R (editado, fisiológico) vs Modo Q (no editado, patológico).

Uso:
    # Validar instalación de NEURON:
    python glua2_amigdala_simulacion.py --modo_prueba

    # Simulación con morfología real:
    python glua2_amigdala_simulacion.py --swc S1-8-pyramidal.swc

    # Cambiar modo:
    python glua2_amigdala_simulacion.py --swc S1-8-pyramidal.swc --modo R
    python glua2_amigdala_simulacion.py --swc S1-8-pyramidal.swc --modo Q

Proyecto: Modelado GluA2 Q/R — Electrofisiología Molecular I · UdeG CUCEI 2026
"""

import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

# ── Importar parámetros compartidos ──────────────────────────────────────────
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from parametros_compartidos import (
    CM_UF_CM2, RM_KOHM_CM2, RA_OHM_CM, V_REPOSO_MV,
    TAU_RISE_MS, TAU_DECAY_MS, G_UNIT_PS,
    P_CA_P_NA_R, P_CA_P_NA_Q
)

# ── Potenciales de reversión (actualizar con valores del Equipo 1) ────────────
E_REV_R = None   # ← reemplazar con V_rev_R del Equipo 1 (mV)
E_REV_Q = None   # ← reemplazar con V_rev_Q del Equipo 1 (mV)

# Valores provisionales hasta recibir del Equipo 1
if E_REV_R is None:
    print("AVISO: E_REV_R/Q son provisionales. Actualizar con valores del Equipo 1.")
    E_REV_R = 0.0
    E_REV_Q = 5.0

# ── Parámetros de simulación ──────────────────────────────────────────────────
N_SINAPSIS       = 15       # número de sinapsis AMPAR
G_MAX_NS         = 0.5      # nS por sinapsis
T_STOP_MS        = 200.0    # ms — duración de la simulación
DT_MS            = 0.025    # ms — paso de tiempo
T_STIM_MS        = 10.0     # ms — tiempo del primer estímulo


def modo_prueba():
    """Verifica que NEURON está instalado y funciona correctamente."""
    print("=== Modo prueba: verificando NEURON ===")
    try:
        from neuron import h
        h.load_file('stdrun.hoc')
        soma = h.Section(name='soma')
        soma.L = 20
        soma.diam = 20
        soma.insert('pas')
        soma.e_pas = V_REPOSO_MV
        soma.g_pas = 1.0 / (RM_KOHM_CM2 * 1e3)   # S/cm²
        soma.cm = CM_UF_CM2

        h.finitialize(V_REPOSO_MV)
        h.continuerun(10)
        print("NEURON instalado correctamente.")
        print(f"Versión: {h.version()}")
        return True
    except ImportError:
        print("ERROR: NEURON no está instalado.")
        print("Instalar con: pip install neuron")
        return False


def cargar_morfologia_swc(swc_path):
    """Importa morfología .swc en NEURON y configura propiedades biofísicas."""
    from neuron import h
    h.load_file('stdrun.hoc')
    h.load_file('import3d.hoc')

    cell = h.Import3d_SWC_read()
    cell.input(swc_path)
    i3d = h.Import3d_GUI(cell, False)
    i3d.instantiate(None)

    # Configurar propiedades pasivas en todas las secciones
    for sec in h.allsec():
        sec.Ra = RA_OHM_CM
        sec.cm = CM_UF_CM2
        sec.insert('pas')
        sec.e_pas = V_REPOSO_MV
        sec.g_pas = 1.0 / (RM_KOHM_CM2 * 1e3)   # S/cm²

    print(f"Morfología cargada: {swc_path}")
    print(f"Secciones totales: {h.topology()}")
    return h


def distribuir_sinapsis(h, n=N_SINAPSIS, e_rev=E_REV_R):
    """Distribuye n sinapsis AMPAR en dendritas basales."""
    sinapsis = []
    netstims  = []
    netcons   = []

    # Seleccionar secciones dendríticas
    dendrites = [sec for sec in h.allsec()
                 if 'dend' in sec.name() or 'basal' in sec.name()]

    if not dendrites:
        print("AVISO: No se encontraron secciones dendríticas con nombre 'dend'/'basal'.")
        print("Usando todas las secciones no-soma.")
        dendrites = [sec for sec in h.allsec() if 'soma' not in sec.name()]

    step = max(1, len(dendrites) // n)

    for i in range(n):
        sec = dendrites[(i * step) % len(dendrites)]
        syn = h.Exp2Syn(sec(0.5))
        syn.tau1 = TAU_RISE_MS
        syn.tau2 = TAU_DECAY_MS
        syn.e    = e_rev

        stim = h.NetStim()
        stim.number = 1
        stim.start  = T_STIM_MS
        stim.noise  = 0

        nc = h.NetCon(stim, syn)
        nc.weight[0] = G_MAX_NS * 1e-3   # µS

        sinapsis.append(syn)
        netstims.append(stim)
        netcons.append(nc)

    print(f"{n} sinapsis distribuidas en {len(dendrites)} dendritas.")
    return sinapsis, netstims, netcons


def correr_simulacion(h, modo='R'):
    """Ejecuta la simulación y regresa tiempo y voltaje somático."""
    e_rev = E_REV_R if modo == 'R' else E_REV_Q

    # Soma (primera sección de tipo soma)
    soma = next((s for s in h.allsec() if 'soma' in s.name()), None)
    if soma is None:
        soma = list(h.allsec())[0]

    # Distribuir sinapsis
    sinapsis, netstims, netcons = distribuir_sinapsis(h, e_rev=e_rev)

    # Vectores de registro
    t_vec = h.Vector().record(h._ref_t)
    v_vec = h.Vector().record(soma(0.5)._ref_v)

    # Correr
    h.dt = DT_MS
    h.tstop = T_STOP_MS
    h.v_init = V_REPOSO_MV
    h.finitialize(V_REPOSO_MV)
    h.continuerun(T_STOP_MS)

    t = np.array(t_vec)
    v = np.array(v_vec)
    return t, v, sinapsis


def analizar_epsp(t, v):
    """Calcula amplitud, tiempo al pico e integral del EPSP."""
    v_base = v[t < T_STIM_MS].mean()
    amp    = v.max() - v_base
    t_pico = t[np.argmax(v)]

    # τ de decaimiento: ajuste exponencial post-pico
    idx_pico = np.argmax(v)
    v_post   = v[idx_pico:]
    t_post   = t[idx_pico:] - t[idx_pico]
    if len(v_post) > 10 and amp > 0.01:
        try:
            from scipy.optimize import curve_fit
            def mono_exp(x, a, tau):
                return a * np.exp(-x / tau)
            popt, _ = curve_fit(mono_exp, t_post, v_post - v_base,
                                p0=[amp, 20.0], maxfev=5000)
            tau_decay = popt[1]
        except Exception:
            tau_decay = float('nan')
    else:
        tau_decay = float('nan')

    integral = np.trapz(v - v_base, t)

    return {
        'amplitud_mV':  round(amp, 4),
        'tiempo_pico_ms': round(t_pico, 2),
        'tau_decay_ms': round(tau_decay, 2) if not np.isnan(tau_decay) else 'N/A',
        'integral_mV_ms': round(integral, 4),
    }


def main():
    parser = argparse.ArgumentParser(description='Simulación GluA2-AMPA en NEURON')
    parser.add_argument('--modo_prueba', action='store_true',
                        help='Verifica instalación de NEURON')
    parser.add_argument('--swc', type=str, default=None,
                        help='Ruta al archivo .swc de morfología')
    parser.add_argument('--modo', choices=['R', 'Q', 'ambos'], default='ambos',
                        help='Modo de edición GluA2 (R, Q, o ambos)')
    args = parser.parse_args()

    if args.modo_prueba:
        modo_prueba()
        return

    if args.swc is None:
        print("ERROR: proporciona --swc <archivo.swc> o usa --modo_prueba")
        sys.exit(1)

    from neuron import h
    print(f"\n=== Simulación GluA2-AMPA — Morfología: {args.swc} ===\n")

    resultados = {}
    modos = ['R', 'Q'] if args.modo == 'ambos' else [args.modo]

    t_data, v_data = {}, {}
    for m in modos:
        h_inst = cargar_morfologia_swc(args.swc)
        print(f"\nCorriendo Modo {m}...")
        t, v, _ = correr_simulacion(h_inst, modo=m)
        t_data[m] = t
        v_data[m] = v
        resultados[m] = analizar_epsp(t, v)
        print(f"  → Amplitud: {resultados[m]['amplitud_mV']} mV")
        print(f"  → Tiempo al pico: {resultados[m]['tiempo_pico_ms']} ms")
        print(f"  → τ decaimiento: {resultados[m]['tau_decay_ms']} ms")

    # ── Figura trazas somáticas ──────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = {'R': 'steelblue', 'Q': 'tomato'}
    for m in modos:
        ax.plot(t_data[m], v_data[m], color=colors[m], lw=2,
                label=f'Modo {m}  (Δ={resultados[m]["amplitud_mV"]} mV)')
    ax.set_xlabel('Tiempo (ms)', fontsize=12)
    ax.set_ylabel('V soma (mV)', fontsize=12)
    ax.set_title('Trazas somáticas — GluA2 Modo R vs Q\nNeurona piramidal amigdalina S1-8', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figura4_trazas_somaticas.png', dpi=300, bbox_inches='tight')
    print('\nFigura guardada: figura4_trazas_somaticas.png')

    # ── Tabla resumen ────────────────────────────────────────────────────────
    import csv
    with open('tabla3_resultados.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Modo', 'Amplitud (mV)', 'Tiempo pico (ms)',
                         'tau decaimiento (ms)', 'Integral EPSP (mV·ms)'])
        for m, res in resultados.items():
            writer.writerow([m, res['amplitud_mV'], res['tiempo_pico_ms'],
                             res['tau_decay_ms'], res['integral_mV_ms']])
    print('Tabla guardada: tabla3_resultados.csv')
    plt.show()


if __name__ == '__main__':
    main()
