# task_for_networking
____
ссылка на docker hub: https://hub.docker.com/repository/docker/5849/subnets_natali


### 1)В системе должен быть установлен докер, команды для установки конкретно в ubuntu (и почти во всех остальных дистрибутивах Linux): 
```bash
sudo apt update && sudo apt upgrade 
sudo apt install apt-transport-https ca-certificates curl software-properties-common 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 
sudo snap install docker 
```
при вводе команды: 
```bash
docker
``` 
должен отобразиться список возможных команд - тогда этот шаг завершен.
### 2) необходимо для входа в docker hub ввести команду:
```bash
docker login 
```
### 3) в каталоге, где лежат файлы in.txt и main.py, ввести команды:
```bash
sudo docker pull 5849/subnets_natali:v1.0
sudo docker run -v $(pwd):/data 5849/subnets_natali:v1.0 
```
должны появиться два файла autogen.txt и out.txt.


1. входные данные - в файле in.txt в первой строке указывается кол-во для генерации валидных подсетей N и произвольный ipv4-адрес.
2. выходные данные - в файле autogen.txt находятся сгенерированные подсети(в данном репозитории в файле находится результат неоднократного запуска программы,
поэтому кол-во подсетей превышает число N), в файле out.txt находится результат соотвествия ipv4-адреса одной или нескольким сгенерированным подсетям, из них выбирается "лучший маршрут", который записывается в данный выходной файл.
В случае отсутствия такового, выводится сообщение об этом и предлагается маршрут "по умолчанию" - 0.0.0.0/0.
3. файл main.py - исходный код.
4. программа не является идеальной :)
