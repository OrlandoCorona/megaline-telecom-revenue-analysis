"""
Análisis de ingresos por plan telefónico — Surf vs Ultimate.

Versión en script del análisis exploratorio del notebook
`megaline_revenue_analysis.ipynb`. Limpia los datos de uso (llamadas,
mensajes e internet), calcula el ingreso mensual por usuario y compara
estadísticamente ambos planes.
"""

import numpy as np
import pandas as pd
from scipy import stats


# Cargar todas las librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime

# --- Cargar datos ---
# Carga los archivos de datos en diferentes DataFrames
users = pd.read_csv('datasets/megaline_users.csv')
calls = pd.read_csv('datasets/megaline_calls.csv')
messages = pd.read_csv('datasets/megaline_messages.csv')
internet = pd.read_csv('datasets/megaline_internet.csv')
plans = pd.read_csv('datasets/megaline_plans.csv')

# --- Tarifas ---
print("Información general de plans:")
print(plans.info())
print("\nDescripción de plans:")
print(plans.describe())

# Imprime una muestra de los datos para las tarifas
print("Muestra de datos de plans:")
print(plans)

# --- Enriquecer los datos ---
plans['gb_per_month_included'] = plans['mb_per_month_included'] / 1024

# --- Usuarios/as ---
# Imprime la información general/resumida sobre el DataFrame de usuarios
print("Información general de users:")
print(users.info())
print("Descripción de users:")
print(users.describe(include='all'))

# Imprime una muestra de datos para usuarios
print("Muestra de datos de users:")
print(users.head())

# --- Corregir los datos ---
# Convertir reg_date y churn_date a datetime
users['reg_date'] = pd.to_datetime(users['reg_date'])
users['churn_date'] = pd.to_datetime(users['churn_date'], errors='coerce')

# Verificar tipos de datos
users['user_id'] = users['user_id'].astype(int)
users['age'] = users['age'].astype(int)
users['plan'] = users['plan'].astype(str)

# --- Enriquecer los datos ---
# Agregar columna para indicar si el usuario esta activo
users['is_active'] = users['churn_date'].isna()
# Agregar columna para identificar región NY-NJ
users['is_ny_nj'] = users['city'].str.contains('New York-NY-NJ-PA', case=False, na=False)

# --- Llamadas ---
# Imprime la información general/resumida sobre el DataFrame de las llamadas
print("Información general de calls:")
print(calls.info())
print("Descripción de calls:")
print(calls.describe())

# Imprime una muestra de datos para las llamadas
print("Muestra de datos de calls:")
print(calls.head())

# Validar valores atípicos en duration
plt.figure(figsize=(8, 6))
sns.boxplot(y=calls['duration'])
plt.title('Distribución de duration en calls')
plt.ylabel('Duración (minutos)')
plt.show()

# --- Corregir los datos ---
# Convertir call_date a datetime
calls['call_date'] = pd.to_datetime(calls['call_date'])

# Redondear duración al minuto superior
calls['duration_rounded'] = np.ceil(calls['duration'])

# Filtrar duration = 0.0 para consumo real
calls = calls[calls['duration'] > 0]

# Manejar valores atípicos en duration (capping al percentil 99 si es necesario)
duration_p99 = calls['duration'].quantile(0.99)
calls['duration'] = calls['duration'].clip(upper=duration_p99)
calls['duration_rounded'] = np.ceil(calls['duration'])

# Verificar tipos de datos
calls['user_id'] = calls['user_id'].astype(int)
calls['duration'] = calls['duration'].astype(float)

calls['month'] = calls['call_date'].dt.to_period('M')

# --- Mensajes ---
# Imprime la información general/resumida sobre el DataFrame de los mensajes
print("Información general de messages:")
print(messages.info())
print("Descripción de messages:")
print(messages.describe())

# Imprime una muestra de datos para los mensajes
print("Muestra de datos de messages:")
print(messages.head())

# --- Corregir los datos ---
# Convertir message_date a datetime
messages['message_date'] = pd.to_datetime(messages['message_date'])

# Verificar tipos de datos
messages['user_id'] = messages['user_id'].astype(int)

# --- Enriquecer los datos ---
# Agregar columna de mes
messages['month'] = messages['message_date'].dt.to_period('M')

# --- Internet ---
# Imprime la información general/resumida sobre el DataFrame de internet
print("Información general de internet:")
print(internet.info())
print("Descripción de internet:")
print(internet.describe())

# Imprime una muestra de datos para el tráfico de internet
print("Muestra de datos de internet:")
print(internet.head())

# Valida valores atipicos en mb_used
plt.figure(figsize=(8, 6))
sns.boxplot(y=internet['mb_used'])
plt.title('Distribución de mb_used en internet')
plt.ylabel('Megabytes')
plt.show()

# --- Corregir los datos ---
internet['session_date'] = pd.to_datetime(internet['session_date'])

# Filtra mb_used = 0.0 para consumo real
internet = internet[internet['mb_used'] > 0]

# Maneja valores atípicos en mb_used (capping al percentil 99 si es necesario)
mb_used_p99 = internet['mb_used'].quantile(0.99)
internet['mb_used'] = internet['mb_used'].clip(upper=mb_used_p99)

# Verifica tipos de datos
internet['user_id'] = internet['user_id'].astype(int)
internet['mb_used'] = internet['mb_used'].astype(float)

# Agrega columna de mes
internet['month'] = internet['session_date'].dt.to_period('M')

# Imprime las condiciones de la tarifa
print("Condiciones de las tarifas:")
print(plans)

# --- Agregar datos por usuario ---
# Calcula el numero de llamadas hechas por cada usuario al mes
calls_per_user_month = calls.groupby(['user_id', 'month'])['id'].count().reset_index(name='call_count')

# Calcula la cantidad de minutos usados por cada usuario al mes. Guarda el resultado.
minutes_per_user_month = calls.groupby(['user_id', 'month'])['duration_rounded'].sum().reset_index(name='total_minutes')

# Calcula el número de mensajes enviados por cada usuario al mes. Guarda el resultado.
messages_per_user_month = messages.groupby(['user_id', 'month'])['id'].count().reset_index(name='message_count')

# Calcula el volumen del tráfico de Internet usado por cada usuario al mes. Guarda el resultado.
internet_per_user_month = internet.groupby(['user_id', 'month'])['mb_used'].sum().reset_index(name='total_mb')

# Fusiona los datos
user_monthly_data = calls_per_user_month.merge(minutes_per_user_month, on=['user_id', 'month'], how='outer')
user_monthly_data = user_monthly_data.merge(messages_per_user_month, on=['user_id', 'month'], how='outer')
user_monthly_data = user_monthly_data.merge(internet_per_user_month, on=['user_id', 'month'], how='outer')

user_monthly_data.fillna({'call_count': 0, 'total_minutes': 0, 'message_count': 0, 'total_mb': 0}, inplace=True)

# información de la tarifa
user_monthly_data = user_monthly_data.merge(users[['user_id', 'plan']], on='user_id', how='left')
user_monthly_data = user_monthly_data.merge(plans, left_on='plan', right_on='plan_name', how='left')

# Calcular el ingreso mensual para cada usuario
def calculate_revenue(row):
    # Minutos excedentes
    minutes_excess = max(0, row['total_minutes'] - row['minutes_included'])
    minutes_cost = minutes_excess * row['usd_per_minute']
    
    # Mensajes excedentes
    messages_excess = max(0, row['message_count'] - row['messages_included'])
    messages_cost = messages_excess * row['usd_per_message']
    
    # Datos excedentes (redondeo al GB superior por mes)
    total_gb = np.ceil(row['total_mb'] / 1024)
    gb_included = row['mb_per_month_included'] / 1024
    gb_excess = max(0, total_gb - gb_included)
    data_cost = gb_excess * row['usd_per_gb']
    
    # Total: cuota mensual + costos por excedentes
    return row['usd_monthly_pay'] + minutes_cost + messages_cost + data_cost

user_monthly_data['revenue'] = user_monthly_data.apply(calculate_revenue, axis=1)

# --- Llamadas ---
# Compara la duración promedio de llamadas por cada plan y por cada mes
avg_call_duration = user_monthly_data.groupby(['plan', 'month'])['total_minutes'].mean().unstack(level=0)
avg_call_duration.plot(kind='bar', figsize=(12, 6))
plt.title('Duración promedio de llamadas por plan y mes')
plt.xlabel('Mes')
plt.ylabel('Minutos promedio')
plt.legend(title='Plan')
plt.show()

# Compara el número de minutos mensuales que necesitan los usuarios de cada plan
plt.figure(figsize=(10, 6))
for plan in ['surf', 'ultimate']:
    sns.histplot(data=user_monthly_data[user_monthly_data['plan'] == plan], x='total_minutes', label=plan, kde=True)
plt.title('Distribución de minutos mensuales por plan')
plt.xlabel('Minutos')
plt.legend()
plt.show()

call_stats = user_monthly_data.groupby('plan')['total_minutes'].agg(['mean', 'var', 'std'])
print("Estadísticas de minutos por plan:")
print(call_stats)

# Traza un diagrama de caja para visualizar la distribución
plt.figure(figsize=(8, 6))
sns.boxplot(x='plan', y='total_minutes', data=user_monthly_data)
plt.title('Distribución de minutos mensuales por plan')
plt.xlabel('Plan')
plt.ylabel('Minutos')
plt.show()

# --- Mensajes ---
# Compara el numero de mensajes que tienden a enviar cada mes los usuarios de cada plan
plt.figure(figsize=(10, 6))
for plan in ['surf', 'ultimate']:
    sns.histplot(data=user_monthly_data[user_monthly_data['plan'] == plan], x='message_count', label=plan, kde=True)
plt.title('Distribución de mensajes mensuales por plan')
plt.xlabel('Mensajes')
plt.legend()
plt.show()

# Estadi­sticas de mensajes
message_stats = user_monthly_data.groupby('plan')['message_count'].agg(['mean', 'var', 'std'])
print("Estadísticas de mensajes por plan:")
print(message_stats)

# --- Internet ---
# Compara la cantidad de trafico de Internet consumido por usuarios por plan
user_monthly_data['total_gb'] = user_monthly_data['total_mb'] / 1024
plt.figure(figsize=(10, 6))
for plan in ['surf', 'ultimate']:
    sns.histplot(data=user_monthly_data[user_monthly_data['plan'] == plan], x='total_gb', label=plan, kde=True)
plt.title('Distribución de datos mensuales (GB) por plan')
plt.xlabel('Gigabytes')
plt.legend()
plt.show()

# Estadísticas de datos
data_stats = user_monthly_data.groupby('plan')['total_gb'].agg(['mean', 'var', 'std'])
print("Estadísticas de datos por plan:")
print(data_stats)

# --- Ingreso ---
# Describe estadísticamente los ingresos de los planes
revenue_stats = user_monthly_data.groupby('plan')['revenue'].agg(['mean', 'var', 'std'])
print("Estadísticas de ingresos por plan:")
print(revenue_stats)

# Visualizar distribución de ingresos
plt.figure(figsize=(10, 6))
for plan in ['surf', 'ultimate']:
    sns.histplot(data=user_monthly_data[user_monthly_data['plan'] == plan], x='revenue', label=plan, kde=True)
plt.title('Distribución de ingresos mensuales por plan')
plt.xlabel('Ingresos (USD)')
plt.legend()
plt.show()

# --- Prueba de las hipotesis estadi­sticas ---
# Prueba las hipotesis
surf_revenue = user_monthly_data[user_monthly_data['plan'] == 'surf']['revenue']
ultimate_revenue = user_monthly_data[user_monthly_data['plan'] == 'ultimate']['revenue']

t_stat, p_value = stats.ttest_ind(surf_revenue, ultimate_revenue, equal_var=False)
print("Prueba t para ingresos Surf vs. Ultimate:")
print(f"Estadistico t: {t_stat}, p-valor: {p_value}")

if p_value < 0.05:
    print("Rechazamos H0: Los ingresos promedio de Surf y Ultimate son diferentes.")
else:
    print("No rechazamos H0: No hay evidencia suficiente para decir que los ingresos promedio difieren.")

# Fusionar datos de ingresos con ciudad
user_monthly_data = user_monthly_data.merge(users[['user_id', 'city']], on='user_id', how='left')

ny_nj_revenue = user_monthly_data[user_monthly_data['city'].str.contains('New York-NY-NJ-PA', case=False, na=False)]['revenue']
other_revenue = user_monthly_data[~user_monthly_data['city'].str.contains('New York-NY-NJ-PA', case=False, na=False)]['revenue']

t_stat, p_value = stats.ttest_ind(ny_nj_revenue, other_revenue, equal_var=False)
print("Prueba t para ingresos NY-NJ vs. otras regiones:")
print(f"Estadística t: {t_stat}, p-valor: {p_value}")

if p_value < 0.05:
    print("Rechazamos H0: Los ingresos promedio de NY-NJ y otras regiones son diferentes.")
else:
    print("No rechazamos H0: No hay evidencia suficiente para decir que los ingresos promedio difieren.")

