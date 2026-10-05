# Makefile minimal pour Sphinx.
# Disposition "plate" : conf.py et les .rst sont ici, la sortie va dans _build/.

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# "make" ou "make help" affiche la liste des constructeurs disponibles.
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Cible fourre-tout : tout autre argument (html, latexpdf, clean, ...) est
# transmis tel quel à sphinx-build.
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
