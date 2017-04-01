# -*- coding: utf-8 -*-
from megawatts.storage import MegaSiteDetailDjangoStorage, MegaSiteDjangoStorage
from megawatts.logic import MegaSiteLogic


_site_storage = MegaSiteDjangoStorage()
_site_detail_storage = MegaSiteDetailDjangoStorage()

site_logic = MegaSiteLogic(
    site_storage=_site_storage,
    site_detail_storage=_site_detail_storage
)