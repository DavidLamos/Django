from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    SupplierMaster, PRMaster, RFQMaster,
    RFQSelectedSupplierHeader, PurchasingDocumentHeader, SchedulePOHeader
)
from datetime import datetime, timedelta
from django.db.models import Count, Q

@api_view(['GET'])
def dashboardData(request):
    filter_param = request.GET.get('filter', 'week')
    now = datetime.now()
    start_date = None
    end_date = now

    # Determine the date range based on the filter parameter
    if filter_param == 'week':
        start_date = now - timedelta(weeks=1)
    elif filter_param == 'month':
        start_date = now - timedelta(days=30)  # Using days instead of weeks for month
    elif filter_param == 'year':
        start_date = now - timedelta(days=365)  # Using days instead of weeks for year

    # Retrieve and aggregate data
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

    # Additional aggregated data
    registered_vendors = SupplierMaster.objects.filter(vendor_status='Registered').count()
    approved_vendors = SupplierMaster.objects.filter(vendor_status='Approved').count()
    rejected_vendors = SupplierMaster.objects.filter(vendor_status='Rejected').count()
    prs_week = PRMaster.objects.filter(PRDate__gte=datetime.today() - timedelta(weeks=1)).count()
    approved_prs_week = PRMaster.objects.filter(pr_status='Approved', PRDate__gte=datetime.today() - timedelta(weeks=1)).count()
    rfqs_week = RFQMaster.objects.filter(StartingDate__gte=datetime.today() - timedelta(weeks=1)).count()
    submitted_rfqs_week = RFQMaster.objects.filter(rfq_status='Submitted', StartingDate__gte=datetime.today() - timedelta(weeks=1)).count()
    negotiations_week = RFQSelectedSupplierHeader.objects.filter(supplier_approval_status='Negotiated', StartingDate__gte=datetime.today() - timedelta(weeks=1)).count()
    finalized_vendors_week = RFQSelectedSupplierHeader.objects.filter(supplier_approval_status='Finalized', StartingDate__gte=datetime.today() - timedelta(weeks=1)).count()
    pos_week = PurchasingDocumentHeader.objects.filter(PORaisedDate__gte=datetime.today() - timedelta(weeks=1)).count()
    acknowledged_pos_week = PurchasingDocumentHeader.objects.filter(po_status='Acknowledged', PORaisedDate__gte=datetime.today() - timedelta(weeks=1)).count()
    schedule_created_week = SchedulePOHeader.objects.filter(ScheduleDate__gte=datetime.today() - timedelta(weeks=1)).count()
    schedule_accepted_week = SchedulePOHeader.objects.filter(schedule_status='Accepted', ScheduleDate__gte=datetime.today() - timedelta(weeks=1)).count()

    # Process and format data for frontend
    formatted_data = {
        'supplier_total': supplier_total,
        'pr_total': pr_total,
        'rfq_total': rfq_total,
        'negotiation_total': negotiation_total,
        'po_total': po_total,
        'schedule_total': schedule_total,
        'registered_vendors': registered_vendors,
        'approved_vendors': approved_vendors,
        'rejected_vendors': rejected_vendors,
        'prs_week': prs_week,
        'approved_prs_week': approved_prs_week,
        'rfqs_week': rfqs_week,
        'submitted_rfqs_week': submitted_rfqs_week,
        'negotiations_week': negotiations_week,
        'finalized_vendors_week': finalized_vendors_week,
        'pos_week': pos_week,
        'acknowledged_pos_week': acknowledged_pos_week,
        'schedule_created_week': schedule_created_week,
        'schedule_accepted_week': schedule_accepted_week,
        'filtered_data': {
            'supplier': {data['vendor_status']: data['count'] for data in supplier_data},
            'pr': {data['pr_status']: data['count'] for data in pr_data},
            'rfq': {data['rfq_status']: data['count'] for data in rfq_data},
            'negotiation': {data['supplier_approval_status']: data['count'] for data in negotiation_data},
            'po': {data['po_status']: data['count'] for data in po_data},
            'schedule': {data['schedule_status']: data['count'] for data in schedule_data},
        }
    }

    return Response(formatted_data)
