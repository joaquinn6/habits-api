from datetime import datetime, date, time
from calendar import monthrange


def range_of_date(year, month=0):
  """
  Obtiene el primer y último día de un mes y año, o de un año completo.

  Args:
      año (int): El año.
      mes (int, opcional): El mes. Si se proporciona, se obtiene el rango del mes. Si no, se obtiene el rango del año.

  Returns:
      tuple: Una tupla con las fechas de inicio y fin (date objects).
  """

  if month != 0:
    # Obtener el primer y último día del month con horas
    primer_dia_date = date(year, month, 1)
    ultimo_dia_date = date(year, month, monthrange(year, month)[1])

    primer_dia = datetime.combine(primer_dia_date, time.min)  # 00:00:00
    ultimo_dia = datetime.combine(ultimo_dia_date, time.max)  # 23:59:59
  else:
    # Obtener el primer y último día del año con horas
    primer_dia_date = date(year, 1, 1)
    ultimo_dia_date = date(year, 12, 31)

    primer_dia = datetime.combine(primer_dia_date, time.min)  # 00:00:00
    ultimo_dia = datetime.combine(ultimo_dia_date, time.max)  # 23:59:59

  return primer_dia, ultimo_dia
