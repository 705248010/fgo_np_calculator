from np_effect_of_pre import *
import re


# 改一下宝具倍率的函数，改成传参（宝具等级，然后返回倍率）
class SelectServant:
    def __init__(self, servant_np_info, servant_atk_info, servant_level, rarity, _class, name):
        self.servant_np_info = servant_np_info
        self.servant_level = servant_level
        self.servant_atk_info = servant_atk_info
        self.rarity = rarity
        self._class = _class
        self.name = name

    # 根据宝具卡色和宝具等级，进行宝具倍率等值计算
    def np_multiplying_power(self, np_level):
        if '马修' in self.name:
            return ''
        if self.servant_np_info[0][0] == 'Arts':
            if self.servant_np_info[0][1] == '单体':
                return self.get_np_level_info()[np_level]
            elif self.servant_np_info[0][1] == '全体':
                return self.get_np_level_info()[np_level]
            else:
                pass
        elif self.servant_np_info[0][0] == 'Buster':
            if self.servant_np_info[0][1] == '单体':
                return self.get_np_level_info()[np_level]
            elif self.servant_np_info[0][1] == '全体':
                return self.get_np_level_info()[np_level]
            else:
                pass
        elif self.servant_np_info[0][0] == 'Quick':
            if self.servant_np_info[0][1] == '单体':
                return self.get_np_level_info()[np_level]
            elif self.servant_np_info[0][1] == '全体':
                return self.get_np_level_info()[np_level]
            else:
                pass

    # 对宝具前置效果进行计算
    def np_effect_of_pre(self):
        if '玛修·基列莱特' == self.name:
            return ''
        np_effect_of_pre = {}
        for i in range(len(self.servant_np_info)):
            for effect in effect_of_pre:
                # 把幅度进行保存
                if effect in self.servant_np_info[i][3]:
                    # print(self.servant_np_info[i][3])
                    np_effect_of_pre[self.servant_np_info[i][3]] = self.servant_np_info[i][4]
        return np_effect_of_pre

    # 一定注意一下马修的情况
    # 根据传入的从者等级，计算出atk
    def atk_transform(self):
        if '玛修·基列莱特' == self.name:
            return self.servant_atk_info[79]
        if self.servant_level == '满破':
            if self.rarity == '1':
                return self.servant_atk_info[59]
            elif self.rarity == '2':
                return self.servant_atk_info[64]
            elif self.rarity == '3':
                return self.servant_atk_info[69]
            elif self.rarity == '4':
                return self.servant_atk_info[79]
            elif self.rarity == '5':
                return self.servant_atk_info[89]
        elif self.servant_level == '90级':
            return self.servant_atk_info[89]
        elif self.servant_level == '100级':
            return self.servant_atk_info[99]

    # 返回计算结果
    def get_calculate_result(self):
        atk = self.atk_transform()
        effect = self.np_effect_of_pre()
        return atk, effect, self.get_class_additions()

    # 返回宝具等级对应的倍率
    def get_np_level_info(self):
        for i in range(len(self.servant_np_info)):
            if '敌方' in self.servant_np_info[i][3]:
                np_level_info = {
                    '1': self.servant_np_info[i][4],
                    '2': self.servant_np_info[i][5],
                    '3': self.servant_np_info[i][6],
                    '4': self.servant_np_info[i][7],
                    '5': self.servant_np_info[i][8],
                }
                return np_level_info

    # 返回职阶补正
    def get_class_additions(self):
        if self._class == 'Saber':
            return '1'
        elif self._class == 'Lancer':
            return '1.05'
        elif self._class == 'Archer':
            return '0.95'
        elif self._class == 'Rider':
            return '1'
        elif self._class == 'Caster':
            return '0.9'
        elif self._class == 'Assassin':
            return '0.9'
        elif self._class == 'Berserker':
            return '1.1'
        elif self._class == 'Ruler':
            return '1.1'
        elif self._class == 'Avenger':
            return '1.1'
        elif self._class == 'Mooncancer':
            return '1'
        elif self._class == 'AlterEgo':
            return '1'
        elif self._class == 'Foreigner':
            return '1'
        elif self._class == 'Shielder':
            return '1'
