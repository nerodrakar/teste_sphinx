# 📘 Tutorial: Documentação com Sphinx + python\_docs\_theme

---

## ✅ Etapa 1 – Instalar Sphinx

Ative seu ambiente virtual e execute:

```bash
pip install sphinx
```

---

## ✅ Etapa 2 – Inicializar o projeto Sphinx

No diretório raiz do seu projeto (onde está `metapy_toolbox/`), rode:

```bash
sphinx-quickstart
```

### Respostas sugeridas:

* Separate source and build directories? `yes`
* Project name: `METAPY Toolbox`
* Author name: `Seu Nome`
* Project release: `1.0`
* Autodoc extension? `yes`
* Everything else: `default` (enter)

Isso cria uma estrutura como:

```
.
├── build/
├── source/
│   ├── conf.py
│   └── index.rst
```

---

## ✅ Etapa 3 – Gerar arquivos `.rst` por módulo

Use `sphinx-apidoc` com `--separate`:

```bash
sphinx-apidoc -o source metapy_toolbox --separate
```

Isso criará:

```
source/
├── metapy_toolbox.rst                  ← resumo do pacote
├── metapy_toolbox.benchmark.rst       ← 1 por módulo
├── metapy_toolbox.simulated_annealing.rst
├── ...
```

Obs.: para criar arquivos `.rst` separados por módulo, use `--separate`.
> 📌 Remova o `--separate` se quiser criar apenas um modulo
---

## ✅ Etapa 4 – Configurar o `conf.py`

Abra `source/conf.py` e edite:

### ➤ 1. Adicione o caminho do projeto

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

### ➤ 2. Ative extensões úteis

Confirme que isso está presente:

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]
```

> `napoleon` permite usar docstrings no estilo Google/NumPy.

### ➤ 3. Aplique o tema `python_docs_theme`

No terminal, instale o tema através do `pip`:

```bash
pip install python-docs-theme
```

No final de `conf.py`, adicione:

```python
html_theme = 'python_docs_theme'
```

Se quiser personalizar (opcional):

```python
html_theme_options = {
    'navigation_with_keys': True
}
```

---

## ✅ Etapa 5 – Atualizar `index.rst`

Edite `source/index.rst` com:

```rst
METAPY Toolbox Documentation
============================

.. toctree::
   :maxdepth: 2
   :caption: Módulos:

   metapy_toolbox.benchmark
   metapy_toolbox.simulated_annealing
   metapy_toolbox.genetic_algorithm
   metapy_toolbox.firefly_algorithm
   metapy_toolbox.differential_evolution
   metapy_toolbox.common_library
   metapy_toolbox.functions_metrics
   metapy_toolbox.meta
```

> 📌 Remova ou ignore `metapy_toolbox.rst` se estiver usando arquivos `.rst` por módulo.

---

## ✅ Etapa 6 – Construir a documentação

Execute:

```bash
sphinx-build -b html source build
```

---

## 📁 Resultado

A documentação HTML será gerada em:

```
build/index.html
```

Abra no navegador ou publique online (ex: GitHub Pages).

---

## ✅ Dica final: build automático (opcional)

Se quiser atualizar a doc sempre que alterar o código:

```bash
sphinx-autobuild source build
```

---

Se desejar, posso gerar esse `conf.py` já ajustado ou um `Makefile`/`make.bat` para Windows. Deseja isso?
