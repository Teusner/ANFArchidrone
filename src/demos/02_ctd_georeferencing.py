#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_ctd_georeferencing.py
ANF ArchiDrone 2026 (Réseaux Drone&Cap' / 2RM)
Auteur : Quentin Brateau

Démonstration pédagogique : Synchronisation temporelle et géoréférencement
d'un transect de sonde CTD (Conductivity, Temperature, Depth) et Fluorimètre.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def run_ctd_processing(output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(123)

    # 1. Trajectoire de l'AUV : profil en dents de scie (yo-yo) le long d'un transect côtier
    # Distance totale : 2.5 km (2500 m), profondeur oscillant entre 2m et 35m
    total_time = 1800  # 30 minutes
    t_nav = np.linspace(0, total_time, 1800)  # 1 Hz pour la navigation
    
    speed = 1.4  # m/s
    distance_along_track = speed * t_nav  # de 0 à ~2500 m
    
    # Ondulation verticale (yo-yo) entre 2m et 35m
    z_depth = 18.5 - 16.5 * np.cos(2 * np.pi * t_nav / 300.0)

    # 2. Flux de données capteur CTD (enregistré à 8 Hz sur une horloge désynchronisée)
    # Simulation d'une dérive d'horloge de +1.2 seconde
    clock_skew = 1.2
    t_sensor = np.arange(0, total_time, 0.125) + clock_skew
    
    # Modèle physique de l'océan côtier :
    # - Thermocline marquée vers 15m de profondeur (22°C en surface -> 14°C au fond)
    # - Panache estuarien / bloom phytoplanctonique (Chlorophylle-a) concentré entre 8m et 18m
    # Interpolation de la profondeur à l'instant du capteur (après correction du biais d'horloge)
    sensor_depth = np.interp(t_sensor - clock_skew, t_nav, z_depth)
    sensor_dist = np.interp(t_sensor - clock_skew, t_nav, distance_along_track)

    # Profil de température avec bruit de mesure
    temp_profile = 14.0 + 8.0 / (1.0 + np.exp((sensor_depth - 15.0) / 3.0))
    temp_measured = temp_profile + np.random.normal(0, 0.05, len(sensor_depth))

    # Profil de Chlorophylle-a (mg/m3) : pic au niveau de la thermocline (Deep Chlorophyll Maximum - DCM)
    chla_profile = 0.5 + 4.5 * np.exp(-((sensor_depth - 14.0)**2) / (2 * 4.0**2))
    # Ajout d'une hétérogénéité spatiale le long du transect (panache à mi-parcours)
    plume_weight = 1.0 + 0.8 * np.exp(-((sensor_dist - 1300.0)**2) / (2 * 350.0**2))
    chla_measured = chla_profile * plume_weight + np.random.normal(0, 0.08, len(sensor_depth))
    chla_measured = np.clip(chla_measured, 0.1, None)

    # 3. Tracé des coupes 2D géoréférencées
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
    fig.patch.set_facecolor('#F8FAFC')

    # Coupe 1 : Température
    sc1 = ax1.scatter(sensor_dist, sensor_depth, c=temp_measured, cmap='Spectral_r', 
                      s=10, alpha=0.9, edgecolors='none')
    ax1.set_ylim(40, 0)  # Inverser l'axe pour la profondeur
    ax1.set_ylabel('Profondeur $z$ (mètres)', fontsize=11, fontweight='bold')
    ax1.set_title(r"Transect AUV Géoréférencé : Température de l'Eau ($^\circ$C) avec Thermocline", 
                  fontsize=12, fontweight='bold', pad=10)
    cbar1 = plt.colorbar(sc1, ax=ax1, pad=0.02)
    cbar1.set_label(r'Température ($^\circ$C)', fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.5)

    # Coupe 2 : Chlorophylle-a
    sc2 = ax2.scatter(sensor_dist, sensor_depth, c=chla_measured, cmap='YlGn', 
                      s=10, alpha=0.9, edgecolors='none')
    ax2.set_ylim(40, 0)
    ax2.set_ylabel('Profondeur $z$ (mètres)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Distance le long du transect (mètres)', fontsize=11, fontweight='bold')
    ax2.set_title('Mesure Fluorimètre : Concentration en Chlorophylle-a (mg/m$^3$) & Détection de Bloom', 
                  fontsize=12, fontweight='bold', pad=10)
    cbar2 = plt.colorbar(sc2, ax=ax2, pad=0.02)
    cbar2.set_label('Chlorophylle-a (mg/m$^3$)', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.5)

    plt.suptitle("ANF ArchiDrone 2026 - Chaîne Data Science : De la Navigation Sous-Marine au Modèle Océanographique", 
                 fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()

    out_file = os.path.join(output_dir, "ctd_transect_profile.png")
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f"[SUCCESS] Figure CTD générée avec succès : {out_file}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    run_ctd_processing(out)

