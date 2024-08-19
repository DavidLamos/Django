from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    SupplierMaster, PRMaster, RFQMaster,
    RFQSelectedSupplierHeader, PurchasingDocumentHeader, SchedulePOHeader
)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import date, timedelta
import json

@receiver(post_save, sender=SupplierMaster)
@receiver(post_delete, sender=SupplierMaster)
@receiver(post_save, sender=PRMaster)
@receiver(post_delete, sender=PRMaster)
@receiver(post_save, sender=RFQMaster)
@receiver(post_delete, sender=RFQMaster)
@receiver(post_save, sender=RFQSelectedSupplierHeader)
@receiver(post_delete, sender=RFQSelectedSupplierHeader)
@receiver(post_save, sender=PurchasingDocumentHeader)
@receiver(post_delete, sender=PurchasingDocumentHeader)
@receiver(post_save, sender=SchedulePOHeader)
@receiver(post_delete, sender=SchedulePOHeader)
def update_dashboard(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = 'dashboard_group'
    
    data = {
        'supplier_total': SupplierMaster.objects.count(),
        'pr_total': PRMaster.objects.count(),
        'rfq_total': RFQMaster.objects.count(),
        'negotiation_total': RFQSelectedSupplierHeader.objects.count(),
        'po_total': PurchasingDocumentHeader.objects.count(),
        'schedule_total': SchedulePOHeader.objects.count(),
        'registered_vendors': SupplierMaster.objects.filter(vendor_status='Registered').count(),
        'approved_vendors': SupplierMaster.objects.filter(vendor_status='Approved').count(),
        'rejected_vendors': SupplierMaster.objects.filter(vendor_status='Rejected').count(),
        'prs_week': PRMaster.objects.filter(PRDate__gte=date.today() - timedelta(weeks=1)).count(),
        'approved_prs_week': PRMaster.objects.filter(pr_status='Approved', PRDate__gte=date.today() - timedelta(weeks=1)).count(),
        'rfqs_week': RFQMaster.objects.filter(StartingDate__gte=date.today() - timedelta(weeks=1)).count(),
        'submitted_rfqs_week': RFQMaster.objects.filter(rfq_status='Submitted', StartingDate__gte=date.today() - timedelta(weeks=1)).count(),
        'negotiations_week': RFQSelectedSupplierHeader.objects.filter(supplier_approval_status='Negotiated', StartingDate__gte=date.today() - timedelta(weeks=1)).count(),
        'finalized_vendors_week': RFQSelectedSupplierHeader.objects.filter(supplier_approval_status='Finalized', StartingDate__gte=date.today() - timedelta(weeks=1)).count(),
        'pos_week': PurchasingDocumentHeader.objects.filter(PORaisedDate__gte=date.today() - timedelta(weeks=1)).count(),
        'acknowledged_pos_week': PurchasingDocumentHeader.objects.filter(po_status='Acknowledged', PORaisedDate__gte=date.today() - timedelta(weeks=1)).count(),
        'schedule_created_week': SchedulePOHeader.objects.filter(ScheduleDate__gte=date.today() - timedelta(weeks=1)).count(),
        'schedule_accepted_week': SchedulePOHeader.objects.filter(schedule_status='Accepted', ScheduleDate__gte=date.today() - timedelta(weeks=1)).count(),
    }
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_dashboard_data',
            'data': json.dumps(data)
        }
    )
