#coding: utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pickle

# メニューに関する各種情報を取得する関数
def get_menu_data(soup, data):
    if data == "メニュー名":
        return soup.find("h4", class_="tt_clr_orange setmenutitle").text
    t = soup.find("img", alt=data).find_next("td")
    try:
        return [tag.text for tag in t.find_all("strong")]
    except:
        return "-"


def main():
    # メニュー一覧ページからそれぞれのメニューへのリンクを取得
    url = "http://gakushoku.coop/list_search.php"
    soup = BeautifulSoup(urlopen(url), "lxml")
    menu_links = []
    for a in soup.find_all("a"):
        menu_link = a.get("href")
        if menu_link and "menu_detail" in menu_link and menu_link not in menu_links:
            menu_links.append(menu_link)

    menus = []  # メニューの情報を保存するリスト
    base = "http://gakushoku.coop/"
    for i, menu_link in enumerate(menu_links):
        url = base+menu_link
        soup = BeautifulSoup(urlopen(url), "lxml")
        # メニューに関する情報を取得
        name = get_menu_data(soup, "メニュー名")
        price = get_menu_data(soup, "税込組価")
        calorie = get_menu_data(soup, "エネルギー量")
        allergen = get_menu_data(soup, "アレルギー物質")
        points = get_menu_data(soup, "3群点数")
        salt = get_menu_data(soup, "塩分")
        # 情報が入った辞書型オブジェクトを作り、リストに格納
        menus.append({"name": name, "price": price, "calorie": calorie,
                      "allergen": allergen, "points": points, "salt": salt})
        print("%03d/%d" % (i+1, len(menu_links)))
        time.sleep(1)  # サーバの負荷軽減のため
    # pickleとして保存
    with open("menus.pickle", "wb") as f:
        pickle.dump(menus, f)


if __name__ == '__main__':
    main()
