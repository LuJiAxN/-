from collections import defaultdict

f = open("Q2_test.log","r")
lines = f.readlines()

#読み込んだログファイルをネストされた辞書に保存（形式は{"address1":{"time":[],"ping":[]},"address2":{"time":[],"ping":[]}}...）
logdata = defaultdict(lambda: defaultdict(list))

for l in range(len(lines)):
    line = lines[l].strip().split(',')
    t,address,p = line[0],line[1],line[2]
    logdata[address]['time'].append(t)#該当アドレス(dictory)に対応している日時をtimeのlistに保存
    logdata[address]['ping'].append(p)#該当アドレス(dictory)に対応している応答結果をpingのlistに保存

f.close()

#N回以上連続してタイムアウトした期間を抽出（"99999999999999"とは、ログファイルが終わったがpingの応答がまだ返されない場合、最後まで出ない意味）
def error_time(N,time,ping):
    error_time_list = []
    if ping.count('-'):
        n = len(ping)
        st = ping.index('-')
        cnt = 1  # 連続タイムアウトを計数
        output = time[st] + "~"
        ed = st + 1
        while st < n:
            if ed >= n:
                output += "99999999999999"
                if cnt >= N:
                    error_time_list.append(output)
                break
            else:
                if ping[ed] == '-':
                    ed += 1
                    cnt += 1
                else:
                    output += time[ed]
                    if cnt >= N:
                        error_time_list.append(output)
                    if ping[ed + 1:].count('-'):
                        st = ping.index('-', ed + 1)
                        ed = st + 1
                        cnt = 1  # 計数をリセット
                        output = time[st] + "~"
                    else:
                        break
    return error_time_list

#設問2
def question2(logdata,N):
    add = logdata.keys()

    for i in add:
        ping = logdata[i]["ping"]
        time = logdata[i]["time"]
        error_time_list = error_time(N,time,ping)
        if len(error_time_list) != 0 :
            print("故障状態のサーバアドレス：", i,"\n故障期間：")
            print(error_time_list)



#設問2テスト
N = int(input("Nの値を入力してください"))
question2(logdata,N)


#チェック用(応答結果をリストにprint、連続数を直観的に確認できる)
'''
add = logdata.keys()
for i in add:
    print(i,logdata[i]['ping'])
'''
