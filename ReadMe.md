# Image Refiner

@author: Aleksandr Melnik

@version: 1.0

## Description

Скрипт для добавления водяного знака к изображению.
Так же приводит размер изображения по большей стороне к 1000 пикселей.

Водяной знак устанавливается в правом нижнем углу изображения.
На вертикальных изображениях водяной знак имеет ширину в половину кадра, на горизонтальных - одну треть.

## Requirements

Python 3.x  
Pillow  

## Usage

Для использования скрипта введите следующую команду:

```
python imgrefiner/main.py --input [input image] --watermark [watermark image] --output [output image] --path [working directory] [--verbose]
```

Замените ```[input image]```, ```[watermark image]```, и ```[output image]``` на имена файлов, которые вы хотите использовать.

Замените ```[working directory]``` на директорию, в которой находятся изображения для пакетной обработки.

Добавьте флаг ```--verbose```, если вы хотите получить дополнительную информацию о процессе.

```[output image]``` - имя файла для выходного изображения. Если не указано, то будет использоваться имя ```[input image] + _watermarked.jpg```

## Example

```
python imgrefiner/main.py --input image.jpg --watermark watermark.png --output output.jpg --path /path/to/images --verbose
```

## Batch processing 

Для пакетной обработки входной параметр может принимать файл со списком изображений.  
Список изображений должен быть в файле в текстовом формате, одно имя в строке.  
Путь к каталогу с изображениями указывается в параметре ```--path```.
расширение файла должно быть ```.txt``` или ```.tmp``` или ```.lst```  
Выходные файлы будут сохранены в каталоге ```--path``` с добавлением к имени суффикса ```_watermarked```.

```
python imgrefiner/main.py --input image_list.txt --watermark watermark.png  --path /path/to/images --verbose
```

## Far Manager

Для использования скрипта в Меню (```F2```) в Far Manager добавьте в редакторе Меню команду:

```
path_to_venv/venv/Scripts/python.exe path_to_script_directory/imgrefiner/main.py --input !@! --watermark path_to_watermark\watermark.png --verbose --path !\
```
