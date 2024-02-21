import django_filters
from django_filters import FilterSet, ModelChoiceFilter
from .models import *


class MachineFilter(FilterSet):
    model_equipment = ModelChoiceFilter(
        field_name='model_equipment__title',
        queryset=Equipment.objects.all(),
        label='Модель техники',
    )

    model_engine = ModelChoiceFilter(
        field_name='model_engine__title',
        queryset=Engine.objects.all(),
        label='Модель двигателя',
    )

    model_transmission = ModelChoiceFilter(
        field_name='model_transmission__title',
        queryset=Transmission.objects.all(),
        label='Модель трансмиссии',
    )

    model_driving_axle = ModelChoiceFilter(
        field_name='model_driving_axle__title',
        queryset=DrivingAxle.objects.all(),
        label='Модель вед. моста',
    )

    model_steering_axle = ModelChoiceFilter(
        field_name='model_steering_axle__title',
        queryset=SteeringAxle.objects.all(),
        label='Модель упр. моста',
    )


class MachinePreviewFilter(FilterSet):
    number_machine = django_filters.CharFilter(
        field_name='number_machine',
        lookup_expr='icontains',
        label='Заводской № машины',
    )


class MaintenanceFilter(FilterSet):
    type = ModelChoiceFilter(
        field_name='type__title',
        queryset=TypeMaintenance.objects.all(),
        label='Вид ТО',
    )

    machine = django_filters.CharFilter(
        field_name='machine__number_machine',
        lookup_expr='icontains',
        label='Заводской № машины',
    )

    service_company = ModelChoiceFilter(
        field_name='service_company__title',
        queryset=ServiceCompany.objects.all(),
        label='Сервисная компания',
    )


class ClaimFilter(FilterSet):
    refusal_node = ModelChoiceFilter(
        field_name='refusal_node__title',
        queryset=RefusalNode.objects.all(),
        label='Узел отказа',
    )

    recovery_method = ModelChoiceFilter(
        field_name='recovery_method__title',
        queryset=RecoveryMethod.objects.all(),
        label='Способ восстановления',
    )

    service_company = ModelChoiceFilter(
        field_name='service_company__title',
        queryset=ServiceCompany.objects.all(),
        label='Сервисная компания',
    )
