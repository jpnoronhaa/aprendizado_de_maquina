import pandas as pd
import numpy as np
import os

project_dir = os.path.join(os.path.dirname(__file__), "..")
data_path = os.path.join(project_dir, "data", "student_habits_performance.csv")
doc_path = os.path.join(project_dir, "doc", "dataset_dict_generated.md")


def create_markdown_table(data_dict, title):
    markdown_table = f"### {title}\n\n"
    header = "| Nome da Variável | Tipo | Descrição | Unidade | Valores Presentes | Observações |\n"
    separator = "|---|---|---|---|---|---|\n"
    markdown_table += header + separator

    for field, details in data_dict.items():
        row = f"| {field} | {details.get('type', '')} | {details.get('description', '')} | {details.get('unit', '')} | {details.get('interval', '')} | {details.get('obs', '')} |\n"
        markdown_table += row

    return markdown_table

def save_markdown(markdown_content, filename):
    with open(filename, "w") as file:
        file.write(markdown_content)

df = pd.read_csv(data_path)

columns = df.columns
data_dict = {}

for col in columns:
  data_dict[col] = {
    'type': str(df.dtypes[col]),
    'description': '-',
    'unit': '-',
    'interval': ', '.join(map(str, df[col].unique())) if len(df[col].unique()) <= 5 else f'{df[col].min()} - {df[col].max()}' if (df[col].dtype == np.int64 or df[col].dtype == np.float64) else '-',
    'obs': '-',
  }

table = create_markdown_table(data_dict, 'Dicionário da Base de Dados')
save_markdown(table, doc_path)