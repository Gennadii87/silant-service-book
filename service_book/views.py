from rest_framework import viewsets
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import (
    Machine, Maintenance, Claim, Client, ServiceCompany, Equipment, Engine, Transmission, DrivingAxle, SteeringAxle,
    MaintenanceCompany, TypeMaintenance, RefusalNode, RecoveryMethod
)
from .filters import MachineFilter, MaintenanceFilter, ClaimFilter, MachinePreviewFilter
from .forms import MachineForm, MaintenanceForm, ClaimForm
from .serializers import MachineSerializer, MaintenanceSerializer, ClaimSerializer
from .permissions import IsAdminOrManager, IsAdminOrManagerOrClientOrServiceCompany


# Вывод списка машин
class MachineList(ListView):
    model = Machine
    ordering = 'shipment_date'
    template_name = 'machines.html'
    context_object_name = 'machines'
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:

            clients = Client.objects.all()
            companies = ServiceCompany.objects.all()
            users_clients = []
            users_companies = []
            queryset = Machine.objects.none()
            for client in clients:
                users_clients.append(client.user_link)
            for company in companies:
                users_companies.append(company.user_link)
            if user.is_superuser == 1 or user.is_staff == 1:
                queryset = super().get_queryset()
            elif user in users_clients:
                queryset = Machine.objects.filter(client__user_link=user).order_by('shipment_date')
            elif user in users_companies:
                queryset = Machine.objects.filter(service_company__user_link=user).order_by('shipment_date')
            self.filter_set = MachineFilter(self.request.GET, queryset)
        else:
            queryset = super().get_queryset()
            number_machine_param = self.request.GET.get('number_machine', '')
            if number_machine_param != '':
                queryset = queryset.filter(number_machine=number_machine_param)
            self.filter_set = MachinePreviewFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


# Подробности по каждой машине
class MachineDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_machine'
    model = Machine
    template_name = 'machine.html'
    context_object_name = 'machine'

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Machine.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Machine.objects.filter(client__user_link=user)
        elif user in users_companies:
            queryset = Machine.objects.filter(service_company__user_link=user)
        return queryset


# Создание записи о новой машине с проверкой прав
class MachineCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'service_book.add_machine'
    form_class = MachineForm
    model = Machine
    template_name = 'machine_edit.html'
    success_url = reverse_lazy('machine_list')


# Редактирование записи о машине с проверкой прав
class MachineEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'service_book.change_machine'
    form_class = MachineForm
    model = Machine
    template_name = 'machine_edit.html'
    success_url = reverse_lazy('machine_list')


# Удаление записи о машине с проверкой прав
class MachineDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'service_book.delete_machine'
    model = Machine
    template_name = 'machine_delete.html'
    success_url = reverse_lazy('machine_list')


# Вывод списка ТО с проверкой прав
class MaintenanceList(PermissionRequiredMixin, ListView):
    permission_required = 'service_book.view_maintenance'
    model = Maintenance
    ordering = 'maintenance_date'
    template_name = 'maintenances.html'
    context_object_name = 'maintenances'
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Maintenance.objects.filter(machine__client__user_link=user).order_by('maintenance_date')
        elif user in users_companies:
            queryset = Maintenance.objects.filter(service_company__user_link=user).order_by('maintenance_date')
        self.filter_set = MaintenanceFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


# Подробности по каждому ТО с проверкой прав
class MaintenanceDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_maintenance'
    model = Maintenance
    template_name = 'maintenance.html'
    context_object_name = 'maintenance'

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Maintenance.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            queryset = Maintenance.objects.filter(service_company__user_link=user)
        return queryset


# Создание записи о новом ТО с проверкой прав
class MaintenanceCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'service_book.add_maintenance'
    form_class = MaintenanceForm
    model = Maintenance
    template_name = 'maintenance_edit.html'
    success_url = reverse_lazy('maintenance_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Редактирование записи о ТО с проверкой прав
class MaintenanceEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'service_book.change_maintenance'
    form_class = MaintenanceForm
    model = Maintenance
    template_name = 'maintenance_edit.html'
    success_url = reverse_lazy('maintenance_list')

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Maintenance.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            queryset = Maintenance.objects.filter(service_company__user_link=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Удаление записи о ТО с проверкой прав
class MaintenanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'service_book.delete_maintenance'
    model = Maintenance
    template_name = 'maintenance_delete.html'
    success_url = reverse_lazy('maintenance_list')

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Maintenance.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            queryset = Maintenance.objects.filter(service_company__user_link=user)
        return queryset


# Вывод списка рекламаций с проверкой прав
class ClaimList(PermissionRequiredMixin, ListView):
    permission_required = 'service_book.view_claim'
    model = Claim
    ordering = 'refusal_date'
    template_name = 'claims.html'
    context_object_name = 'claims'
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Claim.objects.filter(machine__client__user_link=user).order_by('refusal_date')
        elif user in users_companies:
            queryset = Claim.objects.filter(service_company__user_link=user).order_by('refusal_date')
        self.filter_set = ClaimFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


# Подробности по каждой рекламации
class ClaimDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_claim'
    model = Claim
    template_name = 'claim.html'
    context_object_name = 'claim'

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Claim.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            queryset = Claim.objects.filter(service_company__user_link=user)
        return queryset


# Создание записи о новой рекламации с проверкой прав
class ClaimCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'service_book.add_claim'
    form_class = ClaimForm
    model = Claim
    template_name = 'claim_edit.html'
    success_url = reverse_lazy('claim_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Редактирование записи о рекламации с проверкой прав
class ClaimEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'service_book.change_claim'
    form_class = ClaimForm
    model = Claim
    template_name = 'claim_edit.html'
    success_url = reverse_lazy('claim_list')

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Claim.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            queryset = Claim.objects.filter(service_company__user_link=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


# Удаление записи о рекламации с проверкой прав
class ClaimDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'service_book.delete_claim'
    model = Claim
    template_name = 'claim_delete.html'
    success_url = reverse_lazy('claim_list')

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Claim.objects.filter(machine__client__user_link=user)
        elif user in users_companies:
            queryset = Claim.objects.filter(service_company__user_link=user)
        return queryset


# Справочное описание модели техники
class EquipmentDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_equipment'
    model = Equipment
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание модели двигателя
class EngineDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_engine'
    model = Engine
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание модели трансмиссии
class TransmissionDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_transmission'
    model = Transmission
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание модели ведущего моста
class DrivingAxleDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_drivingaxle'
    model = DrivingAxle
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание модели управляемого моста
class SteeringAxleDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_steeringaxle'
    model = SteeringAxle
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание клиента
class ClientDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_steeringaxle'
    model = Client
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание сервисной компании
class ServiceCompanyDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_servicecompany'
    model = ServiceCompany
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание организации, проводившей ТО
class MaintenanceCompanyDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_maintenancecompany'
    model = MaintenanceCompany
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание типа ТО
class TypeMaintenanceDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_typemaintenance'
    model = TypeMaintenance
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание узла отказа
class RefusalNodeDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_refusalnode'
    model = RefusalNode
    template_name = 'reference.html'
    context_object_name = 'reference'


# Справочное описание способа восстановления
class RecoveryMethodDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'service_book.view_recoverymethod'
    model = RecoveryMethod
    template_name = 'reference.html'
    context_object_name = 'reference'


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            clients = Client.objects.all()
            companies = ServiceCompany.objects.all()
            users_clients = []
            users_companies = []
            queryset = Machine.objects.none()
            for client in clients:
                users_clients.append(client.user_link)
            for company in companies:
                users_companies.append(company.user_link)
            if user.is_superuser == 1 or user.is_staff == 1:
                queryset = super().get_queryset()
            elif user in users_clients:
                queryset = Machine.objects.filter(client__user_link=user).order_by('shipment_date')
            elif user in users_companies:
                queryset = Machine.objects.filter(service_company__user_link=user).order_by('shipment_date')
            self.filter_set = MachineFilter(self.request.GET, queryset)
        else:
            if not self.request.GET.__contains__('number_machine'):
                super().get_queryset()
                queryset = Machine.objects.none()
            else:
                if self.request.GET.get('number_machine') != '':
                    queryset = super().get_queryset()
                else:
                    super().get_queryset()
                    queryset = Machine.objects.none()
            self.filter_set = MachinePreviewFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrManagerOrClientOrServiceCompany()]
        else:
            return [IsAdminOrManager()]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Maintenance.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Maintenance.objects.filter(machine__client__user_link=user).order_by('maintenance_date')
        elif user in users_companies:
            queryset = Maintenance.objects.filter(service_company__user_link=user).order_by('maintenance_date')
        self.filter_set = MaintenanceFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrManagerOrClientOrServiceCompany()]
        else:
            return [IsAdminOrManager()]


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        clients = Client.objects.all()
        companies = ServiceCompany.objects.all()
        users_clients = []
        users_companies = []
        queryset = Claim.objects.none()
        for client in clients:
            users_clients.append(client.user_link)
        for company in companies:
            users_companies.append(company.user_link)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_clients:
            queryset = Claim.objects.filter(machine__client__user_link=user).order_by('refusal_date')
        elif user in users_companies:
            queryset = Claim.objects.filter(service_company__user_link=user).order_by('refusal_date')
        self.filter_set = ClaimFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrManagerOrClientOrServiceCompany()]
        else:
            return [IsAdminOrManager()]
