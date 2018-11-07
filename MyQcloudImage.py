import os
import wmi
import configparser
import shutil
from qcloud_image import Client
from qcloud_image import CIFile


class MyQcloudImage:
    __appid = '1252858602'
    __secret_id = 'AKIDTu9e3MafaJuMexuID0er22qUzLgwA3rS' #  https: // console.qcloud.com / cam / capi获取
    __secret_key = 'oCUccQD43wfheYN0Sir16YzGLEC9pRdR'
    __bucket = 'BUCKET'
    __group = ''
    __person = 'person'
    __id = 1
    is_same = 70
    path = ''
    fileList = []
    picInfo = {}

    def __init__(self, path):
        self.path = path
        #初始化配置
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.cf = configparser.ConfigParser()
        self.cf.read("config.conf")
        self.__appid = self.cf.get("info", "appid")
        self.__secret_id = self.cf.get("info", "secret_id")
        self.__secret_key = self.cf.get("info", "secret_key")
        self.is_same = int(self.cf.get("info", "is_same"))

        # 初始化Client
        self.client = Client(self.__appid, self.__secret_id, self.__secret_key, self.__bucket)
        self.client.use_http()
        self.client.set_timeout(30)
        # 初始化group
        self.__group = self.get_board_serialnumber()

    # 主板
    @staticmethod
    def get_board_serialnumber():
        c = wmi.WMI()
        for board_id in c.Win32_BaseBoard():
            return board_id.SerialNumber  # 主板序列号

    def traverse(self):
        fs = os.listdir(self.path)
        for f1 in fs:
            tmp_path = os.path.join(self.path, f1)
            if not os.path.isdir(tmp_path):
                self.fileList.append(tmp_path)

    def add_new_pic(self, path):
        print(self.__person + str(self.__id))
        print(self.client.face_newperson(self.__person + str(self.__id), [self.__group, ], CIFile(path)))
        person_id = self.__person + str(self.__id)
        if person_id in self.picInfo:
            self.picInfo[person_id] = self.picInfo[person_id] + "," + path
        else:
            self.picInfo[person_id] = path
        self.__id = self.__id + 1

    def find_pic(self, path):
        result = self.client.face_identify(self.__group, CIFile(path))
        if result['code'] == 0:
            result = result['data']['candidates']
        else:
            result = []
        return result

    def lookup_pic(self, path):
        mem_list = self.find_pic(path)
        if len(mem_list) == 0:
            self.add_new_pic(path)
            mem_list = self.find_pic(path)
        find_pic = False
        for item in mem_list:
            if item['confidence'] >= self.is_same:
                find_pic = True
                person_id = item['person_id']
                if person_id in self.picInfo:
                    self.picInfo[person_id] = self.picInfo[person_id] + "," + path
                else:
                    self.picInfo[person_id] = path
                return
            if not find_pic:
                self.add_new_pic(path)

    def delete_group(self):
        # 获取组列表
        groups = self.client.face_getgroupids()
        if groups['code'] == 0:
            for item in groups['data']['group_ids']:
                persons = self.client.face_getpersonids(item)
                if persons['code'] == 0:
                    if "person_ids" in persons['data']:
                        for item2 in persons['data']['person_ids']:
                            print(self.client.face_delperson(item2))

    def do_excute(self):
        self.traverse()
        for item in self.fileList:
            self.lookup_pic(item)
        return self.picInfo

try:
    #这里写你很可能出错的代码
    print("输入'cp'(clearperson) 清空索引库\n")
    input_path = input("请输入命令/拖入文件夹路径：\n")
    myQcloudImage = MyQcloudImage(input_path)
    if input_path == "cp":
        myQcloudImage.delete_group()
    else:
        filelist = myQcloudImage.do_excute()
        dirpath = input_path + 'Class'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        for key, values in filelist.items():
            dirpath_child = dirpath + '/' + key;
            if not os.path.exists(dirpath_child):
                os.makedirs(dirpath_child)
            print(key + ":")
            varr = values.split(',')
            for item in varr:
                shutil.copy(item, dirpath_child + "/" + os.path.basename(item))
                print(item)
except Exception as err:
    print(err)
    #让程序停在这里等待回车键退出
    input('Please press enter key to exit ...')














