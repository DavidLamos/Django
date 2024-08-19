from django.db import models

class SupplierMaster(models.Model):
    vendor_status = models.CharField(max_length=50, default='Registered')

class PRMaster(models.Model):
    pr_status = models.CharField(max_length=50, default='Raised')
    PRDate = models.DateField(blank=True, null=True)

class RFQMaster(models.Model):
    rfq_status = models.CharField(max_length=100, default='Pending')
    StartingDate = models.DateField()

class RFQSelectedSupplierHeader(models.Model):
    supplier_approval_status = models.CharField(max_length=100, default='Approval Pending')
    StartingDate = models.DateField(blank=True, null=True)

class PurchasingDocumentHeader(models.Model):
    po_status = models.CharField(max_length=100, default='PO Created')
    PORaisedDate = models.DateField(blank=True, null=True)

class SchedulePOHeader(models.Model):
    schedule_status = models.CharField(max_length=50, default='Schedule Created')
    ScheduleDate = models.DateField()
