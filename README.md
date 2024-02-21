# Проект сервисной кникги дя комании "Силант"
<h4>Сервис предназначен для ведения технического сотояния техники, о проведенных ремонтах и техническом обслуживании</h4>

<h2>Функционал сервиса</h2>

<h3>Роли</h3>

| **Роль**        | **Доступ к данным машин**                   | **Доступ к списку машин**                        |
|-----------------|---------------------------------------------|--------------------------------------------------|
| Клиент          | Имеет доступ к данным определённых машин    | У каждой машины есть только один клиент          |
| Сервисная орг.  | Доступ к данным определённых машин          | У каждой машины только одна сервисная организация|
| Менеджер        | Доступ ко всем данным машин                 | Доступ ко всем машинам и редактированию данных   |

<h2>Преднастроенные роли</h2>
<br>
        Супер-юзер полный доступ {
            логин: admin
            пароль: admin
        }
        <br>
        Клиент ограниченный доступ согласно роли {
            логин: Петров-МНС77 (Пользователь компанни который преобрел технику)
            пароль: Silant1234
        }
        <br>
        Сервисная организация ограниченный доступ согласно роли {
            логин: Силант (Пользовател проводящий ТО)
            пароль: Silant1234
        }
        <br>
        Менеджер ограниченный доступ согласно роли {
            логин: Силант (Доступна вся текника и данные по ней, доступно редактирование)
            пароль: Silant1234
        }
<br>

![Не авторизованный пользователь](/images/imag_login.png)
<br>
<details>
<summary>Нажмите, что бы посотреть дополнительную информацию</summary>

*Не зарегистрированные пользователи могут просмтривать только список машин с ограниченным выводом информации (доступ только к полям пп.1-10)*
Сортировка данных в полях производиться по умолчанию по дате  

Пользователь без авторизации может получить ограниченную информацию о комплектации машины, введя её заводской номер.Данному типу пользователя доступно поле для ввода заводского номера машины и кнопка поиск. Кнопкой поиск можно отсортировать по заводскому номеру машины

![Не авторизованный пользователь](/images/imag_logout.png)
</details>

**самоястоятельная регистрация отключена**

*Авторизация проводиться по логину/паролю, которые назначаются администратором системы. Пользователь не может самостоятельно поменять логин и/или пароль.*
Для этого согда `ACCOUNT_ADAPTER` который управляеться `ACCOUNT_ALLOW_SIGNUPS` и взависимости от ``False`` или ``True`` можно запретить или разрешить регистрацию
<br>

<h3>Верстка</h3>

*Адаптив выполнен для всех разрешений начиная с 360px*

<h3>API</h3>

API доступно по по ссылке:<pre><code> `http://127.0.0.0:8007/api/` </code></pre> 

<h2>Запуск проекта</h2>

<div style='background-color:#163E6C'>

**Склонируйте репозиторий командой:** <pre><code> `git clone https://github.com/Gennadii87/silant-service-book.git` </code></pre> 

**Создайте виртуальное окружение:** <pre><code>`python -m venv`</code></pre> 

**Установите все зависимости:** <pre><code>`pip install -r .\requirements.txt`</code></pre> 

**Запуск сервера:** <pre><code>`python manage.py runserver 8000`</code></pre> 
</div>

<h2>Дополнительно</h2>

**Дополнительно в проекте реализовано приложене для отправки запроса на ввостановление пароля пользователя**

Отправка запроса происходит при вводе адреса почты, если данный арес зарегестрирован, то запрос будет успешно отправлени прямо в админ-панель администратора

*Приложение `password_reset_notification`, открытое API для этого приложения `http://127.0.0.1:8000/accounts/password/reset/api/`*

<h4>Уведомление реализовано через собвсенный слой:</h4>

<pre><code> MIDDLEWARE = ['password_reset_notification.admin.AdminNotificationMiddleware',] </code></pre>

![Запрос отклонен](/images/imag_1.png)
<br>  

![Запрос одобрен](/images/imag_2.png)
<br>

![Авторизоваться](/images/imag_3.png)

