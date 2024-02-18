from django import forms
from django.core.exceptions import ValidationError

from .models import Machine, Maintenance, Claim, Client, ServiceCompany


class MachineForm(forms.ModelForm):
    shipment_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        label='Дата отгрузки с завода'
    )

    class Meta:
        model = Machine
        fields = [
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

        labels = {
            'number_machine': 'Заводской номер машины',
            'model_equipment': 'Модель техники',
            'model_engine': 'Модель двигателя',
            'number_engine': 'Заводской номер двигателя',
            'model_transmission': 'Модель трансмиссии',
            'number_transmission': 'Заводской номер трансмиссии',
            'model_driving_axle': 'Модель ведущего моста',
            'number_driving_axle': 'Заводской номер ведущего моста',
            'model_steering_axle': 'Модель управляемого моста',
            'number_steering_axle': 'Заводской номер управляемого моста',
            'supply_contract': 'Договор поставки (номер, дата)',
            'shipment_date': 'Дата отгрузки с завода',
            'end_consumer': 'Грузополучатель (конечный потребитель)',
            'shipping_address': 'Адрес поставки (эксплуатации)',
            'options': 'Комплектация (дополнительные опции)',
            'client': 'Клиент',
            'service_company': 'Сервисная компания'
        }


# Форма записи о ТО
class MaintenanceForm(forms.ModelForm):
    maintenance_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Указываем ожидаемый формат даты
        label='Дата проведения ТО'
    )
    order_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Указываем ожидаемый формат даты
        label='Дата заказ-наряда'
    )

    class Meta:
        model = Maintenance
        fields = [
            'machine',
            'type',
            'maintenance_date',
            'operating_time',
            'order_number',
            'order_date',
            'maintenance_company',
        ]
        labels = {
            'machine': 'Машина',
            'type': 'Вид ТО',
            'maintenance_date': 'Дата проведения ТО',
            'operating_time': 'Наработка, м/час',
            'order_number': 'Номер заказ-наряда',
            'order_date': 'Дата заказ-наряда',
            'maintenance_company': 'Организация, проводившая ТО',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs['initial']['user']
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user in users_clients:
            self.fields['machine'] = forms.ModelChoiceField(
                queryset=Machine.objects.filter(client__user_link=user)
            )
        elif user in users_companies:
            self.fields['machine'] = forms.ModelChoiceField(
                queryset=Machine.objects.filter(service_company__user_link=user)
            )

    def clean(self):
        cleaned_data = super().clean()
        operating_time = cleaned_data.get("operating_time")
        if operating_time < 0:
            raise ValidationError({
                "operating_time": "Наработка не может быть отрицательной"
            })

        maintenance_date = cleaned_data.get('maintenance_date')
        order_date = cleaned_data.get('order_date')

        if maintenance_date and order_date and order_date > maintenance_date:
            raise ValidationError({
                "order_date": "Дата заказ-наряда не может быть больше даты проведения ТО"
            })
        return cleaned_data


# Форма записи о рекламации
class ClaimForm(forms.ModelForm):
    recovery_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Указываем ожидаемый формат даты
        label='Дата восстановления'
    )
    refusal_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Указываем ожидаемый формат даты
        label='Дата отказа'
    )

    class Meta:
        model = Claim
        fields = [
            'machine',
            'refusal_date',
            'operating_time',
            'refusal_node',
            'refusal_description',
            'recovery_method',
            'repair_parts',
            'recovery_date',
        ]

        labels = {
            'machine': 'Машина',
            'refusal_date': 'Дата отказа',
            'operating_time': 'Наработка, м/час',
            'refusal_node': 'Узел отказа',
            'refusal_description': 'Описание отказа',
            'recovery_method': 'Способ восстановления',
            'repair_parts': 'Используемые запасные части',
            'recovery_date': 'Дата восстановления',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs['initial']['user']
        companies = ServiceCompany.objects.all()
        users_companies = []
        for company in companies:
            users_companies.append(company.user_link)
        if user in users_companies:
            # Если сервисная компания - доступны только ее машины
            self.fields['machine'] = forms.ModelChoiceField(
                queryset=Machine.objects.filter(service_company__user_link=user)
            )

    def clean(self):
        cleaned_data = super().clean()
        refusal_date = cleaned_data.get("refusal_date")
        recovery_date = cleaned_data.get("recovery_date")
        operating_time = cleaned_data.get("operating_time")
        if self.is_valid():
            if recovery_date < refusal_date:
                raise ValidationError({
                    "recovery_date": "Дата восстановления должна быть не раньше даты отказа"
                })
            # Проверка корректности наработки
            if operating_time < 0:
                raise ValidationError({
                    "operating_time": "Наработка должна быть положительным числом"
                })
        return cleaned_data
