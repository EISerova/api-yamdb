
# YaMDb
<div id="badges">
  <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>  <img src="https://img.shields.io/badge/django-red?style=for-the-badge&logo=django&logoColor=white" alt="django Badge"/>
</div>

______________________________
#### ��������:
������� ������ ������, ����� �� � ������ ������������ ����� �������� ���� ������ � ������, �������, ������ � ������ ������. 
�������� �������, ���������� ������������, �������� ������ ������. ?
________________________

#### �������� �������� ������� �� ��� ���������� �������� �������������:
- [��������� �������](https://github.com/EISerova/),
- [���� �����������](https://github.com/Bakarasik),
- [��������� �������](https://github.com/Cognitoid).
__________________________

#### ������ ������� ������������:
* Python 3.8
* Django 2.2
* Django rest framework 3.12
* JWT 2.1

__________________________

#### ��� ��������� ������:
- ����������� �����������:\
```git clone https://github.com/EISerova/api_yamdb```\
```cd api_yamdb```

- ������� � ������������ ����������� ���������:\
```python -m venv env```\
```source env/bin/activate```

- ���������� ����������� �� ����� requirements.txt:\
```python -m pip install --upgrade pip```\
```pip install -r requirements.txt```

- ��������� ��������:\
```python manage.py migrate```

- ��������� ������:\
```python manage.py runserver```
______________________

#### ������ ������:
� ���� ������ ����� ������������� csv-�����:\
```python manage.py import_csv.py```
______________________

#### ����������� �������� �������:
�� [�������� � ������������� redoc](http://127.0.0.1:8000/redoc/) ����� ������������ � ��������� �������� � ������� �� ���.
______________________

#### ������� API-��������:
 ��������� ������ ���� ������������.
```mermaid
graph TD;
    A[GET] --> B(http://127.0.0.1:8000/api/v1/titles/)
    B --> C[Response]
    C --> E[id, name, year, raiting, description, genre, category]
```

�������� ����� ����� � ������������ � id 1.
```mermaid
graph TD;
A[POST] --> B(http://127.0.0.1:8000/api/v1/titles/1/reviews/)
B --> C[Response]
C --> D[id, text, author, score, pub_date]
```
______________________

#### ��� ����������� ������������ ����� �������������� ��������� ���� username � email �� [/auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/). ����� ����� �� �������� ������ � ����� ������������. 

����� ���������� ������� ����� ��� ��������������, ����������� ��� � ������� ��� ������ � username �� ������ [/auth/token/](http://127.0.0.1:8000/api/v1/auth/token/).
