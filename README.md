1. Установить зависимости из файла requirements.txt;
2. Перетащить в папку с проектом *.proto файл;
3. Выполнить команду в папке с *.proto файлом:   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto_fie_name.proto
