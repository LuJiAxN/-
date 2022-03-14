from collections import defaultdict

f = open("Q1_test.log","r")
lines = f.readlines()

#読み込んだログファイルをネストされた辞書に保存（形式は{"address1":{"time":[],"ping":[]},"address2":{"time":[],"ping":[]}}...）
logdata = defaultdict(lambda: defaultdict(list))

for l in range(len(lines)):
    line = lines[l].strip().split(',')
    t,address,p = line[0],line[1],line[2]
    logdata[address]['time'].append(t)#該当アドレス(dictory)に対応している日時をtimeのlistに保存
    logdata[address]['ping'].append(p)#該当アドレス(dictory)に対応している応答結果をpingのlistに保存

f.close()

#設問1
def question1(logdata):
    add = logdata.keys() #アドレスをdictoryから抽出

    for i in add:#アドレスごとに故障発生するかどうかを判断
        check_error = 0#該当アドレスは故障するかを判断する変数、0：故障なし/1：故障あり
        if logdata[i]['ping'].count('-'):
            n = len(logdata[i]['ping'])
            st = logdata[i]['ping'].index('-')#初めて'-'タイムアウト位置を検索
            output = logdata[i]['time'][st] + " ~ "#初めて'-'タイムアウト開始時間を保存
            ed = st + 1
            while st < n:#初めて'-'タイムアウト位置から応答結果リストの最後まで故障を検索
                if ed >= n:#最後までpingの応答がまだ返されない場合
                    output += "ログファイル最後までpingの応答がまだ返されないので、不明"
                    if check_error == 0:
                        print("故障状態のサーバアドレス：", i,"\n故障期間：")
                        print(output)
                        check_error = 1
                    else:
                        print(output)
                    break
                else:
                    if logdata[i]['ping'][ed] == '-':#次の日時は'-'タイムアウトかどうかを判断（連続）
                        ed += 1
                    else:
                        output += logdata[i]['time'][ed]
                        if check_error == 0:
                            print("故障状態のサーバアドレス：", i,"\n故障期間：")
                            print(output)
                            check_error = 1
                        else:
                            print(output)
                        if logdata[i]['ping'][ed+1:].count('-'):#次の'-'タイムアウトを検索
                            st = logdata[i]['ping'].index('-',ed+1)
                            ed = st + 1
                            output = logdata[i]['time'][st] + " ~ "
                        else:
                            break
        print("")




#設問1テスト
question1(logdata)

#チェック用(応答結果をリストにprint、連続数を直観的に確認できる)
'''
print("\n\nチェック用の応答結果")
add = logdata.keys()
for i in add:
    print(i,logdata[i]['ping'])
'''