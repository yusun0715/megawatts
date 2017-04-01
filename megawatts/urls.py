# -*- coding: utf-8 -*-
from rest_framework import routers

from megawatts.views.site import Site
from megawatts.views.summary import Summary
from megawatts.views.summary_average import SummaryAverage

v1_router_mega = routers.SimpleRouter()
v1_router_mega.register(r'sites', Site, base_name='sites')
v1_router_mega.register(r'summary', Summary, base_name='summary')
v1_router_mega.register(r'summary-average', SummaryAverage, base_name='summary-average')
v1_router_mega_slashless = routers.DefaultRouter(trailing_slash=False)
v1_router_mega_slashless.registry = v1_router_mega.registry[:]
