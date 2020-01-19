import os
#照片檔案路徑
Path = r"檔案路徑"
all_file_list = os.listdir(Path)

Oldpostfix = [r".con" ,r".=sc"]
Newpostfix = r".jpg"

IOldpostfix = [r".DB9" ,r".DB8" ,r".DBA"]
INewpostfix = r".mp4"


def Modifypostfix(oldftype ,newftype):
    for file_name in all_file_list:
        currentdir = os.path.join(Path ,file_name)
        print(currentdir)
        #print(file_name)
        if os.path.isdir(currentdir): #跳過資料夾
            continue
        fname  = os.path.splitext(file_name)[0]
        refname = fname.split(".")[0]
        ftype = os.path.splitext(file_name)[1]
        if (ftype == oldftype[0] or ftype == oldftype[1] ) :  #找到需要修改的副檔名
            newname = os.path.join(Path ,refname+newftype)
            os.rename(currentdir ,newname)


def Iodifypostfix(oldftype ,newftype):
    for file_name in all_file_list:
        currentdir = os.path.join(Path ,file_name)
        print(currentdir)
        #print(file_name)
        if os.path.isdir(currentdir): #跳過資料夾
            continue
        fname  = os.path.splitext(file_name)[0]
        refname = fname.split(".")[0]
        ftype = os.path.splitext(file_name)[1]
        if (ftype == oldftype[0] or ftype == oldftype[1] or ftype == oldftype[2] ):  #找到需要修改的副檔名
            newname = os.path.join(Path ,refname+newftype)
            os.rename(currentdir ,newname)



print("Modify file postfix")
Modifypostfix(Oldpostfix ,Newpostfix)
Iodifypostfix(IOldpostfix ,INewpostfix)
print("finished")
