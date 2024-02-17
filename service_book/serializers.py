from rest_framework import serializers
from .models import Machine, Maintenance, Claim


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = [
            'id',
            'number_machine',
            'model_equipment',
            'model_engine',
            'number_engine',
            'model_transmission',
            'number_transmission',
            'model_driving_axle',
            'number_driving_axle',
            'model_steering_axle',
            'number_steering_axle',
            'supply_contract',
            'shipment_date',
            'end_consumer',
            'shipping_address',
            'options',
            'client',
            'service_company'
        ]


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = [
            'id',
            'type',
            'maintenance_date',
            'operating_time',
            'order_number',
            'order_date',
            'maintenance_company',
            'machine',
            'service_company'
        ]


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = [
            'id',
            'refusal_date',
            'operating_time',
            'refusal_node',
            'refusal_description',
            'recovery_method',
            'repair_parts',
            'recovery_date',
            'downtime',
            'machine',
            'service_company'
        ]
