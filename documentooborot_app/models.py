from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
import re 
from datetime import datetime

class Department(models.Model):
    class Meta:
        db_table = "department"
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    id_department = models.IntegerField(primary_key=True, verbose_name="ID подразделения")
    department_name = models.TextField(verbose_name="Наименование подразделения")

    def __str__(self) -> str: 
        return f'{self.id_department} {self.department_name}'


def validate_phone_number(phone_number):
    reg_pattern = re.compile(r"(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$")
    if not reg_pattern.match(phone_number):
        raise ValidationError(
            gettext_lazy('%(phone_number)s некорректный номер'),
            params={'phone_number': phone_number}
        )

class Documents(models.Model):
    class Meta:
        db_table="documents"
        verbose_name="Документы"
        verbose_name_plural="Документы"

    id_doc=models.IntegerField(primary_key=True, verbose_name="ID документа")
    doc_name=models.TextField(verbose_name="Наименование документа")
    doc_type=models.TextField(verbose_name="Тип документа")
    doc_description=models.TextField(verbose_name='Краткое описание',blank=True,null=True)
    doc_date=models.DateField(verbose_name="Дата создания документа")

    def __str__(self) -> str:  
        return f'''{self.id_doc} {self.doc_name} {self.doc_type} {self.doc_description} {self.doc_date}'''
        
class Employee(models.Model):
    class Meta:
        db_table = "employee"
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"

    Genders = (
        ('M', 'Мужской'),
        ('F', 'Женский')
    )

    id_employee = models.IntegerField(primary_key=True, verbose_name="ID сотрудника")
    first_name = models.TextField(verbose_name="Имя")
    last_name = models.TextField(verbose_name="Фамилия")
    patronymic = models.TextField(verbose_name="Отчество", blank=True, null=True)
    date_birth = models.DateField(verbose_name="Дата рождения")
    id_passport = models.IntegerField(verbose_name="Номер и серия паспорта", blank=True, null=True)
    gender = models.CharField(verbose_name="Пол", choices=Genders, max_length=1) 
    phone_number = models.TextField(verbose_name="Номер телефона", validators=[validate_phone_number])
    date_employment = models.DateField(verbose_name="Дата принятия на работу")
    date_dismissal = models.DateField(verbose_name="Дата увольнения", blank=True, null=True)
    position = models.TextField(verbose_name="Должность")
    id_department = models.ForeignKey(Department, on_delete=models.RESTRICT, verbose_name="Подразделение", blank=True, null=True)
    id_doc = models.ForeignKey(Documents, on_delete=models.RESTRICT, verbose_name='ID документа', blank=True, null=True)

    def __str__(self) -> str:  
        return f'''{self.id_employee} {self.first_name} {self.last_name} {self.patronymic} {self.date_birth} {self.id_passport}
        {self.gender} {self.phone_number} {self.date_employment} {self.date_dismissal} {self.position} {self.id_department}'''

def status_validator(order_status):
    if order_status not in ["open", "closed", "in progress", "need info"]:
        raise ValidationError(
            gettext_lazy('%(order_status)s is wrong order status'),
            params={'order_status': order_status},
        )

class Trud(models.Model):
    class Meta:
        db_table="trud"
        verbose_name="Трудоустройство"
        verbose_name_plural="Трудоустройство"

    id_order=models.IntegerField(primary_key=True, verbose_name="ID заявки")
    order_status=models.TextField(verbose_name="Статус заявки")
    id_employee=models.ForeignKey(Employee, verbose_name="ID Сотрудника",on_delete=models.RESTRICT)
    id_department=models.ForeignKey(Department, verbose_name="ID Подразделения", on_delete=models.RESTRICT)

def save(self, *args, **kwargs):
    self.last_updated_dt = datetime.now()
    super().save(*args, **kwargs)