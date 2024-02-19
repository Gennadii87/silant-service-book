from django.urls import path, include
from rest_framework.routers import DefaultRouter
from allauth.account.views import LoginView, PasswordResetView
from .views import *


router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='machines')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'claims', ClaimViewSet, basename='claims')


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', MachineList.as_view(), name='machine_list'),
    path('machines/<int:pk>', MachineDetail.as_view(), name='machine_detail'),
    path('machines/create/', MachineCreate.as_view(), name='maсhine_create'),
    path('machines/<int:pk>/edit/', MachineEdit.as_view(), name='machine_edit'),
    path('machines/<int:pk>/delete/', MachineDelete.as_view(), name='machine_delete'),
    path('maintenances/', MaintenanceList.as_view(), name='maintenance_list'),
    path('maintenances/<int:pk>', MaintenanceDetail.as_view(), name='maintenance_detail'),
    path('maintenances/create/', MaintenanceCreate.as_view(), name='maintenance_create'),
    path('maintenances/<int:pk>/edit/', MaintenanceEdit.as_view(), name='maintenance_edit'),
    path('maintenances/<int:pk>/delete/', MaintenanceDelete.as_view(), name='maintenance_delete'),
    path('claims/', ClaimList.as_view(), name='claim_list'),
    path('claims/<int:pk>', ClaimDetail.as_view(), name='claim_detail'),
    path('claims/create/', ClaimCreate.as_view(), name='claim_create'),
    path('claims/<int:pk>/edit/', ClaimEdit.as_view(), name='claim_edit'),
    path('claims/<int:pk>/delete/', ClaimDelete.as_view(), name='claim_delete'),
    path('equipments/<int:pk>', EquipmentDetail.as_view(), name='equipment_detail'),
    path('engines/<int:pk>', EngineDetail.as_view(), name='engine_detail'),
    path('transmissions/<int:pk>', TransmissionDetail.as_view(), name='transmission_detail'),
    path('drivingaxles/<int:pk>', DrivingAxleDetail.as_view(), name='drivingaxle_detail'),
    path('sreeringaxles/<int:pk>', SteeringAxleDetail.as_view(), name='steeringaxle_detail'),
    path('clients/<int:pk>', ClientDetail.as_view(), name='client_detail'),
    path('servicecompanies/<int:pk>', ServiceCompanyDetail.as_view(), name='servicecompany_detail'),
    path('maintenancecompanies/<int:pk>', MaintenanceCompanyDetail.as_view(), name='maintenancecompany_detail'),
    path('typesmaintenance/<int:pk>', TypeMaintenanceDetail.as_view(), name='typemaintenance_detail'),
    path('refusalnodes/<int:pk>', RefusalNodeDetail.as_view(), name='refusalnode_detail'),
    path('recoverymethods/<int:pk>', RecoveryMethodDetail.as_view(), name='recoverymethod_detail'),
]
