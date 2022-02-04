# Created by Piddnad on 2019/8/19
# Edited on 2022/2/4
# Reference: http://www.leancrew.com/all-this/2013/10/photo-management-via-the-finder/

import os, shutil
import subprocess
import os.path
import datetime as dt
from datetime import datetime
import hachoir.parser
import hachoir.metadata
from tqdm import tqdm


#################### Configuration #########################

# 照片文件的初始位置和整理后位置
source_dir = os.environ['HOME'] + '/Pictures/iPhone_export'
dest_dir = os.environ['HOME'] + '/Pictures/iPhone_organized'

# 照片和其他文件格式
photo_fmt = ['jpg', 'JPG', 'HEIC', 'PNG']
addition_fmt = ['MOV', 'mov', 'mp4', 'AAE']

# 新照片文件名格式
fmt = "%Y-%m-%d %H.%M.%S"


######################## Functions #########################

# 返回照片的拍摄时间
def get_photo_date(f):
    output = subprocess.check_output(['sips', '-g', 'creation', f]).decode('utf-8')
    take_date = output.split('\n')[1].lstrip().split(': ')[1]
    return datetime.strptime(take_date, "%Y:%m:%d %H:%M:%S")


def get_video_date(f):
    info = hachoir.metadata.extractMetadata(hachoir.parser.createParser(f))
    for line in info.exportPlaintext():
        if 'Creation date' in line:
            take_date = line.replace('- Creation date:', '').strip()
            return (datetime.strptime(take_date, "%Y-%m-%d %H:%M:%S") + dt.timedelta(hours=8))


###################### Main program ########################

if __name__ == "__main__":
    # 整理时出现问题的照片
    problems = []
    
    # 获取照片文件名
    files = os.listdir(source_dir)
    photos = [ x for x in files if x.split('.')[1] in photo_fmt]
    additions = [ x for x in files if x.split('.')[1] in addition_fmt]

    #复制照片到年月目录下并重命名照片文件为拍摄日期，如果有多个照片有相同拍摄日期，在文件名加'a','b',...后缀
    for photo in tqdm(photos):
        original = source_dir + '/' + photo
        suffix = 'a'
        try:
            take_date = get_photo_date(original)
            yr = take_date.year
            mo = take_date.month
            newname = take_date.strftime(fmt)
            dir = dest_dir + '/%04d/%02d/' % (yr, mo)
            if not os.path.exists(dir):
                os.makedirs(dir)
            duplicate = dir + newname + photo[photo.find('.'):]
            # 处理重名照片
            while os.path.exists(duplicate):
                newname = take_date.strftime(fmt) + suffix
                duplicate = dir + newname + photo[photo.find('.'):]
                suffix = chr(ord(suffix) + 1)
            
            shutil.copy2(original, duplicate)
            
            # 复制其他文件（mov、aae）
            for a_fmt in addition_fmt:
                addition = photo[:photo.rfind('.')] + '.' + a_fmt
                if addition in additions:
                    additions.remove(addition)
                    addition_file = original[:original.rfind('.')] + '.' + a_fmt
                    duplicate = duplicate[:duplicate.rfind('.')] + '.' + a_fmt
                    shutil.copy2(addition_file, duplicate)

        except ValueError:
            problems.append(photo)
    
    # 处理单独的视频文件
    for addition in additions:
        original = source_dir + '/' + addition
        try:
            take_date = get_video_date(original)
            yr = take_date.year
            mo = take_date.month
            newname = take_date.strftime(fmt)
            dir = dest_dir + '/%04d/%02d/' % (yr, mo)
            if not os.path.exists(dir):
                os.makedirs(dir)
            duplicate = dir + newname + addition[addition.find('.'):]
            
            shutil.copy2(original, duplicate)

        except Exception:
            problems.append(addition)

    print("Processing completed!")
   
    # 打印和处理出现问题的照片
    if len(problems) > 0:
        print("Problem files:")
        print("\n".join(problems))
        if not os.path.exists(dest_dir + '/problems'):
            os.makedirs(dest_dir + '/problems')
        for file in problems:
            original = source_dir + '/' + file
            duplicate = dest_dir + '/problems/' + file
            shutil.copy2(original, duplicate)