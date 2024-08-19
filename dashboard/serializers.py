from rest_framework import serializers
from .models import SupplierMaster, PRMaster, RFQMaster, RFQSelectedSupplierHeader, PurchasingDocumentHeader, SchedulePOHeader

class SupplierMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierMaster
        fields = ['vendor_status']

class PRMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRMaster
        fields = ['pr_status', 'PRDate']

class RFQMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQMaster
        fields = ['rfq_status', 'StartingDate']

class RFQSelectedSupplierHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQSelectedSupplierHeader
        fields = ['supplier_approval_status', 'StartingDate']

class PurchasingDocumentHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasingDocumentHeader
        fields = ['po_status', 'PORaisedDate']

class SchedulePOHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulePOHeader
        fields = ['schedule_status', 'ScheduleDate']
