import unittest


class CheckPro(unittest.TestCase):
    def check_output(self, expected, actual):
        """
        接口返回体(dict)通用校验方法
        :param expected: 期望值的协议，协议需要对齐接口文档中的数据结构。
        ①接口文档所描述的key需要对齐到数据结构体中；
        ②如果进行动态值的校验即校验数据类型，只需要把期望值key的值描述成类型，比方说  'order_id': int；
        ③如果进行精准值的校验，把值明确写在数据结构上即可，比方说 'order_id': '123'
        :param actual:返回体（json需转义dict）
        :return:
        """
        self.assertEqual(len(expected.keys()), len(actual.keys()), msg=f'{actual.keys()} object keys len inconsistent!')
        for key, value in expected.items():
            self.assertIn(key, actual.keys(), msg=f'{key} not in actual!')
            if isinstance(value, type):
                self.assertEqual(value, type(actual[key]), msg=f'{key} type inconsistent！')
            elif isinstance(value, dict):
                self.check_output(value, actual[key])
            elif isinstance(value, list):
                self.assertEqual(len(value), len(actual[key]), f'{actual.keys()} object items len inconsistent!')
                for list_index in range(len(value)):
                    if isinstance(value[list_index], type):
                        self.assertEqual(value[list_index], type(actual[key][list_index]),
                                         msg=f'{value[list_index]} type inconsistent！')
                    elif isinstance(value[list_index], dict):
                        self.check_output(value[list_index], actual[key][list_index])
                    else:
                        self.assertEqual(value[list_index], actual[key][list_index],
                                         msg=f'{value[list_index]} value inconsistent！')
            else:
                self.assertEqual(value, actual[key], msg=f'{key} value inconsistent！')


if __name__ == '__main__':
    # actual = {'responseTime': 0, 'webNotes': [
    #     {'noteId': 'noteid1723038523534', 'createTime': 1723037924397, 'star': 1, 'remindTime': 0, 'remindType': 0,
    #      'infoVersion': 1, 'infoUpdateTime': 1723037924397, 'groupId': '', 'title': 'title', 'summary': 'summary',
    #      'thumbnail': None, 'contentVersion': 1, 'contentUpdateTime': 1723037924616}]}
    a_actual = {'responseTime': 0, 'webNotes': 'abc'}
    except1 = ['responseTime', 'webNotes']
