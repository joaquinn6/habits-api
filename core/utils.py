from datetime import datetime, date, time
from calendar import monthrange
from dateutil.relativedelta import relativedelta


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
    first_day_date = date(year, month, 1) - relativedelta(months=1)

    # Obtener el último día del mes siguiente
    next_month = date(year, month, 1) + relativedelta(months=1)
    last_day_date = date(next_month.year, next_month.month, monthrange(
        next_month.year, next_month.month)[1])

    # Combinar con horas
    first_day = datetime.combine(first_day_date, time.min)
    last_day = datetime.combine(last_day_date, time.max)
  else:
    # Obtener el primer y último día del año con horas
    first_day_date = date(year, 1, 1)
    last_day_date = date(year, 12, 31)

    first_day = datetime.combine(first_day_date, time.min)
    last_day = datetime.combine(last_day_date, time.max)

  return first_day, last_day
