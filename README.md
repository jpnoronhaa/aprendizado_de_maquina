### Códigos da Disciplina de Aprendizado de Máquina (UFT, Ciência da Computação, 2025.01) 

Aula 01 - Introdução à Inteligência Artificial e ao Aprendizado de Máquina.

Aula 02 - Utilização da API de consulta do Google.

O arquivo environment.yml possui as configurações do ambiente conda, ele deve ser sempre exportando para funcionar em diferentes plataformas (MacOS e Linux preferencialmente).

Código para exportar o ambiente conda junto com os pacotes instalados pelo `pip`, fonte [ekiwi111](https://github.com/conda/conda/issues/9628#issuecomment-1608913117) no github:

```bash
# Extract installed pip packages
pip_packages=$(conda env export | grep -A9999 ".*- pip:" | grep -v "^prefix: ")

# Export conda environment without builds, and append pip packages
conda env export --from-history | grep -v "^prefix: " > environment.yml
echo "$pip_packages" >> environment.yml
```

Código para criar o ambiente local com base no arquivo `environment.yml`:

```bash
conda env create -f environment.yml
```

