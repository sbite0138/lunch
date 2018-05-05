#coding: utf-8
import pickle
from copy import deepcopy
# 点数同士の足し算にはdecimalを使う（floatだと結果に誤差がでたので）
from decimal import Decimal


# 3群点数同士を足し算する関数
def add(a, b):
    ret = [Decimal(a[0])+Decimal(b[0]), Decimal(a[1]) +
           Decimal(b[1]), Decimal(a[2])+Decimal(b[2])]
    return ret


# ある3群点数の各数値が別の３群点数以下であるかを返す関数
def is_lower(a, b):
    return a[0] <= b[0] and a[1] <= b[1] and a[2] <= b[2]


def main():
    # pickle化したmenusを復元
    with open("menus.pickle", "rb") as f:
        menus = pickle.load(f)
    # menusを黄色の点数順にソート
    menus.sort(key=lambda x: float(x["points"][2]))
    # 検索結果を格納する辞書
    table = {}
    table.update({repr([0.0, 0.0, 0.0]): [[0.0, 0.0, 0.0], [[]]]})
    loop_count = 0
    is_changed = True
    while is_changed:
        is_changed = False
        copied_table = deepcopy(table)
        for values in copied_table.values():
            current_points = values[0]  # 現在注目している要素の3群点数
            lunches = values[1]  # 上の3群点数になる学食
            for lunch in lunches:
                for menu in menus:
                    # menusをソートしているので、現在のmenuとcurrent_pointsの黄点の和が7.0を超えたらそれ以降は考えなくてもいい。
                    if add(current_points, menu["points"])[2] > 7.0:
                        break
                    # menuが現在の学食でまだ選択されておらず、学食とメニューの3群点数の和が目安よりも少ないなら
                    if menu["name"] not in lunch and is_lower(add(current_points, menu["points"]), [2.0, 1.0, 7.0]):
                        # 現在の学食にmenuを加えて新しい学食を作る
                        copied_lunch = deepcopy(lunch)
                        copied_lunch.append(menu["name"])
                        copied_lunch.sort()
                        # 新しい学食の3群点数を計算する
                        points = add(current_points, menu["points"])
                        key = repr(points)
                        # tableを更新
                        if key not in table:
                            table.update({key: [points, [copied_lunch]]})
                            is_changed = True
                        else:
                            if copied_lunch not in table[key][1]:
                                table[key][1].append(copied_lunch)
                                is_changed = True
        loop_count += 1
        # 一回のループごとに結果を保存する
        with open("result%02d.txt" % loop_count, "w") as f:
            if "[Decimal('2.0'), Decimal('1.0'), Decimal('7.0')]" in table:
                f.write(
                    repr(table["[Decimal('2.0'), Decimal('1.0'), Decimal('7.0')]"]))
            else:
                f.write("None")
            print("saved:result%02d.txt" % loop_count)


if __name__ == '__main__':
    main()
