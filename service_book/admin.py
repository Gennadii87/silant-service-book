from django.contrib import admin

from .models import (
    Equipment, Engine, Transmission, DrivingAxle, SteeringAxle, Client, ServiceCompany, MaintenanceCompany,
    TypeMaintenance, RefusalNode, RecoveryMethod, Machine, Maintenance, Claim, MaintenanceAdmin, ClaimAdmin
)

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from .forms import FlatPageForm


# поля для Equipment
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для Engine
class EngineAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для Transmission
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для DrivingAxle
class DrivingAxleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для SteeringAxle
class SteeringAxleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для Client
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user_link')


# поля для ServiceCompany
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user_link')


# поля для MaintenanceCompany
class MaintenanceCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для TypeMaintenance
class TypeMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для RefusalNode
class RefusalNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для RecoveryMethod
class RecoveryMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# поля для Machine
class MachineAdmin(admin.ModelAdmin):
    list_display = ('number_machine', 'model_equipment', 'model_engine', 'number_engine', 'model_transmission',
                    'number_transmission', 'model_driving_axle', 'number_driving_axle', 'model_steering_axle',
                    'number_steering_axle', 'supply_contract', 'shipment_date', 'end_consumer', 'shipping_address',
                    'options', 'client', 'service_company')


class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(DrivingAxle, DrivingAxleAdmin)
admin.site.register(SteeringAxle, SteeringAxleAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ServiceCompany, ServiceCompanyAdmin)
admin.site.register(MaintenanceCompany, MaintenanceCompanyAdmin)
admin.site.register(TypeMaintenance, TypeMaintenanceAdmin)
admin.site.register(RefusalNode, RefusalNodeAdmin)
admin.site.register(RecoveryMethod, RecoveryMethodAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Claim, ClaimAdmin)
