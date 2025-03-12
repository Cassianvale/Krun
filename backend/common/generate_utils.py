# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : generate_utils.py
@DateTime: 2025/1/15 13:57
"""
import random
import string
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional, Literal, Union

from dateutil.relativedelta import relativedelta
from faker import Faker
from xpinyin import Pinyin


class GenerateUtils:
    # 用于存储该类的唯一实例
    __private_instance = None
    __private_initialized = False
    __private_lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> object:
        """
        创建并返回类的唯一实例。

        使用单例模式，在整个应用程序的生命周期内仅创建一个 `RequestSyncUtils` 实例。
        在多线程环境下，通过 `threading.Lock` 确保线程安全。

        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: `RequestSyncUtils` 类的实例
        """
        if not cls.__private_instance and not cls.__private_initialized:
            with cls.__private_lock:
                if not cls.__private_instance and not cls.__private_initialized:
                    cls.__private_instance = super().__new__(cls)
                    cls.__private_initialized = True

        return cls.__private_instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker_cn = Faker(locale="zh_CN")
        self.faker_en = Faker(locale="en_US")
        self.pinyin = Pinyin()
        self.formats: dict = {
            11: "%Y",
            12: "%m",
            13: "%d",
            14: "%H",
            15: "%M",
            16: "%S",

            21: "%Y%m%d",
            22: "%Y-%m-%d",
            23: "%Y{0}%m{1}%d{2}".format("年", "月", "日"),

            31: "%H%M%S",
            32: "%H:%M:%S",
            33: "%H{0}%M{1}%S{2}".format("时", "分", "秒"),

            41: "%Y%m%d%H%M%S",
            42: "%Y-%m-%d %H:%M:%S",
            43: "%Y/%m/%d %H:%M:%S",
            44: "%Y{0}%m{1}%d{2} %H{3}%M{4}%S{5}".format("年", "月", "日", "时", "分", "秒"),

            51: "%Y%m%d%H%M%S%f",
            52: "%Y-%m-%d %H:%M:%S:%f",
            53: "%Y/%m/%d %H:%M:%S:%f",
            54: "%Y{0}%m{1}%d{2} %H{3}%M{4}%S{5}%f{6}".format("年", "月", "日", "时", "分", "秒", "毫秒"),
        }

    @property
    def generate_country(self):
        return self.faker_cn.country()

    @property
    def generate_province(self):
        return self.faker_cn.province()

    @property
    def generate_city(self):
        return self.faker_cn.city()

    @property
    def generate_district(self):
        return self.faker_cn.district()

    @property
    def generate_address(self):
        return self.faker_cn.address()

    @property
    def generate_company(self):
        return self.faker_cn.company()

    @property
    def generate_bank_account_number(self):
        return self.faker_cn.credit_card_number()

    @property
    def generate_email(self):
        return self.faker_cn.email()

    @property
    def generate_job(self):
        return self.faker_cn.job()

    @property
    def generate_name(self):
        return self.faker_cn.name()

    @property
    def generate_phone(self):
        return self.faker_cn.phone_number()

    @property
    def generate_week_number(self):
        today = datetime.today()
        return today.isocalendar()[:2][1]

    @property
    def generate_week_name(self):
        return self.faker_cn.day_of_week()

    @property
    def generate_day(self):
        return datetime.now().timetuple().tm_yday

    @property
    def generate_am_or_pm(self):
        return "上午" if self.faker_cn.am_pm() == "AM" else "下午"

    @property
    def generate_ident_card_number(self):
        return self.faker_cn.ssn(min_age=18, max_age=65)

    def generate_ident_card_number_condition(self, min_age: int, max_age: int):
        return self.faker_cn.ssn(min_age=min_age, max_age=max_age)

    @staticmethod
    def generate_ident_card_birthday(ident_card_number: str):
        return ident_card_number[6:-4]

    @staticmethod
    def generate_ident_card_gender(ident_card_number: str):
        return "女" if int(ident_card_number[-2]) % 2 == 0 else "男"

    def generates(self, funcname: str, funcargs: Optional[dict] = None, funclocale: Literal["en", "cn"] = "cn"):
        return getattr(eval("self.faker_" + funclocale), funcname)(**funcargs or {})

    @staticmethod
    def generate_random_number(min: int, max: int) -> int:
        return random.randint(min, max)

    @staticmethod
    def generate_string(length: int, digit: bool = False, char: bool = False, chinese: bool = False) -> str:
        try:
            length: int = int(length)
            number = "".join(random.sample(string.digits * length, length))
            english = "".join(random.sample(string.ascii_letters * length, length))
            word = str("".join([chr(random.randint(0x4e00, 0x9fbf)) for _ in range(length)]))
        except ValueError as ve:
            raise ValueError(f"随机生成字符串失败，处理长度参数[{length}]时发生意外错误：{ve}")

        # 1.随机一种
        if digit and not char and not chinese:
            generate_string = number
        elif char and not digit and not chinese:
            generate_string = english
        elif chinese and not digit and not char:
            generate_string = english

        # 2.随机两种
        elif digit and char and not chinese:
            generate_string = "".join(random.sample(number + english, length))
        elif digit and chinese and not char:
            generate_string = "".join(random.sample(number + word, length))
        elif char and chinese and not digit:
            generate_string = "".join(random.sample(english + word, length))

        # 3.随机三种
        elif digit and char and chinese:
            generate_string = "".join(random.sample(number + word + english, length))

        # 默认
        else:
            generate_string = number

        return generate_string[::-1]

    def generate_datetime(self, year: int = 0, month: int = 0, day: int = 0,
                          hour: int = 0, minute: int = 0, second: int = 0,
                          fmt: Optional[Union[int, str]] = None, isMicrosecond: bool = False) -> Union[datetime, str]:
        """
        根据当前日期时间自定义修改年、月、日、时、分、秒和格式
        :param year:    非必填项，年份控制
        :param month:   非必填项，月份控制
        :param day:     非必填项，日份控制
        :param hour:    非必填项，小时控制
        :param minute:  非必填项，分钟控制
        :param second:  非必填项，秒数控制
        :param fmt:  非必填项，格式控制
        :param isMicrosecond:  非必填项，毫秒控制
        :return: 默认以XXXX-XX-XX XX:XX:XX格式返回当前日期时间
        """
        # 获取当前日期时间
        current_datetime = datetime.now()
        if not isMicrosecond:
            current_datetime = current_datetime.replace(microsecond=0)

        # 计算偏移量
        current_datetime = current_datetime + relativedelta(**{
            "years": year, "months": month, "days": day,
            "hours": hour, "minutes": minute, "seconds": second
        })

        # 格式化
        if fmt:
            if fmt not in (23, 33, 43, 53):
                current_datetime = current_datetime.strftime(self.formats.get(fmt, fmt))
            else:
                current_datetime = current_datetime.strftime(
                    self.formats.get(fmt, fmt).encode("unicode_escape").decode('utf-8')
                ).encode("utf-8").decode("unicode_escape")

        return current_datetime

    def generate_pinyin(self, chars: str, splitter: str = "",
                        convert: Literal["lower", "upper", "capitalize"] = "lower"):
        # 暂时无法处理多音字
        return self.pinyin.get_pinyin(chars=chars, splitter=splitter, convert=convert)

    def generate_information(self, minAge: int = 18, maxAge: int = 65,
                             convert: Literal["lower", "upper", "capitalize"] = "upper"):
        ident_card_name: str = self.generate_name
        ident_card_number: str = self.generate_ident_card_number_condition(minAge, maxAge)
        ident_card_gender: str = self.generate_ident_card_gender(ident_card_number)
        ident_card_birthday: str = self.generate_ident_card_birthday(ident_card_number)
        ident_card_age: int = int(self.generate_datetime(fmt=11)) - int(ident_card_birthday[:4])
        bank_card_name: str = self.generate_bank_account_number
        resp: dict = {
            "name": ident_card_name,
            "alias": self.generate_pinyin(chars=ident_card_name, convert=convert),
            "age": str(ident_card_age),
            "gender": ident_card_gender,
            "ssn": ident_card_number,
            "card": bank_card_name,
            "phone": self.generate_phone,
            "email": self.generate_email,
            "address": self.generate_address,
            "company": self.generate_company,
            "company_address": self.generate_address,
            "job": self.generate_job,
            "birthday1": ident_card_birthday,
            "birthday2": ident_card_birthday[:4] + "-" + ident_card_birthday[4:-2] + "-" + ident_card_birthday[-2:],
        }
        return resp

    @property
    def generate_global_serial_number(self):
        """
        全局流水号，28位（年 + 月 + 日 + 时 + 分 + 秒 + 毫秒 + 9999 + 4位随机数）
        """
        stamp = self.generate_datetime(fmt=51, isMicrosecond=True)
        g1 = stamp + "9999" + self.generate_string(length=4)
        g2 = stamp + "9999" + self.generate_string(length=4)
        g3 = stamp + "9999" + self.generate_string(length=4)
        return g1, g2, g3

    @property
    def generate_uuid(self):
        return uuid.uuid4().__str__()

    @property
    def generate_timestamp(self):
        now = datetime.now()
        timestamp = (now - datetime(1970, 1, 1)).total_seconds() * 1000000
        return int(timestamp)

    @property
    def generate_seconds_until_22h(self):
        now = datetime.now()
        midnight = now.replace(hour=22, minute=0, second=0, microsecond=0)
        if now >= midnight:
            midnight += timedelta(days=1)
        delta = midnight - now
        return int(delta.total_seconds())

    @classmethod
    def generate_seconds_until(cls, year: int = 0, month: int = 0, day: int = 0,
                               hour: int = 0, minute: int = 0, second: int = 0) -> int:
        # 当前时间
        current_datetime: datetime = datetime.now()
        target_datetime: datetime = current_datetime
        # 时间偏移
        target_datetime = target_datetime + relativedelta(**{
            "years": year, "months": month, "days": day,
            "hours": hour, "minutes": minute, "seconds": second
        })
        # 计算时间差
        time_difference: timedelta = target_datetime - current_datetime
        total_seconds: int = int(time_difference.total_seconds())
        return total_seconds if total_seconds > 0 else 0


GENERATE = GenerateUtils()

if __name__ == '__main__':
    vd = GenerateUtils()
    # print("国家：", vd.generate_country)
    # print("地址：", vd.generate_address)
    # print("姓名：", vd.generate_name)
    # print("银行卡号：", vd.generate_bank_account_number)
    # print("身份证号码：", vd.generate_ident_card_number)
    # print("身份证号码：", vd.generate_ident_card_number_condition(1, 10))
    # print("身份证生日：", vd.generate_ident_card_birthday(idn))
    # print("身份证性别：", vd.generate_ident_card_gender(idn))
    # print("周名：", vd.generate_week_name)
    # print("周号：", vd.generate_week_number)
    # print("天：", vd.generate_day)
    # print("反射：", vd.generates(funcname="ssn"))
    # print("反射：", vd.generates(funcname="ssn", funcargs={"min_age": 18, "max_age": 18}))
    # print("反射：", vd.generates(funcname="profile", funcargs={"fields": None, "sex": "F"}))
    # print("反射：", vd.generates(funcname="simple_profile", funcargs={"sex": "M"}))
    # print("个人档案：", vd.generates(funcname="profile"))
    # print("个人档案：", vd.generate_information())
    # print("时间：", vd.generate_datetime(fmt=11))
    # print("时间：", vd.generate_datetime(fmt=21))
    # print("时间：", vd.generate_datetime(fmt=31))
    # print("时间：", vd.generate_datetime(fmt=41))
    # print("时间：", vd.generate_datetime(fmt="%Y----%m"))
    # print("时间：", vd.generate_datetime(year=int("-1"), fmt=23))
    # print("时间：", vd.generate_datetime(fmt="%Y----%23"))
    print("时间戳：", vd.generate_timestamp)
    # print("拼音：", vd.generate_pinyin("上海银行"))
    # print("拼音：", vd.generate_pinyin("上海银行", splitter="-"))
    # print("拼音：", vd.generate_pinyin("上海银行", splitter="-", convert="upper"))
    # print(vd.generate_string(length=10))
    # print(vd.generate_string(length=10, char=True))
    # print(vd.generate_string(length=10, chinese=True))
    # print(vd.generate_string(length=10, digit=True))
    # print(vd.generate_string(length=10, char=True, chinese=True, digit=True))
    print(vd.generate_global_serial_number)
    print(vd.generate_seconds_until_22h)
    print(vd.generate_seconds_until())
    print(vd.generate_seconds_until(minute=3, second=59))
