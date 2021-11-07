from django.shortcuts import render

# Create your views here.

import pandas as pd
import numpy as np
from django.views.generic import TemplateView
from .methods import csv_to_db
from .models import Purchase
from .charts import load_data, Chart, average_power, max_power, last_power, history

PALETTE = ['#465b65', '#184c9c', '#d33035', '#ffc107', '#28a745', '#6f7f8c', '#6610f2', '#6e9fa5', '#fd7e14', '#e83e8c', '#17a2b8', '#6f42c1' ]

class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['charts'] = []
        
        df = load_data("/home/pi/gitwork/electric_meter_web/electric_meter/data/meter_data.csv")

        context['avergage_power'] = average_power(df, 'Current Power [W]')
        context['max_power'] = max_power(df, 'Current Power [W]')
        context['current_power'] = last_power(df, 'Current Power [W]')

        df_reduced = history(df, hours=2)

        current_power = Chart('line', chart_id='current_power', palette=['#9E4770'])
        current_power.from_df(df_reduced, values='Current Power [W]', labels=['Date'], round_values=0, title='Power [W] - Last 2h')
        context['charts'].append(current_power.get_presentation())

        total_energy = Chart('line', chart_id='total_energy', palette=['#631D76'])
        total_energy.from_df(df_reduced, values='Total Energy [kWh]', labels=['Date'], round_values=3, title='Energy [kWh] - Last 2h')
        context['charts'].append(total_energy.get_presentation())

        df_reduced = history(df, hours=24)
        current_power_long_term = Chart('line', chart_id='current_power_long_term', palette=['#9E4770'])
        current_power_long_term.from_df(df_reduced, values='Current Power [W]', labels=['Date'], round_values=0, title='Power [W] - Last 24h')
        context['charts'].append(current_power_long_term.get_presentation())
        
        total_energy_long_term = Chart('line', chart_id='total_energy_long_term', palette=['#631D76'])
        total_energy_long_term.from_df(df_reduced, values='Total Energy [kWh]', labels=['Date'], round_values=3, title='Energy [kWh] - Last 24h')
        context['charts'].append(total_energy_long_term.get_presentation())
        
        return context
