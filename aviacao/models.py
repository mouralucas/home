# from django.db import models
# import core.models
#
#
# class CompanhiaAerea(core.models.Log):
#     nome = models.CharField(max_length=250, null=True)
#     alias = models.CharField(max_length=200, null=True)
#     iata = models.CharField(max_length=10, null=True)
#     icao = models.CharField(max_length=10, null=True)
#     callsign = models.CharField(max_length=100, null=True)
#     country = models.CharField(max_length=250, null=True)
#
#     class Meta:
#         db_table = 'aviacao"."companhiaaerea'
#
#
# class Aeroporto(core.models.Log):
#     ident = models.CharField(max_length=50, null=True)
#     tipo = models.CharField(max_length=200, null=True)
#     nome = models.CharField(max_length=250, null=True)
#     latitude = models.CharField(max_length=250, null=True)
#     longitude = models.CharField(max_length=250, null=True)
#     elevacao = models.IntegerField(null=True)
#     continente = models.CharField(max_length=20, null=True)
#     pais = models.ForeignKey('core.Pais', on_delete=models.DO_NOTHING, null=True)
#     regiao = models.ForeignKey('core.Regiao', on_delete=models.DO_NOTHING, null=True)
#     cidade = models.CharField(max_length=250, null=True)
#     iata = models.CharField(max_length=10, null=True)
#     icao = models.CharField(max_length=10, null=True)
#     timezone_offset = models.DecimalField(max_digits=5, decimal_places=2, null=True)
#     codigo_local = models.CharField(max_length=10, null=True)
#
#     class Meta:
#         db_table = 'aviacao"."aeroporto'
#
#
# class Voo(core.models.Log):
#     companhia = models.ForeignKey('aviacao.CompanhiaAerea', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_companhia')
#     data = models.DateField(null=True, db_index=True)
#     partida_tz_offset = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text='Timezone offset from origin airport')
#     nr_voo = models.CharField(max_length=15)
#     registro = models.CharField(max_length=15, null=True, help_text='tail number')
#     origem = models.ForeignKey('aviacao.Aeroporto', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_origem')
#     destino = models.ForeignKey('aviacao.Aeroporto', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_destino')
#     partida_prevista = models.TimeField(null=True)
#     dat_partida_prevista = models.DateTimeField(null=True)
#     partida_real = models.TimeField(null=True)
#     dat_partida_real = models.DateTimeField(null=True)
#     partida_atraso = models.IntegerField(null=True)
#     weels_off = models.TimeField(null=True)
#     dat_weels_off = models.DateTimeField(null=True)
#     taxi_out = models.IntegerField(null=True)
#
#     chegada_tz_offset = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text='Timezone offset from destination airport')
#     weels_on = models.TimeField(null=True)
#     dat_weels_on = models.DateTimeField(null=True)
#     taxi_in = models.IntegerField(null=True)
#     chegada_prevista = models.TimeField(null=True)
#     dat_chegada_prevista = models.DateTimeField(null=True)
#     chegada_real = models.TimeField(null=True)
#     dat_chegada_real = models.DateTimeField(null=True)
#     chegada_atraso = models.IntegerField(null=True)
#
#     is_cancelado = models.BooleanField(default=False, null=True)
#     is_alternado = models.BooleanField(default=False, null=True)
#
#     tempo_corrido_previsto = models.IntegerField(null=True)
#     tempo_corrido_real = models.IntegerField(null=True)
#
#     tempo_ar = models.IntegerField(null=True)
#
#     distancia = models.IntegerField(null=True)
#
#     atraso_companhia = models.IntegerField(null=True, help_text='The cause of the cancellation or delay was due to circumstances within the airlines control (e.g. maintenance or crew problems, aircraft cleaning, baggage loading, fueling, etc.)')
#     atraso_tempo = models.IntegerField(null=True, help_text='Significant meteorological conditions')
#     atraso_nas = models.IntegerField(null=True, help_text='Delays and cancellations attributable to the national aviation system that refer to a broad set of conditions, such as non-extreme weather conditions, airport operations, heavy traffic volume, and air traffic control')
#     atraso_seguranca = models.IntegerField(null=True, help_text='Delays or cancellations caused by evacuation of a terminal or concourse')
#     atraso_aeronave = models.IntegerField(null=True, help_text='A previous flight with same aircraft arrived late')
#
#     class Meta:
#         db_table = 'aviacao"."voo'
