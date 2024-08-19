from django.contrib import admin
from .models import SupplierMaster, PRMaster, RFQMaster, RFQSelectedSupplierHeader, PurchasingDocumentHeader, SchedulePOHeader

admin.site.register(SupplierMaster)
admin.site.register(PRMaster)
admin.site.register(RFQMaster)
admin.site.register(RFQSelectedSupplierHeader)
admin.site.register(PurchasingDocumentHeader)
admin.site.register(SchedulePOHeader)
