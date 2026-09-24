import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
from scipy.optimize import curve_fit

# ==========================================
# DIOM-DLEQM: Hardware Constants & Data Loading
# ==========================================
E_P = 1.22e19  # Planck Energy (GeV) - Absolute grid resolution limit

# Simulated cleaned system logs from NASA HEASARC & MAST archives
grb_data_csv = """GRB_Name,delta_t_obs,delta_E_GeV,L_over_c_seconds
GRB_090510,0.829,31,2.30e17
GRB_221009A,158.6,18000,7.568e16
GRB_190114C,0.012,0.4,1.45e17
GRB_130427A,3.1,94,4.03e17
GRB_080916C,12.5,270,5.65e17
"""

# ==========================================
# Module 1: Verdict V (GRB Rendering Latency)
# ==========================================
print(">>> INITIATING DIOM VERDICT V: GRB LATENCY EXTRACTION...")
df_grb = pd.read_csv(io.StringIO(grb_data_csv))
df_grb['x_data'] = (df_grb['delta_E_GeV'] / E_P) * df_grb['L_over_c_seconds']
x_grb = df_grb['x_data'].values
y_grb = df_grb['delta_t_obs'].values

def diom_delay_model(delta_E_L_over_c, xi):
    # DSR Latency Law: delta_t = xi * (delta_E / E_p) * (L/c)
    return xi * delta_E_L_over_c

popt_grb, _ = curve_fit(diom_delay_model, x_grb, y_grb)
xi_fitted = popt_grb[0]
print(f"[SYSTEM LOG] Empirical Fitted Impedance Constant: xi = {xi_fitted:.4f}")

# ==========================================
# Module 2: Visual Rendering (The UI of Truth)
# ==========================================
plt.style.use('dark_background')
fig, ax1 = plt.subplots(figsize=(8, 6))

ax1.scatter(x_grb, y_grb, color='cyan', marker='x', s=80, label='Fermi/LHAASO Logs')
x_line1 = np.linspace(0, max(x_grb)*1.1, 100)
ax1.plot(x_line1, diom_delay_model(x_line1, xi_fitted), color='red', linewidth=2, label=f'DIOM Latency ($\\xi={xi_fitted:.4f}$)')
ax1.set_title("Verdict V: GRB Computational Latency", fontweight='bold')
ax1.set_xlabel("Impedance Factor: $(\Delta E / E_p) * (L/c)$")
ax1.set_ylabel("Observed Frame-Drop $\Delta t$ (s)")
ax1.grid(True, color='#333333', linestyle='--')
ax1.legend(frameon=False)

plt.tight_layout()
plt.show()
