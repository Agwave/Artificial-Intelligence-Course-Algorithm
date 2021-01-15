

def first_feature():
    """
    选择特征确定动物类别
    :return: 动物类别: int
    """
    print('1恒温且有脊椎；2有羽毛且卵生；3有鳞片/角质层且三心室')
    choice = input('请选择特征')
    return int(choice)

def specific_feature(choice):
    """
    输入动物类别，再选择动物特征，确定具体动物类别
    :param choice: int
    :return: 具体动物: str
    """
    if choice == 1:
        mammal()
    elif choice == 2:
        bird()
    elif choice == 3:
        reptile()
    else:
        print('输入无效，无法确定动物类别')

def mammal():
    """
    确定是哺乳动物，继续选择特征，确定具体动物
    :return: 无
    """
    print('该动物是哺乳动物')
    print()
    print('1能捕鼠；2有黑色斑点；3生活在海洋')
    choice = int(input('请继续从上面特征中进行选择'))
    if choice == 1:
        print('该动物是猫')
    elif choice == 2:
        print('该动物是豹')
    elif choice == 3:
        print('该动物是鲸')
    else:
        print('输入无效，无法确定具体动物')

def bird():
    """
    确定是鸟类，继续选择特征，确定具体动物
    :return: 无
    """
    print('该动物是鸟类动物')
    print()
    print('1羽毛艳丽；2雌雄成对；3乌黑羽毛')
    choice = int(input('请继续从上面特征中进行选择'))
    if choice == 1:
        print('该动物是孔雀')
    elif choice == 2:
        print('该动物是鸳鸯')
    elif choice == 3:
        print('该动物是乌鸦')
    else:
        print('输入无效，无法确定具体动物')

def reptile():
    """
    确定是爬行动物，继续选择特征，确定具体动物
    :return: 无
    """
    print('该动物是爬行动物')
    print()
    print('1无四肢；2体背腹扁平；3有甲壳')
    choice = int(input('请继续从上面特征中进行选择'))
    if choice == 1:
        print('该动物是蛇')
    elif choice == 2:
        print('该动物是壁虎')
    elif choice == 3:
        print('该动物是乌龟')
    else:
        print('输入无效，无法确定具体动物')

if __name__ == '__main__':
    choice = first_feature()
    specific_feature(choice)
