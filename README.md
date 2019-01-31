# Хабрапрокси
Используется`Python3`.
Http-прокси-сервер показывает содержимое страниц Хабра, модицифируя текст на страницах следующим образом: 
* после каждого слова из шести букв добавляет значок «™»
* при навигации по ссылкам, которые ведут на другие страницы хабра, браузер остается на адресе нашего прокси

## Установка
1. Создайте копию данного удаленного репозитория на своем устройстве. В примере ниже клонирование происходит в папку `src`, но вы можете выбрать любое другое имя
```bash
$ git clone https://github.com/andrepopoff/habraproxy src
```
2. Переместитесь в директорию `src`:
```bash
$ cd src
```
3. Создайте виртуальное окружение и активируйте его:
```bash
$ virtualenv venv
$ source venv/bin/activate
```
4. Установите зависимости
```bash
$ pip install -r requirements.txt
```
5. Переместитесь в директорию `habraproxy`:
```bash
$ cd habraproxy
```
6. Запустите Django сервер:
```bash
$ python manage.py runserver
```
Всё готово к работе!

## Использование
По умолчанию, сервер запускается по адресу http://127.0.0.1:8000/
Перейдя по этому адресу, Вы увидите главную страницу Хабра с модифицированным текстом
