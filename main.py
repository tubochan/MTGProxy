from mtgsdk import Card
import urllib.request
import urllib.parse
import os
import PySimpleGUI as sg
import shutil
import requests
import bs4
import time

def DECKFILE_func():
    """カード名ファイルが変更された際に呼び出される関数

    """    

    if os.path.exists(values['-DECKFILE-']):
        with open(values['-DECKFILE-'], mode='r') as f:
            #data1 = f.read().split('\n')
            data1 = f.read()
            window['-LIST-'].update(data1)
            print('File loaded.')
    else:
        print('File not found.')

def MTGSDK_func():
    """MTGSDKボタンを押したときに呼び出される関数
    """    

    # フォルダパス取得
    folderPath = values['-FOLDER-']

    # ポップアップ
    for singleLine in values['-LIST-'].split("\n"):
        if singleLine != "":
            splitedLine = singleLine.split(maxsplit=1)
            if len(splitedLine) == 1 and splitedLine[0].isnumeric() == False:
                # 分割した要素が1つ＝カード名直接で数字でなければそのままカード名を使う
                search_SDK_image(folderPath, splitedLine[0], 1)
            elif len(splitedLine) == 2 and splitedLine[0].isnumeric() == True:
                # 分割した要素が2つ＝枚数＆カード名なら枚数を使う
                search_SDK_image(folderPath, splitedLine[1],int(splitedLine[0]))
            window.refresh()
            # SDKの負荷軽減のため1秒待機
            time.sleep(1)

    print("Finish Create Proxy!")
    sg.popup("Finish!")

def WISDOM_func():
    """WISDOMボタンを押したときに呼び出される関数
    """    

    # フォルダパス取得
    folderPath = values['-FOLDER-']

    # ポップアップ
    for singleLine in values['-LIST-'].split("\n"):
        if singleLine != "":
            splitedLine = singleLine.split(maxsplit=1)
            if len(splitedLine) == 1 and splitedLine[0].isnumeric() == False:
                # 分割した要素が1つ＝カード名直接で数字でなければそのままカード名を使う
                search_wisdom_image(folderPath, splitedLine[0], 1)
            elif len(splitedLine) == 2 and splitedLine[0].isnumeric() == True:
                # 分割した要素が2つ＝枚数＆カード名なら枚数を使う
                search_wisdom_image(folderPath, splitedLine[1],int(splitedLine[0]))
            window.refresh()
            # Wisdomの負荷軽減のため3秒待機
            time.sleep(3)

    print("Finish Create Proxy!")
    sg.popup("Finish!")

def search_wisdom_image(folderPath, cardname,maisu) :
    """WisdomギルドからGatherを検索→ImageUrl取得→Gatherから保存する関数

    Args:
        folderPath (str): 保存フォルダパス
        cardname (str): カード名：英語表記
        maisu (int): カード枚数
    """
    base_url = 'http://whisper.wisdom-guild.net/card/'
    wisdom_url = base_url+urllib.parse.quote(cardname)
    wisdom_response = requests.get(wisdom_url)
    wisdom_response.raise_for_status()
    # print(str(wisdom_response.text))
    wisdom_soup = bs4.BeautifulSoup(wisdom_response.text, 'lxml')

    # Wisdomカード名から日本語名を取得
    pass

    # Wisdomのカード検索画面右下の多言語テーブルをひっぱる
    elements = wisdom_soup.select("table#card_detail_language>tr")

    for singleElement in elements:
        TRelement = bs4.BeautifulSoup(str(singleElement), 'lxml')
        TDelements = TRelement.select("td")
        if TDelements[0].text == "日本語":
            # print(TDelements[1].select_one("a").get("href"))
            multiVerseID = str(TDelements[1].select_one("a").get("href")).replace("http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=", "")
            # print(multiVerseID)

            #得られたマルチバースIDからURLを生成し画像取得
            image_request = urllib.request.urlopen("https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + multiVerseID + "&type=card")
            image_data = image_request.read()
            out_file_name = cardname + ".jpg"
            print("{}".format(out_file_name))
            os.makedirs(folderPath, exist_ok=True)
            with open(folderPath + "\\" + out_file_name, "wb") as out_file:
                out_file.write(image_data)

            if maisu >= 2:
                # 枚数が2以上なら枚数増やしてコピー
                for i in range(2, maisu+1):
                    copySakiName = cardname + '(' + str(i) + ').jpg'
                    print(folderPath + "\\" + copySakiName)
                    shutil.copy(folderPath + "\\" + out_file_name, folderPath + "\\" + copySakiName)

            # 1枚でも見つかったらreturnで関数抜ける
            return

    # 日本語画像が見つかれなければGatherのURLから画像へ
    gatherElement = wisdom_soup.select_one('a[href^="http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid="]')
    # print(gatherElement.get("href"))
    multiVerseID = gatherElement.get("href").replace( "http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=", "")

    # 得られたマルチバースIDからURLを生成し画像取得
    image_request = urllib.request.urlopen(
        "https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + multiVerseID + "&type=card")
    image_data = image_request.read()
    out_file_name = cardname + ".jpg"
    print("{}".format(out_file_name))
    os.makedirs(folderPath, exist_ok=True)
    with open(folderPath + "\\" + out_file_name, "wb") as out_file:
        out_file.write(image_data)

    if maisu >= 2:
        # 枚数が2以上なら枚数増やしてコピー
        for i in range(2, maisu+1):
            copySakiName = cardname + '(' + str(i) + ').jpg'
            print(folderPath + "\\"  + copySakiName)
            shutil.copy(folderPath + "\\" + out_file_name, folderPath + "\\" + copySakiName)


def search_SDK_image(folderPath, cardname,maisu):
    """MTGSDKのAPIカード検索→ImageUrl取得→Gatherから保存する関数

    Args:
        folderPath (str): 保存フォルダパス
        cardname (str): カード名：英語表記
        maisu (int): カード枚数
    """
    # カード名でAPI検索
    target_cards = Card.where(name=cardname).all()
    # 見つかったカード名（4ED,5EDなど複数出てくる）それぞれでfor each
    for singleCard in target_cards:
        # 部分一致で検索にひっかかる（The Abyss→Magus of the Abyssもひっかかる）のでカード名完全一致も見る
        if singleCard.name == cardname:
            # 見つかったカード名にforeign_names要素があればそれをfor eachで深堀り
            if singleCard.foreign_names is not None:
                for singleLanguage in singleCard.foreign_names:
                    # 日本語が見つかって、imageUrlが出てくれば日本語画像を取得
                    if singleLanguage['language'] == 'Japanese' and singleLanguage['imageUrl'] is not None:
                        # 画像保存する関数を使って保存
                        save_image_by_url(folderPath, singleLanguage['imageUrl'], cardname, maisu)

                        #1枚でも見つかったらreturnで関数抜ける
                        return
    
    # 日本語カード名が見つからなかった場合ここ
    # 再度for eachで検索結果をループ
    for singleCard in target_cards:
        # 部分一致で検索にひっかかる（The Abyss→Magus of the Abyssもひっかかる）のでカード名完全一致も見る
        if singleCard.name == cardname:
            # 最初に見つかった画像を保存、なぜかcards直下はimage_urlになるので表記変更
            save_image_by_url(folderPath, singleCard.image_url, cardname, maisu)
            # returnで関数抜ける
            return

    # 英語カード名も見つからなかった場合ここ
    # エラーメッセージを表示して終了
    print(cardname + "は見つかりませんでした")

def save_image_by_url(folderPath, imgUrl, cardname, maisu):
    """imgUrlの画像をfolderPathにcardnameの名前でmaisu分だけ保存する関数

    Args:
        folderPath (str): 保存フォルダパス
        imgUrl (str): 画像URL
        cardname (str): カード名：英語表記
        maisu (int): カード枚数
    """

    image_request = urllib.request.urlopen(imgUrl)
    image_data = image_request.read()
    out_file_name = cardname + ".jpg"
    print("{}".format(out_file_name))
    os.makedirs(folderPath, exist_ok=True)
    with open(folderPath + "\\"+ out_file_name, "wb") as out_file:
        print(folderPath + "\\"+ out_file_name)
        out_file.write(image_data)

    if maisu >= 2:
        # 枚数が2以上なら枚数増やしてコピー
        for i in range(2, maisu+1):
            out_file_name = cardname + "(" + str(i) + ").jpg"
            print("{}".format(out_file_name))
            with open(folderPath + "\\"+ out_file_name, "wb") as out_file:
                print(folderPath + "\\"+ out_file_name)
                out_file.write(image_data)


# ～～～関数記述ここまで～～～

# ～～～MAIN部ここから～～～
#  セクション1 - オプションの設定と標準レイアウト
sg.theme('Dark Blue 3')

layout = [
    [sg.Text('MTG Proxy')],
    [
        sg.Text('カード名ファイル', size=(15, 1)),
        sg.InputText('テキストファイル名', key='-DECKFILE-', enable_events=True),
        sg.FileBrowse('テキスト読み込み', key='-FILES-', file_types=(('MO形式テキストファイル', ('*.txt', '*.dek')),))
    ],
    [sg.Text('出力先フォルダ', size=(15, 1)), sg.InputText('./image', key='-FOLDER-'), sg.FolderBrowse('フォルダ指定')],
    [sg.Text('カードリスト', size=(15, 1))],
    [sg.Multiline(size=(100, 30), key='-LIST-')],
    [sg.Text('実行ログ')],
    [sg.Output(size=(100,7), key='-Log-')],
    # [sg.Submit(button_text='MTGSDK'), sg.Submit(button_text='Wisdom'), sg.Submit(button_text='終了')]
    [sg.Submit(button_text='MTGSDK'), sg.Submit(button_text='終了')]
]

# セクション 2 - ウィンドウの生成
window = sg.Window('MTG Proxy v0.10', layout)

# セクション 3 - イベントループ
# ハンドラ設定
handler = {
    '-DECKFILE-': DECKFILE_func,
    'MTGSDK': MTGSDK_func,
    'Wisdom': WISDOM_func,
}

while True:
    event, values = window.read()

    print(event, values)

    if event in (None, '終了'):
        print("exit")
        break
        
    function = handler[event]  # handlerからeventに応じた関数を呼び出す
    function()

# セクション 4 - ウィンドウの破棄と終了
window.close()


