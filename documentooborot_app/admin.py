from django.contrib import admin
from .models import Department, Employee, Documents, Trud


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id_department', 'department_name')
    search_fields = ('id_department','department_name')


class EmployeeAdmin(admin.ModelAdmin):
    list_display=('id_employee', 'first_name', 'last_name', 'patronymic', 'date_birth',
                  'id_passport', 'gender', 'phone_number', 'date_employment','date_dismissal',
                  'position', 'id_department','id_doc')
    search_fields=('id_doc__doc_name','id_department__department_name')

    

class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id_doc', 'doc_name', 'doc_type','doc_description','doc_date')
    search_fields=('id_doc','doc_name','doc_type','doc_date')
    

class OrderAdmin(admin.ModelAdmin):
    def my_Department(self, obj):
        return f'{obj.id_department.department_name}'
    
    def my_Employee(self, obj):
        return f'{obj.employee.id_employee} {obj.employee.last_name}'
    
    def my_Documents(self, obj):
        return f'{obj.documents.id_doc} {obj.documents.doc_name}'
    def my_phone(self, obj):
        return f'{obj.phophone_number}'

    my_Employee.short_description = 'Сотрудник'
    my_phone.short_description = 'Телефон'
    my_Documents.short_description = 'Документ'
    my_Department.short_description = 'Подразделение'

    list_display = ('id_order', 'order_status', 'id_employee',
                    'id_department','my_Department')
    search_fields=('id_employee__id_employee','id_employee__second_name','id_department__department_name','id_department__id_department')
    raw_id_fields=('id_employee','id_department')
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(Trud, OrderAdmin)