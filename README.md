# Telecom Plan Revenue Analysis

Análisis comparativo de los planes de prepago **Surf** y **Ultimate** de un
operador de telecomunicaciones, orientado a identificar cuál genera más
ingresos y dónde conviene concentrar la inversión publicitaria.

## Objetivo del negocio

El equipo comercial necesita decidir cómo repartir el presupuesto de
publicidad entre los dos planes. La pregunta clave es:

> ¿Qué plan deja **más ingresos por usuario** y existe una diferencia
> estadísticamente significativa entre ambos?

A partir del comportamiento de 500 clientes (llamadas, mensajes y consumo de
datos) se calcula el ingreso mensual real de cada usuario —cuota fija más
cargos por excedente— y se contrasta una hipótesis sobre la diferencia de
ingresos.

## Tecnologías

- Python 3.11
- pandas / NumPy — limpieza y agregación de datos
- SciPy — prueba de hipótesis (t de Welch)
- Matplotlib / Seaborn — visualización
- Jupyter Notebook

## Dataset

Cinco tablas con el uso mensual del operador (aprox. diciembre 2018): usuarios,
llamadas, mensajes, sesiones de internet y condiciones de los planes. El
detalle de cada archivo está en [`datasets/README.md`](datasets/README.md).

## Proceso de análisis

1. **Carga y exploración** de las cinco tablas.
2. **Limpieza:** conversión de fechas a `datetime`, tipos de datos correctos,
   filtrado de registros en cero y *capping* de valores atípicos al
   percentil 99.
3. **Enriquecimiento:** columnas auxiliares (`is_active`, `is_ny_nj`, `month`,
   `gb_per_month_included`).
4. **Agregación por usuario/mes:** llamadas, minutos, mensajes y datos.
5. **Cálculo de ingresos:** cuota mensual + excedentes de minutos, mensajes y
   gigabytes según las condiciones de cada plan.
6. **Análisis comparativo** de minutos, mensajes y datos por plan.
7. **Pruebas de hipótesis:** ingresos Surf vs Ultimate y NY-NJ vs resto.

## Resultados

- Los usuarios de **Ultimate** consumen más minutos, mensajes y datos por sus
  límites más altos; **Surf** genera ingresos extra vía excedentes (sobre todo
  de datos).
- La prueba t de Welch muestra que los ingresos promedio de ambos planes
  **difieren de forma significativa** (p-valor < 0.05).

## Conclusiones

**Ultimate** ofrece un ingreso medio más alto y estable, por lo que es el
candidato natural para concentrar la inversión publicitaria. Conviene además
vigilar a los usuarios de **Surf** con alto consumo de datos: son buenos
candidatos a migrar a un plan superior.

## Estructura del proyecto

```
telecom-plan-revenue-analysis/
├── Notebook/
│   └── megaline_revenue_analysis.ipynb   # análisis exploratorio
├── datasets/                             # 5 CSV de uso del operador
├── telecom_plan_revenue_analysis.py      # análisis en formato script
├── requirements.txt
├── LICENSE
└── README.md
```

## Cómo ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/OrlandoCorona/telecom-plan-revenue-analysis.git
cd telecom-plan-revenue-analysis

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Abrir el notebook
jupyter notebook Notebook/megaline_revenue_analysis.ipynb
```

El mismo análisis está disponible como script en
[`telecom_plan_revenue_analysis.py`](telecom_plan_revenue_analysis.py).

## Capturas sugeridas

Para enriquecer este README puedes añadir, en una carpeta `images/`:

- Distribución de ingresos mensuales por plan (histograma).
- Boxplot de minutos por plan.
- Resultado de la prueba de hipótesis.

## Trabajo futuro

- Segmentar a los usuarios por nivel de consumo (clustering) para diseñar
  campañas más específicas.
- Estimar el *churn* asociado a cada plan.
- Automatizar la generación de un reporte mensual.
