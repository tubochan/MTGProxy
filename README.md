# MTGProxy

MTGProxy is a software to make proxy card images of Magic: the gathering.
Please prepare MO format decklist or English cardlist.

# DEMO
You can make proxy images easily.
![image](https://user-images.githubusercontent.com/88754228/129301022-9941ea7c-dbab-4c4d-acee-ace5279d95e1.png)

# Features

- 

# Requirement

* Python 3.8.3
* requests(https://requests-docs-ja.readthedocs.io/en/latest/#)
* beautifulsoup4(https://pypi.org/project/beautifulsoup4/)
* PySimpleGUI(https://pysimplegui.readthedocs.io/en/latest/)
* mtgsdk(https://github.com/MagicTheGathering/mtg-sdk-python)

# Installation

```bash
pip install requests
pip install bs4
pip install PySimpleGUI
pip install mtgsdk
```

# Usage

```bash
python main.py
```

1. Use "テキスト読み込み" button to load your cardlist, or write your cardlist into "カードリスト" directory.
2. If you change directory to save proxy image, use "フォルダ指定" button. Default is "C:\Users\xxxxx\Pictures\MTGProxy".
3. Push "Proxy作成" button.
4. Wait until popup says "Finish!"

# Author

* tubochan
* [@tubo_chan_](https://twitter.com/tubo_chan_)

# License

MTGProxy is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
