"""
parametros_compartidos.py
=========================
Parámetros biofísicos compartidos por todos los equipos.
NO modificar sin avisar al grupo.

Proyecto: Modelado GluA2 Q/R — Electrofisiología Molecular I
UdeG · CUCEI · 2026
"""

# ── Temperatura ──────────────────────────────────────────────────────────────
TEMP_CELSIUS = 37.0          # °C (fisiológica humana)
TEMP_KELVIN  = TEMP_CELSIUS + 273.15

# ── Constantes físicas ───────────────────────────────────────────────────────
R = 8.314    # J / (mol·K)   constante de gas ideal
F = 96485    # C / mol       constante de Faraday

# ── Concentraciones iónicas (mM) ─────────────────────────────────────────────
#    sufijo _o = extracelular | sufijo _i = intracelular
NA_O  = 145.0
NA_I  = 12.0

K_O   = 4.0
K_I   = 140.0

CA_O  = 1.8
CA_I  = 0.0001   # 100 nM en reposo

# ── Selectividad del receptor AMPA-GluA2 ─────────────────────────────────────
P_CA_P_NA_R = 0.05   # Modo R (editado, fisiológico)   — Burnashev 1992
P_CA_P_NA_Q = 1.0    # Modo Q (no editado, patológico) — Burnashev 1992

P_K_P_NA    = 1.0    # Misma para ambos modos (AMPAR)
P_NA_P_NA   = 1.0    # Referencia (= 1 por definición)

# ── Cinética sináptica AMPAR ──────────────────────────────────────────────────
TAU_RISE_MS  = 0.5   # ms — tiempo de subida
TAU_DECAY_MS = 3.0   # ms — tiempo de bajada
G_UNIT_PS    = 10.0  # pS — conductancia unitaria (igual en R y Q)

# ── Propiedades pasivas de membrana ──────────────────────────────────────────
RA_OHM_CM   = 150.0   # Ω·cm  — resistividad axial (neurona piramidal)
CM_UF_CM2   = 1.0     # µF/cm² — capacitancia de membrana
RM_KOHM_CM2 = 30.0    # kΩ·cm² — resistencia de membrana (neurona piramidal)

V_REPOSO_MV = -70.0   # mV — potencial de reposo

# ── Factor de Nernst a 37 °C ─────────────────────────────────────────────────
#    61.5 mV = (RT/F) * ln(10) * 1000  a 37 °C
NERNST_FACTOR_MV = (R * TEMP_KELVIN / F) * 2.3026 * 1000   # ≈ 61.5 mV

# ── Valores esperados (para verificación) ───────────────────────────────────
# E_Na  ≈ +67 mV
# E_K   ≈ −95 mV
# E_Ca  ≈ +130 mV

if __name__ == "__main__":
    import math
    print("=== Verificación de parámetros compartidos ===")
    print(f"Factor Nernst a {TEMP_CELSIUS}°C : {NERNST_FACTOR_MV:.2f} mV  (esperado ≈ 61.5 mV)")
    E_Na = NERNST_FACTOR_MV / 1 * math.log10(NA_O / NA_I)
    E_K  = NERNST_FACTOR_MV / 1 * math.log10(K_O  / K_I)
    E_Ca = NERNST_FACTOR_MV / 2 * math.log10(CA_O / CA_I)
    print(f"E_Na = {E_Na:.1f} mV  (esperado ≈ +67 mV)")
    print(f"E_K  = {E_K:.1f} mV  (esperado ≈ −95 mV)")
    print(f"E_Ca = {E_Ca:.1f} mV  (esperado ≈ +130 mV)")
