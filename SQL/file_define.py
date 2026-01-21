from data_define import Record
import json

#定义抽象类
class FileReader:

    def read_data(self) -> list[Record]:
        """ 读取文件的数据，读取到的每一条数据都转化为Record对象，将它们封装到list中"""
        pass


class TextFileReader(FileReader):

    def __init__(self, path):
        self.path = path

    #复写，实现抽象方法
    def read_data(self) -> list[Record]:
        f = open(self.path, "r", encoding="UTF-8")

        record_list = []
        for line in f.readlines():
            line = line.strip()     #消除读取到的回车
            data_list = line.split(",")
            record = Record(data_list[0], data_list[1], int(data_list[2]), data_list[3])
            record_list.append(record)
        
        f.close()
        return record_list


class JsonFileReader(FileReader):
    
    def __init__(self, path):
        self.path = path

    #复写
    def read_data(self) -> list[Record]:
        f = open(self.path, "r", encoding = "UTF-8")

        record_list = []
        for line in f.readlines():
            data_dict = json.loads(line)
            record = Record(data_dict["date"], data_dict["order_id"], int(data_dict["money"]), data_dict["province"])
            record_list.append(record)

        f.close()
        return record_list