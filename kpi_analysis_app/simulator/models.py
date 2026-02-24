from django.db import models

class ProductionData(models.Model):
    # Базовые входные параметры
    date = models.DateField(auto_now_add=True)  # Для исторических данных
    ore_volume = models.FloatField(help_text="Объём добытой руды, тонн")  # Q
    operating_time = models.FloatField(help_text="Плановое время работы, часы")  # T_plan
    downtime = models.FloatField(help_text="Время простоя, часы")  # T_down
    crew_size = models.IntegerField(help_text="Численность бригады")  # N
    fuel_consumption = models.FloatField(help_text="Расход топлива, литры")  # F
    # При необходимости добавьте другие поля: electricity_consumption, material_costs и т.д.

    def __str__(self):
        return f"Данные за {self.date}: {self.ore_volume}т"

    class Meta:
        verbose_name = "Производственные данные"
        verbose_name_plural = "Производственные данные"
