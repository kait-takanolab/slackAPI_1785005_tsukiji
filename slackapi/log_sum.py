# -*- coding: utf-8 -*-
#各チャンネルのログを統合し、まとめたログの作成
import codecs,json,csv,glob
from datetime import datetime

#フォルダcsv内にあるすべてのcsvファイルを取得する。
files = []
files = glob.glob('../json/20180419/*.json')

fm = codecs.open("memberlist.json","r","utf-8")
memberlist = json.load(fm)


def append_index(index, username, text, ts, date_ts):
    index.append([username, text, ts, date_ts])

def search_nameindex(username):
    for i in memberlist:
        if (username in i["id"]) == True:
            name = i["name"]
    return name

def loggets(logfile, logs):
    try:
        for i in logfile:
            if ('user' in i ) and ( 'text' in i ):
                name = search_nameindex(i['user'])
                append_index(logs, name, i['text'], float(i['ts']), datetime.fromtimestamp(float(i["ts"])))
                continue

            elif ('user' not in i ) or ('text' not in i):
                if 'bot_id' in i: 
                    append_index(logs, i['bot_id'], i['text'], float(i['ts']), datetime.fromtimestamp(float(i["ts"])))         
                    continue

                if 'comment' in i:
                    name = search_nameindex(i['comment']['user'])
                    #print(i['comment']['user'], i['comment']['comment'], i['comment']['timestamp'])
                    append_index(logs, name, i['comment']['comment'], float(i['comment']['timestamp']), datetime.fromtimestamp(float(i['comment']['timestamp'])))
                    continue

    # 起こりそうな例外をキャッチ
    except FileNotFoundError as e:
        print(e)

#まだ一応残しておく
    '''
    if(i.get("subtype") == "file_share"):
        continue
    elif(i.get("subtype") == "bot_add"):
        continue
    elif(i.get("subtype") == "bot_message"):
        username = i["bot_id"]
        for at in i["attachments"]:
            s_text = at["text"]
    elif(i.get("subtype") == "file_comment"):
        for j in memberlist:
            if (i['comment']['user'] in j["id"]) == True:
                username = j["name"]
                s_text = i["comment"]["comment"]
    else:           
        for j in memberlist:
            if (i['user'] in j["id"]) == True:
                username = j["name"]
                s_text = i["text"]
    sumlog.append([username, s_text, float(i["ts"]), datetime.fromtimestamp(float(i["ts"]))])
    '''
    

if __name__ == '__main__':
    #csvファイルに発言、時間、人のデータを書き込む
    #member.jsonでユーザ名に変換
    logs = []
    for f in files:
        # ログのJSONファイルの読み込み
        fl = codecs.open(f, "r", "utf-8")
        f_json = json.load(fl)
        loggets(f_json['messages'],logs)

    print(logs)


    '''
    sumlog = sorted(sumlog, key=lambda x:(x[0],x[2]))

    with open('slacklog.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow(['User', 'text', 'timestamp', 'time'])
        for i in sumlog:
            writer.writerow([i[0], i[1], i[2], i[3]])
    '''