from collections import defaultdict

f = open("Q3_test.log","r")
lines = f.readlines()

#読み込んだログファイルをネストされた辞書に保存（形式は{"address1":{"time":[],"ping":[]},"address2":{"time":[],"ping":[]}}...）
logdata = defaultdict(lambda: defaultdict(list))

for l in range(len(lines)):
    line = lines[l].strip().split(',')
    t,address,p = line[0],line[1],line[2]
    logdata[address]['time'].append(t)#該当アドレス(dictory)に対応している日時をtimeのlistに保存
    logdata[address]['ping'].append(p)#該当アドレス(dictory)に対応している応答結果をpingのlistに保存

f.close()


#設問3
def question3(logdata,m,t):
    add = logdata.keys()

    for i in add:
        check_over = 0
        n = len(logdata[i]['ping'])
        st = 0
        output = logdata[i]['time'][st] + " ~ "
        ed = st + m - 1
        while st <= n - m:
            ping_sum = 0
            output_check = 0
            for j in range(st,ed+1):
                if logdata[i]['ping'][j] == '-':#'-'タイムアウトを含めている時に、直接過負荷状態に判断
                    output += logdata[i]['time'][ed]
                    if check_over == 0:
                        print("サーバ",i,"過負荷状態となっている期間：")
                        print(output)
                        check_over = 1
                        output_check = 1
                    else:
                        print(output)
                        output_check = 1
                    break
                else:
                    ping_sum += int(logdata[i]['ping'][j])
            if output_check != 1 and ping_sum / m > t:#'-'を含めていない場合に、平均応答時間を判断
                output += logdata[i]['time'][ed]
                if check_over == 0:
                    print("サーバ",i, "過負荷状態となっている期間：")
                    print(output)
                    check_over = 1
                else:
                    print(output)
            st += 1
            ed = st + m - 1
            output = logdata[i]['time'][st] + " ~ "

        print("")




#設問3テスト
m = int(input("mの値を入力してください"))
t = int(input("tの値を入力してください"))
question3(logdata,m,t)


#チェック用(応答結果をリストにprint、連続数を直観的に確認できる)
'''
print("\n\nチェック用の応答結果")
add = logdata.keys()
for i in add:
    print(i,logdata[i]['ping'])
'''