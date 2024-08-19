# myapp/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import (
    SupplierMaster, PRMaster, RFQMaster,
    RFQSelectedSupplierHeader, PurchasingDocumentHeader, SchedulePOHeader
)
from datetime import datetime, timedelta
from django.db.models import Count

class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Optionally add authentication checks
        await self.send_dashboard_data()

    async def send_dashboard_data(self):
        now = datetime.now()
        start_date = now - timedelta(weeks=1)
        end_date = now

        supplier_total = SupplierMaster.objects.count()
        pr_total = PRMaster.objects.count()
        rfq_total = RFQMaster.objects.count()
        negotiation_total = RFQSelectedSupplierHeader.objects.count()
        po_total = PurchasingDocumentHeader.objects.count()
        schedule_total = SchedulePOHeader.objects.count()

        supplier_data = SupplierMaster.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('vendor_status').annotate(count=Count('id'))

        pr_data = PRMaster.objects.filter(
            PRDate__range=(start_date, end_date)
        ).values('pr_status').annotate(count=Count('id'))

        rfq_data = RFQMaster.objects.filter(
            StartingDate__range=(start_date, end_date)
        ).values('rfq_status').annotate(count=Count('id'))

        negotiation_data = RFQSelectedSupplierHeader.objects.filter(
            StartingDate__range=(start_date, end_date)
        ).values('supplier_approval_status').annotate(count=Count('id'))

        po_data = PurchasingDocumentHeader.objects.filter(
            PORaisedDate__range=(start_date, end_date)
        ).values('po_status').annotate(count=Count('id'))

        schedule_data = SchedulePOHeader.objects.filter(
            ScheduleDate__range=(start_date, end_date)
        ).values('schedule_status').annotate(count=Count('id'))

        formatted_data = {
            'supplier_total': supplier_total,
            'pr_total': pr_total,
            'rfq_total': rfq_total,
            'negotiation_total': negotiation_total,
            'po_total': po_total,
            'schedule_total': schedule_total,
            'filtered_data': {
                'supplier': {data['vendor_status']: data['count'] for data in supplier_data},
                'pr': {data['pr_status']: data['count'] for data in pr_data},
                'rfq': {data['rfq_status']: data['count'] for data in rfq_data},
                'negotiation': {data['supplier_approval_status']: data['count'] for data in negotiation_data},
                'po': {data['po_status']: data['count'] for data in po_data},
                'schedule': {data['schedule_status']: data['count'] for data in schedule_data},
            }
        }
        await self.send_json(formatted_data)
    
    async def receive_json(self, content):
        # Handle incoming messages from the WebSocket here
        # For instance, update the data based on filters
        await self.send_dashboard_data()

    async def disconnect(self, close_code):
        # Handle disconnection logic here
        pass
