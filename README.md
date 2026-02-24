# Telecom Plan Revenue Analysis

Análisis comparativo de los planes de prepago **Surf** y **Ultimate** de un
operador de telecomunicaciones, para determinar cuál genera más ingresos y
orientar la inversión publicitaria.

## Objetivo del negocio

El equipo comercial necesita decidir qué plan priorizar en su presupuesto de
publicidad. Ambos planes difieren mucho en precio y recursos incluidos:

| | Surf | Ultimate |
|---|---|---|
| Cuota mensual | \$20 | \$70 |
| Minutos incluidos | 500 | 3 000 |
| Mensajes incluidos | 50 | 1 000 |
| Datos incluidos | 15 GB | 30 GB |
| Minuto extra | \$0.03 | \$0.01 |
| Mensaje extra | \$0.03 | \$0.01 |
| GB extra | \$10.00 | \$7.00 |

> **Hipótesis de partida:** Surf podría generar ingresos competitivos por
> cargos de excedente, pese a su cuota base más baja.

## Tecnologías

Python 3.11 · pandas · NumPy · SciPy · Matplotlib · Seaborn · Jupyter Notebook

## Dataset

500 clientes observados durante 2018, en cinco tablas relacionales:

| Archivo | Descripción |
|---|---|
| `megaline_users.csv` | Perfiles de usuario (plan, ciudad, alta/baja). |
| `megaline_calls.csv` | Registro de llamadas (usuario, fecha, duración). |
| `megaline_messages.csv` | Registro de mensajes. |
| `megaline_internet.csv` | Sesiones de datos (MB consumidos). |
| `megaline_plans.csv` | Condiciones de tarifa de cada plan. |

## Estructura del proyecto

```
telecom-plan-revenue-analysis/
├── Notebook/
│   └── megaline_revenue_analysis.ipynb
├── datasets/                             # 5 CSV de uso del operador
├── telecom_plan_revenue_analysis.py      # análisis en formato script
├── requirements.txt
├── LICENSE
└── README.md
```

## Metodología

**1. Limpieza (por tabla).** Conversión de fechas a `datetime`; nulos de
`churn_date` preservados como usuarios activos; duración de llamadas redondeada
al minuto superior (convención de facturación); filtrado de sesiones en cero;
columnas auxiliares (`is_active`, `is_ny_nj`, `month`, `total_gb`).

**2. Ingeniería de ingresos.** Una función `calculate_revenue()` calcula el
ingreso mensual por usuario:

```
ingreso = cuota_mensual
        + max(0, minutos_usados − minutos_incluidos) × tarifa_minuto
        + max(0, mensajes_usados − mensajes_incluidos) × tarifa_mensaje
        + max(0, ceil(gb_usados) − gb_incluidos) × tarifa_gb
```

Los datos usan `math.ceil()`: un GB parcial se factura como GB completo.

**3. Análisis exploratorio.** Tendencias mensuales de uso por plan;
estadística descriptiva (media, varianza, desviación); histogramas de ingresos.

**4. Prueba de hipótesis.** Prueba t de Welch (`equal_var=False`), α = 0.05.

## Resultados

**Uso promedio mensual**

| Métrica | Surf | Ultimate |
|---|---|---|
| Minutos usados | 427.5 | 429.0 |
| Mensajes enviados | 31.2 | 37.6 |
| Datos consumidos | 16.1 GB | 16.8 GB |

Dato clave: ambos grupos consumen volúmenes casi idénticos, pero el límite de
Surf es de **15 GB** y sus usuarios promedian **16.1 GB** — lo exceden de forma
recurrente y disparan cargos de \$10/GB.

**Ingresos**

| Métrica | Surf | Ultimate |
|---|---|---|
| Ingreso medio mensual | \$60.33 | \$72.24 |
| Desviación estándar | \$54.95 | \$11.13 |
| Varianza | \$3 019.03 | \$123.80 |

Ultimate genera ~\$12 más por usuario al mes; Surf tiene ~25× más varianza
(ingreso impredecible por excedentes), mientras Ultimate es casi tarifa plana.

**Prueba 1 — ingresos Surf vs Ultimate:** t = −8.23, p ≈ 3.51 × 10⁻¹⁶ →
**se rechaza H₀**: los ingresos medios difieren de forma altamente significativa.

**Prueba 2 — NY-NJ vs resto:** **no concluyente** — la muestra de NY-NJ es
demasiado pequeña para un estadístico fiable (`SmallSampleWarning`).

## Conclusiones

1. **Ultimate debe ser la prioridad publicitaria:** ~20 % más de ingreso por
   usuario (\$72.24 vs \$60.33) con ingreso estable y de baja varianza.
2. **Surf no es deficitario:** los excedentes de datos (sus usuarios superan los
   15 GB) compensan parcialmente la cuota baja, pero el ingreso es volátil.
3. El comportamiento de uso es casi idéntico entre planes, lo que sugiere que
   los usuarios de Surf están limitados por su plan y son candidatos a migrar a
   Ultimate.

## Cómo ejecutar

```bash
git clone https://github.com/OrlandoCorona/telecom-plan-revenue-analysis.git
cd telecom-plan-revenue-analysis

python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

jupyter notebook Notebook/megaline_revenue_analysis.ipynb
```

El mismo análisis está disponible como script en
[`telecom_plan_revenue_analysis.py`](telecom_plan_revenue_analysis.py).

## Trabajo futuro

- Segmentar usuarios por nivel de consumo para campañas específicas.
- Estimar el *churn* asociado a cada plan.
- Automatizar un reporte mensual de ingresos.
