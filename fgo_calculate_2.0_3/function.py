from test_gui import *
from PyQt5 import QtWidgets
from select_servant import *
from servant_name import *
import time
import sys
import csv
import os
import re

'''
1.进行测试，确认无误后更新数据库，并尝试添加新的功能
2.精简代码，删除多余、无用代码
3.修复狂那伤害计算错误(已修复)
4.把职阶技能的buff加入到计算中
注：5期泳装数据暂未加入
'''


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("fgo np calculator v2.0 Beta")
        self.setWindowIcon(QtGui.QIcon('./fgo.png'))
        self.random = 0
        self.class_rate = 0
        self.np_level = 0
        self.camp_rate = 0
        self.servant_np_info = []
        self.rarity = ''
        self.atk_info = []
        self.servant_level = ''
        self._class = ''
        self.name = ''
        self.servant = ''
        self.atk = ''
        self.effect = {}
        self.about_gui = AboutGUI()
        self.is_exist = True

    # 计算
    def s_calculate(self):
        # 开始计算

        # 检测从者信息是否存在
        if not self.is_exist:
            QtWidgets.QMessageBox.warning(self, "警告", "从者信息暂未加入数据库")
            self.log(3, 'servant info not exist')
            self.log(3, 'cal fail')
            return 0

        # 检测是否选中从者
        if not self.comboBox_2.currentText():
            QtWidgets.QMessageBox.warning(self, "警告", "从者未选中")
            self.log(2, 'servant not select')
            self.log(3, 'cal fail')
            return 0

        # 检测是否设置从者等级
        if self.radioButton.isChecked() or self.radioButton_2.isChecked() or self.radioButton_3.isChecked():
            pass
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "从者等级未设置")
            self.log(2, "servant level set fail")
            self.log(3, 'cal fail')
            return 0

        # 检测宝具种类是否为‘辅助’
        if self.servant.servant_np_info[0][1] == '辅助':
            QtWidgets.QMessageBox.warning(self, "警告", "从者宝具种类为‘辅助’，无法计算伤害")
            self.log(2, 'servant np kind not correct')
            self.log(3, 'cal fail')
            return 0

        # 获取buff值
        calculate_element = self.get_calculate_element()
        for key, value in calculate_element.items():
            if not value:
                calculate_element[key] = '0'
        if calculate_element['np_special_attack'] == '0':
            calculate_element['np_special_attack'] = '100'
        # 重新获取一下值，防止不对乱数什么的进行设置，导致值为0
        self.s_get_camp_rate()
        self.s_get_class_rate()
        self.s_get_random()

        # 获取宝具前置效果
        for key, value in self.effect.items():
            if ('Buster' or 'Quick' or 'Arts') in key:
                calculate_element['card_range'] = re.sub('%', '', self.effect[key])
            elif '宝具' in key:
                calculate_element['np_power'] = re.sub('%', '', self.effect[key])
            elif ('防御力下降' or '攻击力') in key:
                calculate_element['ATK_range'] = re.sub('%', '', self.effect[key])
            # elif '特攻' in key:
            #     calculate_element['special_attack'] = re.sub('%', '', self.effect[key])

        # 转换
        card_range = eval(calculate_element['card_range'] + '/100')
        np_power = eval(calculate_element['np_power'] + '/100')
        ATK_range = eval(calculate_element['ATK_range'] + '/100')
        defense_down = eval(calculate_element['defense_down'] + '/100')
        np_special_attack = eval(calculate_element['np_special_attack'] + '/100')
        special_attack = eval(calculate_element['special_attack'] + '/100')
        fixed_damage = int(calculate_element['fixed_damage'])
        np_multiplying_power = re.sub('%', '', self.servant.np_multiplying_power(self.get_np_level()))
        if self.servant_np_info[0][0] == 'Arts':
            np_multiplying_power = eval(np_multiplying_power + '/100')
        elif self.servant_np_info[0][0] == 'Buster':
            np_multiplying_power = eval(np_multiplying_power + '/100' + '* 1.5')
        elif self.servant_np_info[0][0] == 'Quick':
            np_multiplying_power = eval(np_multiplying_power + '/100' + '* 0.8')
        atk = eval(self.servant.get_class_additions() + '* {}'.format(calculate_element['atk']))

        # 计算
        result = atk * 0.23 * (
                np_multiplying_power * (1 + card_range) * (1 + np_power + special_attack) * np_special_attack * (
                1 + ATK_range + defense_down) * float(self.random) * float(self.camp_rate) * float(
            self.class_rate)) + fixed_damage

        # 输出结果
        self.log(1, '宝具伤害：%.0f' % result)

    # 获取职阶系数
    def s_get_class_rate(self):
        if self.get_class() not in ['berserker', 'alterego']:
            if self.get_class_rate() == '克制':
                self.class_rate = '2'
            elif self.get_class_rate() == '被克制':
                self.class_rate = '0.5'
            elif self.get_class_rate() == '一般':
                self.class_rate = '1'
        else:
            if self.get_class_rate() == '克制':
                self.class_rate = '1.5'
            elif self.get_class_rate() == '被克制':
                self.class_rate = '0.5'
            elif self.get_class_rate() == '一般':
                self.class_rate = '1'

    # 获取宝具等级
    def s_get_np_level(self):
        self.np_level = self.get_np_level()

    # 获取乱数
    def s_get_random(self):
        if self.get_random() == '最大':
            self.random = '1.1'
        elif self.get_random() == '最小':
            self.random = '0.9'
        elif self.get_random() == '平均':
            self.random = '1'

    # 获取阵营系数
    def s_get_camp_rate(self):
        if self.get_camp_rate() == '克制':
            self.camp_rate = '1.1'
        elif self.get_camp_rate() == '一般':
            self.camp_rate = '1'
        elif self.get_camp_rate() == '被克制':
            self.camp_rate = '0.9'

    # 根据职阶选择从者
    def set_combobox2(self):
        if self.get_class() == 'saber':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Saber)
        elif self.get_class() == 'archer':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Archer)
        elif self.get_class() == 'lancer':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Lancer)
        elif self.get_class() == 'rider':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Rider)
        elif self.get_class() == 'caster':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Caster)
        elif self.get_class() == 'berserker':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Berserker)
        elif self.get_class() == 'assassin':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Assassin)
        elif self.get_class() == 'mooncancer':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(MoonCancer)
        elif self.get_class() == 'alterego':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(AlterEgo)
        elif self.get_class() == 'ruler':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Ruler)
        elif self.get_class() == 'avenger':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Avenger)
        elif self.get_class() == 'shielder':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Shielder)
        elif self.get_class() == 'foreigner':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(Foreigner)

    # 根据combobox中的从者名，上相应的文件夹中遍历出所有的csv文件，然后读取、过滤出想要的信息
    def set_servant_info(self):
        self.servant_np_info = []
        self.atk_info = []
        self.rarity = ''
        f_csv_1 = ''
        f_csv_2 = ''
        f_csv_3 = ''
        selected_servant = self.comboBox_2.currentText()
        self.add_image(selected_servant)
        dirs = os.listdir('./data/servant')
        for file in dirs:
            if selected_servant == re.sub('[0-9]+', '', file):
                f_csv_1 = self.csv_reader(file + '/data_np.csv')
                f_csv_2 = self.csv_reader(file + '/data_atk.csv')
                f_csv_3 = self.csv_reader(file + '/data_basic.csv')
                break
        if f_csv_1 == '' and f_csv_2 == '' and f_csv_3 == '':
            self.is_exist = False
        else:
            # row[3]卡色,row[4]宝具类型,row[5]宝具是否强化,row[6]宝具强化时间,row[7]宝具效果,row[19:24]提升幅度(宝具前置效果默认不随oc变化，只记录oc100的幅度)
            for row in f_csv_1:
                if row[5] != '强化前' and row[3] != '卡色':
                    self.servant_np_info.append(
                        [row[3], row[4], row[5], row[7], row[19], row[20], row[21], row[22], row[23]])
            for row in f_csv_2:
                if row[0] != '\ufeff序号':
                    self.atk_info = row[2:]
            for row in f_csv_3:
                if row[0] != '\ufeff序号':
                    self.rarity = row[1]
                    self.name = row[2]
                    self._class = row[8]
            self.is_exist = True

    # csv读取
    def csv_reader(self, filepath):
        try:
            f = open('./data/servant/' + filepath, encoding='utf-8')
            f_csv = csv.reader(f)
            return f_csv
        except:
            file = './data/servant/' + filepath
            self.log(3, '%s not exist' % file)
            return ''

    # 设置从者等级
    def set_servant_level(self):
        # 检测是否选中从者
        if not self.comboBox_2.currentText():
            QtWidgets.QMessageBox.warning(self, "警告", "从者未选中")
            self.log(2, 'servant not select')
            return 0
        if not self.is_exist:
            QtWidgets.QMessageBox.warning(self, "警告", "从者信息暂未加入数据库")
            self.log(3, 'servant info not exist')
            return 0

        r1, r2, r3 = self.get_state()
        if r1:
            self.servant_level = '满破'
        elif r2:
            self.servant_level = '90级'
        elif r3:
            self.servant_level = '100级'
        self.create_servant()

    # 创建从者实例，方便信息保存和调用
    def create_servant(self):
        self.servant = SelectServant(servant_np_info=self.servant_np_info, servant_atk_info=self.atk_info,
                                     servant_level=self.servant_level,
                                     rarity=self.rarity, _class=self._class, name=self.name)
        self.atk, self.effect = self.servant.get_calculate_result()
        self.lineEdit.setText(self.atk)

    # 日志
    def log(self, log_kind, log_text):
        if log_kind == 1:
            log_kind = '[INFO]'
        elif log_kind == 2:
            log_kind = '[WARNING]'
        elif log_kind == 3:
            log_kind = '[ERROR]'
        self.textEdit.append(
            log_kind + ' ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' %s' % log_text)

    # 清除全部buff内容
    def clear(self):
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.log(1, 'clear buff success')

    # 工具信息，展示窗口
    def about(self):
        self.about_gui.show()

    # 添加图片
    def add_image(self, servant_name):
        # 图片序号
        number = 0
        dirs = os.listdir('./data/servant')
        for file in dirs:
            if servant_name == re.sub('[0-9]+', '', file):
                number = re.findall("[0-9]+", file)[0]
                break
        dirs = os.listdir('./servant_logo')
        for file in dirs:
            if number == re.findall('[0-9]+', file)[0]:
                image = QtGui.QPixmap('./servant_logo/Servant%s.jpg' % number)
                self.label_17.setPixmap(image)
                break


# 关于信息子窗口
class AboutGUI(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(AboutGUI, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("关于")
        self.setWindowIcon(QtGui.QIcon('./fgo.png'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
