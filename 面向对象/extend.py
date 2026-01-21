class Phone:
    IMEI = None
    producer = "HM"

    def call_by_4g(self):
        print("使用4G通话")

class Phone2025(Phone):
    face_id = "1234567890"   #面部识别

    def call_by_5g(self):
        print("使用5G通话")


class NFCReader:
    nfc_type = "第五代"
    producer = "非洲"

    def read_card(self):
        print("NFC读卡")

    def write_card(self):
        print("NFC写入")


class RemoteControl:
    rc_type = "红外遥控"

    def control(self):
        print("红外开启了")


class MyPhone(Phone, RemoteControl, NFCReader):
    pass
#单继承
phone = Phone2025()
phone.call_by_5g()
phone.call_by_4g()
print(phone.producer)

#多继承
phone1 = MyPhone()
phone1.call_by_4g()
phone1.read_card()
phone1.write_card()
phone1.control()
#继承的属性若有不同，按顺序优先
print(phone1.producer)

#调用父类
class PHONE(Phone):
    producer = "ITcast"

    def check_p(self):
        print(f"本机的厂商是{self.producer}")
        print(f"上一代厂商{super().producer}")

phone2 = PHONE()
phone2.check_p()