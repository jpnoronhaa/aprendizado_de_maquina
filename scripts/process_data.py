import pandas as pd
import numpy as np
import json
from src.preprocessing import (
    fill_parental_education_level,
    frequency_encoding,
    aplicar_ordinal_encoder,
    remove_outliers_iqr,
    remove_ordinal_outliers_zscore,
    remove_nominal_outliers_frequency,
    min_max_normalization
)

def convert_to_serializable(obj):
  """Converte objetos numpy para tipos nativos do Python para serialização JSON"""
  if isinstance(obj, (np.int32, np.int64)):
    return int(obj)
  elif isinstance(obj, (np.float32, np.float64)):
    return float(obj)
  elif isinstance(obj, np.ndarray):
    return obj.tolist()
  elif isinstance(obj, dict):
    return {k: convert_to_serializable(v) for k, v in obj.items()}
  elif isinstance(obj, list):
    return [convert_to_serializable(v) for v in obj]
  return obj

def process_data(input_file, output_file, stats_file):
  """ Processa os dados do arquivo de entrada e salva o resultado no arquivo de saída. 
  Também salva estatísticas do processamento em um arquivo JSON.
  
  Args:
    input_file (str): Caminho para o arquivo de entrada CSV
    output_file (str): Caminho para o arquivo de saída CSV
    stats_file (str): Caminho para o arquivo de estatísticas JSON
  """
  df = pd.read_csv(input_file)
  
  processing_stats = {}
  
  fill_parental_education_level(df)
  processing_stats['missing_values'] = {
    'parental_education_level': 'Valores nulos preenchidos com "High School"'
  }
  
  nominal_cols = ['gender', 'part_time_job', 'extracurricular_participation']
  df, freq_maps = frequency_encoding(df, nominal_cols)
  processing_stats['frequency_encoding'] = freq_maps
  
  ordinal_cols = ['diet_quality', 'parental_education_level', 'internet_quality']
  if ordinal_cols:
    df, ordinal_maps = aplicar_ordinal_encoder(df, ordinal_cols)
    processing_stats['ordinal_encoding'] = ordinal_maps
  
  numeric_cols = ['age', 'study_hours_per_day', 'social_media_hours', 
    'netflix_hours', 'attendance_percentage', 'sleep_hours',
    'exercise_frequency', 'mental_health_rating', 'exam_score']
  df, numeric_outliers = remove_outliers_iqr(df, numeric_cols)
  processing_stats['numeric_outliers'] = numeric_outliers
  
  ordinal_outlier_cols = ['diet_quality', 'parental_education_level', 'internet_quality']
  if ordinal_outlier_cols:
    df, ordinal_outliers = remove_ordinal_outliers_zscore(df, ordinal_outlier_cols)
    processing_stats['ordinal_outliers'] = ordinal_outliers
  
  df, nominal_outliers = remove_nominal_outliers_frequency(df, nominal_cols)
  processing_stats['nominal_outliers'] = nominal_outliers
  
  cols_to_normalize = ['study_hours_per_day', 'social_media_hours', 'netflix_hours',
    'attendance_percentage', 'sleep_hours', 'exam_score']
  df, norm_params = min_max_normalization(df, cols_to_normalize)
  processing_stats['normalization'] = norm_params


  processing_stats = convert_to_serializable(processing_stats)
  df.to_csv(output_file, index=False)
  
  with open(stats_file, 'w') as f:
    json.dump(processing_stats, f, indent=4, default=str)
  
  print(f"Processamento concluído. Dados salvos em {output_file}")
  print(f"Estatísticas de processamento salvas em {stats_file}")

if __name__ == "__main__":
  import argparse
  
  parser = argparse.ArgumentParser(description='Processamento de dados de estudantes')
  parser.add_argument('input', help='Arquivo de entrada CSV')
  parser.add_argument('output', help='Arquivo de saída CSV')
  parser.add_argument('--stats', default='processing_stats.json',  help='Arquivo de estatísticas JSON')
  
  args = parser.parse_args()

  try:
    process_data(args.input, args.output, args.stats)
    print("Processamento concluído com sucesso!")
  except Exception as e:
    print(f"Erro durante o processamento: {str(e)}")
    raise