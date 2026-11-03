# ==============================================================================
# Makefile - ANF ArchiDrone 2026 (Drone&Cap' / 2RM)
# Support de cours : Robotique Marine & Sous-Marine pour l'Acquisition Scientifique
# Auteur : Quentin Brateau
# ==============================================================================

SHELL           := /bin/bash

# Compilateurs et options
LATEXMK         ?= latexmk
PDFLATEX        ?= pdflatex
PYTHON          ?= python3

LATEXMK_FLAGS   ?= -cd -pdf -interaction=nonstopmode -halt-on-error
PDFLATEX_FLAGS  ?= -interaction=nonstopmode -halt-on-error

# Répertoires sources
SRC_DIR         := src
SLIDES_DIR      := $(SRC_DIR)/slides
HANDOUT_DIR     := $(SRC_DIR)/handouts
DEMOS_DIR       := $(SRC_DIR)/demos
IMGS_DIR        := imgs

# Fichiers sources et cibles intermédiaires
SLIDES_SRC      := $(SLIDES_DIR)/main.tex
SLIDES_ALL_SRC  := $(wildcard $(SLIDES_DIR)/*.tex)
SLIDES_PDF      := $(SLIDES_DIR)/main.pdf

HANDOUT_SRC     := $(HANDOUT_DIR)/fiche_memo_robotique_sous_marine.tex
HANDOUT_PDF     := $(HANDOUT_DIR)/fiche_memo_robotique_sous_marine.pdf

IMGS            := $(wildcard $(IMGS_DIR)/*) $(wildcard $(IMGS_DIR)/logos/*)

# Répertoires et cibles finales (conforme à la structure README.md)
BUILD_DIR       := build
BUILD_SLIDES    := $(BUILD_DIR)/slides/slides_robotique_sous_marine.pdf
BUILD_SYNTHESIS := $(BUILD_DIR)/synthesis/fiche_synthese_robotique_sous_marine.pdf
BUILD_DEMOS_DIR := $(BUILD_DIR)/demos

# Extensions de fichiers auxiliaires LaTeX à nettoyer
AUX_EXTS        := aux log out toc nav snm vrb fls fdb_latexmk synctex.gz bbl blg run.xml bcf

# ==============================================================================
# Cibles principales
# ==============================================================================

.DEFAULT_GOAL   := all

.PHONY: all presentation slides fiche synthese handout demos clean distclean fclean help watch-slides watch-handout

## all : Compile la présentation et la fiche de synthèse
all: presentation fiche

## presentation / slides : Compile les transparents Beamer (src/slides/main.tex)
presentation: $(BUILD_SLIDES)

slides: presentation

## fiche / synthese / handout : Compile la fiche mémo / synthèse (2 pages recto-verso)
fiche: $(BUILD_SYNTHESIS)

synthese: fiche

handout: fiche

# Alias pour compatibilité directe avec la demande "src/main.tex"
src/main.pdf: $(SLIDES_PDF)
	@mkdir -p $(@D)
	cp -f $< $@

# ==============================================================================
# Règles de compilation LaTeX
# ==============================================================================

$(SLIDES_PDF): $(SLIDES_ALL_SRC) $(IMGS)
	@echo "==> Compilation de la présentation Beamer ($(SLIDES_SRC))..."
	@if command -v $(LATEXMK) > /dev/null 2>&1; then \
		$(LATEXMK) $(LATEXMK_FLAGS) $(SLIDES_SRC); \
	else \
		cd $(SLIDES_DIR) && \
		$(PDFLATEX) $(PDFLATEX_FLAGS) $(notdir $(SLIDES_SRC)) && \
		$(PDFLATEX) $(PDFLATEX_FLAGS) $(notdir $(SLIDES_SRC)); \
	fi

$(BUILD_SLIDES): $(SLIDES_PDF)
	@mkdir -p $(@D)
	cp -f $< $@
	@echo "[OK] Présentation générée avec succès : $@"

$(HANDOUT_PDF): $(HANDOUT_SRC) $(IMGS)
	@echo "==> Compilation de la fiche de synthèse ($(HANDOUT_SRC))..."
	@if command -v $(LATEXMK) > /dev/null 2>&1; then \
		$(LATEXMK) $(LATEXMK_FLAGS) $(HANDOUT_SRC); \
	else \
		cd $(HANDOUT_DIR) && \
		$(PDFLATEX) $(PDFLATEX_FLAGS) $(notdir $(HANDOUT_SRC)) && \
		$(PDFLATEX) $(PDFLATEX_FLAGS) $(notdir $(HANDOUT_SRC)); \
	fi

$(BUILD_SYNTHESIS): $(HANDOUT_PDF)
	@mkdir -p $(@D)
	cp -f $< $@
	@echo "[OK] Fiche de synthèse générée avec succès : $@"

# ==============================================================================
# Démonstrations Python (optionnel)
# ==============================================================================

## demos : Exécute les scripts de simulation/démonstration Python
demos: $(BUILD_DEMOS_DIR)/dvl_drift_comparison.png $(BUILD_DEMOS_DIR)/ctd_transect_profile.png

$(BUILD_DEMOS_DIR)/dvl_drift_comparison.png: $(DEMOS_DIR)/01_dead_reckoning_dvl.py
	@mkdir -p $(BUILD_DEMOS_DIR)
	@echo "==> Exécution de la simulation 01_dead_reckoning_dvl.py..."
	$(PYTHON) $< $(BUILD_DEMOS_DIR)

$(BUILD_DEMOS_DIR)/ctd_transect_profile.png: $(DEMOS_DIR)/02_ctd_georeferencing.py
	@mkdir -p $(BUILD_DEMOS_DIR)
	@echo "==> Exécution de la simulation 02_ctd_georeferencing.py..."
	$(PYTHON) $< $(BUILD_DEMOS_DIR)

# ==============================================================================
# Mode surveillance continue (Live preview avec latexmk)
# ==============================================================================

## watch-slides : Recompile automatiquement la présentation à chaque sauvegarde
watch-slides:
	$(LATEXMK) -pvc $(LATEXMK_FLAGS) $(SLIDES_SRC)

## watch-handout : Recompile automatiquement la fiche mémo à chaque sauvegarde
watch-handout:
	$(LATEXMK) -pvc $(LATEXMK_FLAGS) $(HANDOUT_SRC)

# ==============================================================================
# Nettoyage
# ==============================================================================

## clean : Supprime les fichiers auxiliaires générés par LaTeX
clean:
	@echo "==> Nettoyage des fichiers auxiliaires LaTeX..."
	@for ext in $(AUX_EXTS); do \
		rm -f $(SLIDES_DIR)/*.$$ext $(HANDOUT_DIR)/*.$$ext $(SRC_DIR)/*.$$ext *.$$ext; \
	done
	@rm -f $(SLIDES_DIR)/texput.log $(HANDOUT_DIR)/texput.log texput.log
	@echo "[OK] Fichiers auxiliaires nettoyés."

## distclean / fclean : Supprime tous les fichiers générés (auxiliaires et PDFs)
distclean: clean
	@echo "==> Suppression des PDFs et du dossier $(BUILD_DIR)..."
	@rm -f $(SLIDES_PDF) $(HANDOUT_PDF) $(SRC_DIR)/main.pdf
	@rm -rf $(BUILD_DIR)
	@echo "[OK] Répertoire de travail entièrement réinitialisé."

fclean: distclean

# ==============================================================================
# Aide
# ==============================================================================

## help : Affiche la liste des cibles disponibles
help:
	@echo "======================================================================="
	@echo " Makefile - ANF ArchiDrone 2026 : Robotique Marine & Sous-Marine"
	@echo "======================================================================="
	@echo "Cibles disponibles :"
	@echo "  make (ou make all)   : Compile la présentation Beamer et la fiche mémo"
	@echo "  make presentation    : Compile la présentation Beamer (src/slides/main.tex)"
	@echo "  make fiche           : Compile la fiche de synthèse condensée (2 pages)"
	@echo "  make demos           : Exécute les démonstrations Python (DVL & CTD)"
	@echo "  make watch-slides    : Mode interactif continu pour la présentation"
	@echo "  make watch-handout   : Mode interactif continu pour la fiche mémo"
	@echo "  make clean           : Supprime les fichiers temporaires LaTeX (.aux, .log, ...)"
	@echo "  make distclean       : Supprime tous les fichiers générés y compris les PDFs"
	@echo "  make help            : Affiche cette aide"
	@echo "======================================================================="