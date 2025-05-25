from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
import numpy as np

def fill_parental_education_level(df):
  """ Preenche os campos não presentes de parental_education_level com 'High School'
  Args:
    df (pd.Dataframe): DataFrame com os dados dos estudantes

  Returns:
    None: sem retorno
  """
  df['parental_education_level'].fillna(value='High School')
  return None

def frequency_encoding(df, columns):
  """ Aplica a Codificação de Frequência nas colunas especificadas de um DataFrame.
  Args:
    df (pd.DataFrame): DataFrame original
    columns (list): Lista de nomes de colunas categóricas para codificar
  
  Returns:
    pd.DataFrame: Novo DataFrame com as colunas codificadas
    dict: Dicionário com os mapeamentos de categorias para valores de frequência
  """
  df_encoded = df.copy()
  frequency_maps = {}
  
  for col in columns:
    freq = df[col].value_counts()
    df_encoded[col] = df[col].map(freq)
    frequency_maps[col] = {k: int(v) for k, v in freq.to_dict().items()}
  
  return df_encoded, frequency_maps

def aplicar_ordinal_encoder(df, colunas_categoricas):
  """ Aplica OrdinalEncoder nas colunas categóricas especificadas de um DataFrame.
  Args:
    df (pd.DataFrame): DataFrame original
    colunas_categoricas (list): Lista de nomes de colunas categóricas para codificar
  
  Returns:
    pd.DataFrame: Novo DataFrame com as colunas codificadas
    dict: Dicionário com os mapeamentos de categorias para valores numéricos
  """
  df_codificado = df.copy()
  encoder = OrdinalEncoder()
  df_codificado[colunas_categoricas] = encoder.fit_transform(df[colunas_categoricas])
  
  mapeamentos = {}
  for i, coluna in enumerate(colunas_categoricas):
    mapeamentos[coluna] = {categoria: idx for idx, categoria in enumerate(encoder.categories_[i])}
  
  return df_codificado, mapeamentos

def remove_outliers_iqr(df, numeric_columns, threshold=1.5):
  """ Remove outliers de colunas numéricas usando o método IQR.
  Args:
    df (pd.DataFrame): DataFrame original
    numeric_columns (list): Lista de colunas numéricas
    threshold (float): Multiplicador do IQR (padrão 1.5)
    return_plots (bool): Se True, retorna figuras para visualização
  
  Returns:
    pd.DataFrame: DataFrame sem outliers
    dict: Estatísticas dos outliers removidos
  """
  df_clean = df.copy()
  outlier_stats = {}
  
  for col in numeric_columns:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    
    outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
    outlier_count = len(outliers)
    
    outlier_stats[col] = {
      'outlier_count': outlier_count,
      'percent_outliers': (outlier_count / len(df)) * 100,
      'lower_bound': lower_bound,
      'upper_bound': upper_bound,
      'min_value': df_clean[col].min(),
      'max_value': df_clean[col].max()
    }
    
    df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
  
  return df_clean, outlier_stats

def remove_ordinal_outliers_zscore(df, ordinal_columns, z_threshold=3):
  """ Remove outliers de colunas ordinais usando z-score.
  Args:
    df (pd.DataFrame): DataFrame original
    ordinal_columns (list): Lista de colunas ordinais
    z_threshold (float): Limite do z-score (padrão 3)
  
  Returns:
    pd.DataFrame: DataFrame sem outliers
    dict: Estatísticas dos outliers removidos
  """
  df_clean = df.copy()
  outlier_stats = {}
  
  for col in ordinal_columns:
    mean = df_clean[col].mean()
    std = df_clean[col].std()
    
    z_scores = np.abs((df_clean[col] - mean) / std)
    
    outliers = df_clean[z_scores > z_threshold]
    outlier_count = len(outliers)
    
    outlier_stats[col] = {
      'outlier_count': outlier_count,
      'percent_outliers': (outlier_count / len(df)) * 100,
      'z_threshold': z_threshold,
      'mean': mean,
      'std': std
    }
    
    df_clean = df_clean[z_scores <= z_threshold]
  
  return df_clean, outlier_stats

def remove_nominal_outliers_frequency(df, nominal_columns, freq_threshold=0.01):
  """ Remove outliers de colunas nominais com base na frequência.
  Args:
    df (pd.DataFrame): DataFrame original
    nominal_columns (list): Lista de colunas nominais
    freq_threshold (float): Limite mínimo de frequência (0-1)
  
  Returns:
    pd.DataFrame: DataFrame sem outliers
    dict: Estatísticas dos outliers removidos
  """
  df_clean = df.copy()
  outlier_stats = {}
  
  for col in nominal_columns:
    freq = df_clean[col].value_counts()
    
    rare_categories = freq[freq < freq_threshold].index
    outliers = df_clean[df_clean[col].isin(rare_categories)]
    outlier_count = len(outliers)
    
    outlier_stats[col] = {
      'outlier_count': outlier_count,
      'percent_outliers': (outlier_count / len(df)) * 100,
      'freq_threshold': freq_threshold,
      'rare_categories': list(rare_categories),
      'category_counts': df[col].value_counts().to_dict()
    }
    
    df_clean = df_clean[~df_clean[col].isin(rare_categories)]
  
  return df_clean, outlier_stats

def min_max_normalization(df, columns, feature_range=(0, 1)):
  """ Aplica normalização Min-Max nas colunas especificadas.
  Args:
  df (pd.DataFrame): DataFrame original
  columns (list): Lista de colunas numéricas para normalizar
  feature_range (tuple): Intervalo desejado (padrão 0-1)

  Returns:
  pd.DataFrame: DataFrame com colunas normalizadas
  dict: Parâmetros de normalização usados
  """
  df_norm = df.copy()
  scaler = MinMaxScaler(feature_range=feature_range)
  normalization_params = {}

  df_norm[columns] = scaler.fit_transform(df[columns])

  for i, col in enumerate(columns):
    normalization_params[col] = {
      'min_original': scaler.data_min_[i],
      'max_original': scaler.data_max_[i],
      'min_scaled': feature_range[0],
      'max_scaled': feature_range[1]
    }

  return df_norm, normalization_params