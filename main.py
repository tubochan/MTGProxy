from mtgsdk import Card
import pickle
import urllib.request
import urllib.parse
import os
import PySimpleGUI as sg
import shutil
import requests
import bs4
import lxml
import time


# WisdomギルドからGatherを検索→mageUrl取得→Gatherから保存する関数
def search_wisdom_image(maisu, folderPath, cardname):
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


# MTGSDKのAPIカード検索→ImageUrl取得→Gatherから保存する関数
def search_SDK_image(maisu, folderPath, cardname):
    # カード名でAPI検索
    target_card = Card.where(name=cardname).all()
    # 見つかったカード名（4ED、5EDなど複数出てくる）それぞれでfor each
    for singleCard in target_card:
        if singleCard.foreign_names is not None:
            for singleLanguage in singleCard.foreign_names:
                if singleLanguage['language'] == 'Japanese' and singleLanguage['imageUrl'] is not None:
                    image_request = urllib.request.urlopen(singleLanguage['imageUrl'])
                    image_data = image_request.read()
                    out_file_name = singleLanguage['name'] + ".jpg"
                    print("{}".format(out_file_name))
                    os.makedirs(folderPath, exist_ok=True)
                    with open(folderPath + "\\"+ out_file_name, "wb") as out_file:
                        print(folderPath + "\\"+ out_file_name)
                        out_file.write(image_data)

                    if maisu >= 2:
                        # 枚数が2以上なら枚数増やしてコピー
                        for i in range(2, maisu+1):
                            copySakiName = singleLanguage['name'] + '(' + i + ').jpg'
                            print(folderPath+copySakiName)
                            shutil.copy(folderPath + "\\"+ out_file_name, folderPath+ "\\"+copySakiName)

                    #1枚でも見つかったらreturnで関数抜ける
                    return


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
    [sg.Listbox([],size=(100, 30), key='-LIST-')],
    [sg.Text('実行ログ')],
    [sg.Output(size=(100,7), key='-Log-')],
    [sg.Submit(button_text='実行'), sg.Submit(button_text='Wisdom'), sg.Submit(button_text='終了')]
]

# セクション 2 - ウィンドウの生成
window = sg.Window('MTG Proxy v0.1', layout)

# セクション 3 - イベントループ
while True:
    event, values = window.read()

    print(event)

    if event in (None, '終了'):
        print('exit')
        break

    if event == '-DECKFILE-':

        if os.path.exists(values['-DECKFILE-']):
            with open(values['-DECKFILE-'], mode='r') as f:
                data1 = f.read().split('\n')
                window['-LIST-'].update(data1)
                print('File loaded')
        else:
            print('File not found.')

    if event == '実行':
        # フォルダパス取得
        folderPath = values['-FOLDER-']

        # ポップアップ
        for singleLine in window['-LIST-'].GetListValues():
            splitedLine = singleLine.split(' ', maxsplit=1)
            if len(splitedLine) == 1 and splitedLine[0].isnumeric() == False:
                # 分割した要素が1つ＝カード名直接で数字でなければそのままカード名を使う
                search_SDK_image(1, folderPath, splitedLine[0])
            elif len(splitedLine) == 2 and splitedLine[0].isnumeric() == True:
                # 分割した要素が2つ＝枚数＆カード名なら枚数を使う
                search_SDK_image(int(splitedLine[0]), folderPath, splitedLine[1])
            window.refresh()

        print("Finish Create Proxy!")
        sg.popup("Finish!")

    if event == 'Wisdom':
        # フォルダパス取得
        folderPath = values['-FOLDER-']

        # ポップアップ
        for singleLine in window['-LIST-'].GetListValues():
            if singleLine != "":
                splitedLine = singleLine.split(' ', maxsplit=1)
                if len(splitedLine) == 1 and splitedLine[0].isnumeric() == False:
                    # 分割した要素が1つ＝カード名直接で数字でなければそのままカード名を使う
                    search_wisdom_image(1, folderPath, splitedLine[0])
                elif len(splitedLine) == 2 and splitedLine[0].isnumeric() == True:
                    # 分割した要素が2つ＝枚数＆カード名なら枚数を使う
                    search_wisdom_image(int(splitedLine[0]), folderPath, splitedLine[1])
                window.refresh()
                # Wisdomの負荷軽減のため3秒待機
                time.sleep(3)

        print("Finish Create Proxy!")
        sg.popup("Finish!")


# セクション 4 - ウィンドウの破棄と終了
window.close()


