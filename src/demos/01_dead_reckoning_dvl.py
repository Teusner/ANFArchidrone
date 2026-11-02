#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_dead_reckoning_dvl.py
ANF ArchiDrone 2026 (Réseaux Drone&Cap' / 2RM)
Auteur : Quentin Brateau

Démonstration pédagogique : Pourquoi l'IMU seule échoue sous l'eau
et comment le DVL (Doppler Velocity Log) et l'USBL permettent de naviguer.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)

    # 1. Trajectoire de référence (AUV réalisant un fauchage en créneaux de 600m)
    duration = 600  # 10 minutes (600 secondes)
    dt = 0.5        # 2 Hz
    t = np.arange(0, duration, dt)
    n_steps = len(t)

    # Vitesse nominale : 1.5 m/s
    nominal_speed = 1.5
    current_velocity = np.array([0.15, -0.05])  # Courant marin de travers (m/s)

    # Trajectoire en créneaux (lawnmower survey)
    gt_x = np.zeros(n_steps)
    gt_y = np.zeros(n_steps)
    vx = np.zeros(n_steps)
    vy = np.zeros(n_steps)

    leg_duration = 100.0  # 100s par branche
    for i in range(1, n_steps):
        leg = int(t[i] / leg_duration)
        if leg % 2 == 0:
            vx_cmd = nominal_speed if (leg % 4 == 0) else -nominal_speed
            vy_cmd = 0.0
        else:
            vx_cmd = 0.0
            vy_cmd = nominal_speed

        vx[i] = vx_cmd
        vy[i] = vy_cmd
        gt_x[i] = gt_x[i-1] + vx[i] * dt
        gt_y[i] = gt_y[i-1] + vy[i] * dt

    # 2. Simulation IMU seule (Double intégration de l'accélération avec biais MEMS typique)
    # Biais d'accélération : 0.02 m/s^2 (très raisonnable pour un capteur MEMS !)
    acc_bias = np.array([0.02, -0.015])
    acc_noise_std = 0.05
    imu_x = np.zeros(n_steps)
    imu_y = np.zeros(n_steps)
    imu_vx = 0.0
    imu_vy = 0.0

    # 3. Simulation DVL + Gyro (Intégration de vitesse fond mesurée avec bruit ~0.5%)
    dvl_x = np.zeros(n_steps)
    dvl_y = np.zeros(n_steps)
    dvl_noise_std = 0.02

    # 4. Simulation USBL (Position absolue périodique reçue toutes les 30s avec bruit ~2m)
    usbl_period = 30.0
    usbl_times = []
    usbl_x = []
    usbl_y = []

    # 5. Filtre complémentaire / Kalman simplifié fusionnant DVL et USBL
    fused_x = np.zeros(n_steps)
    fused_y = np.zeros(n_steps)

    for i in range(1, n_steps):
        # Dérive IMU
        true_ax = (vx[i] - vx[i-1]) / dt
        true_ay = (vy[i] - vy[i-1]) / dt
        meas_ax = true_ax + acc_bias[0] + np.random.normal(0, acc_noise_std)
        meas_ay = true_ay + acc_bias[1] + np.random.normal(0, acc_noise_std)
        imu_vx += meas_ax * dt
        imu_vy += meas_ay * dt
        imu_x[i] = imu_x[i-1] + imu_vx * dt
        imu_y[i] = imu_y[i-1] + imu_vy * dt

        # DVL
        meas_vx = vx[i] + np.random.normal(0, dvl_noise_std)
        meas_vy = vy[i] + np.random.normal(0, dvl_noise_std)
        dvl_x[i] = dvl_x[i-1] + meas_vx * dt
        dvl_y[i] = dvl_y[i-1] + meas_vy * dt

        # Prédiction fusion
        fused_x[i] = fused_x[i-1] + meas_vx * dt
        fused_y[i] = fused_y[i-1] + meas_vy * dt

        # USBL Update
        if t[i] % usbl_period < dt:
            u_x = gt_x[i] + np.random.normal(0, 2.5)
            u_y = gt_y[i] + np.random.normal(0, 2.5)
            usbl_times.append(t[i])
            usbl_x.append(u_x)
            usbl_y.append(u_y)
            # Correction Kalman (gain K ~ 0.3)
            fused_x[i] += 0.3 * (u_x - fused_x[i])
            fused_y[i] += 0.3 * (u_y - fused_y[i])

    # Tracé des résultats
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1.3, 1]})
    fig.patch.set_facecolor('#F8FAFC')

    # Trajectoire spatiale 2D
    ax1.plot(gt_x, gt_y, 'k--', linewidth=2, label='Trajectoire Réelle (Vérité Terrain)')
    ax1.plot(dvl_x, dvl_y, color='#00A8B5', linewidth=1.8, label='Estime DVL + Cap (dérive linéaire ~0.5%)')
    ax1.plot(fused_x, fused_y, color='#10B981', linewidth=2, label='Fusion DVL + Fixes USBL (Kalman)')
    ax1.scatter(usbl_x, usbl_y, color='#E11D48', s=25, alpha=0.7, label='Pings acoustiques USBL surface (T=30s)')
    ax1.set_title('Trajectoire AUV : Impact des Capteurs de Navigation', fontsize=13, fontweight='bold', pad=12)
    ax1.set_xlabel('Position Est X (m)', fontsize=11)
    ax1.set_ylabel('Position Nord Y (m)', fontsize=11)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower right', framealpha=0.9)

    # Erreur en distance au cours du temps (échelle logarithmique)
    err_imu = np.sqrt((imu_x - gt_x)**2 + (imu_y - gt_y)**2)
    err_dvl = np.sqrt((dvl_x - gt_x)**2 + (dvl_y - gt_y)**2)
    err_fused = np.sqrt((fused_x - gt_x)**2 + (fused_y - gt_y)**2)

    ax2.plot(t, err_imu, color='#EF4444', linewidth=2, label='IMU seule (dérive quadratique $t^2$)')
    ax2.plot(t, err_dvl, color='#00A8B5', linewidth=1.8, label='DVL seul (dérive linéaire $t$)')
    ax2.plot(t, err_fused, color='#10B981', linewidth=2, label='Fusion DVL + USBL (erreur bornée)')
    ax2.set_yscale('log')
    ax2.set_title("Évolution de l'Erreur de Position dans le Temps", fontsize=13, fontweight='bold', pad=12)
    ax2.set_xlabel('Temps écoulé (secondes)', fontsize=11)
    ax2.set_ylabel('Erreur de position (mètres, échelle log)', fontsize=11)
    ax2.grid(True, which="both", linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', framealpha=0.9)

    # Annotation sur l'IMU
    ax2.annotate(f'Erreur IMU > {int(err_imu[-1])} m\nen seulement 10 min !', 
                 xy=(t[-1], err_imu[-1]), xytext=(t[-1]-220, err_imu[-1]*0.1),
                 arrowprops=dict(facecolor='#EF4444', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color='#B91C1C',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#FEE2E2", ec="#EF4444", lw=1))

    plt.suptitle("ANF ArchiDrone 2026 - Drone&Cap' / 2RM - Pourquoi l'acoustique et le DVL sont vitaux", 
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    out_file = os.path.join(output_dir, "dvl_drift_comparison.png")
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f"[SUCCESS] Figure générée avec succès : {out_file}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    run_simulation(out)

