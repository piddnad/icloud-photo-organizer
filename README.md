# Photos Organizer

## Overview
日常生活中产生的海量照片，在本地进行备份是非常重要的。iCloud 照片虽然自带了导出功能，但导出的照片完全没有可整理性，文件命名也是一团糟。

因此，我编写了该脚本，实现自动整理 iCloud 照片导出的照片和视频文件。

## Functions
- 复制照片原文件，保留照片元数据；
- 按照 2019-01-01 09.12.34.JPG 的格式重命名文件；
- 按照 拍摄年份/月份 的文件夹结构分类照片；
- 支持 Live Photos，实现了照片同名的 mov 文件的改名和整理；
- 支持 AAE文件（在设备上对照片进行的编辑）；
- 支持视频文件（.MOV）。

## To-dos
* [ ] 增量备份功能 

## References
1. http://www.leancrew.com/all-this/2013/10/photo-management-via-the-finder/
2. https://it.ismy.fun/2018/08/22/python3-read-exif-by-pillow/