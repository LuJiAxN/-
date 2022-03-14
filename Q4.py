from collections import defaultdict

f = open("Q4_test.log","r")
lines = f.readlines()

#読み込んだログファイルをネストされた辞書に保存（形式は{"address1":{"time":[],"ping":[]},"address2":{"time":[],"ping":[]}}...）
logdata = defaultdict(lambda: defaultdict(list))

for l in range(len(lines)):
    line = lines[l].strip().split(',')
    t,address,p = line[0],line[1],line[2]
    logdata[address]['time'].append(t)#該当アドレス(dictory)に対応している日時をtimeのlistに保存
    logdata[address]['ping'].append(p)#該当アドレス(dictory)に対応している応答結果をpingのlistに保存

f.close()

#サブネットマスクをバイナリに変換（例：24→11111111111111111111111100000000）
def mask_to_bin(mask):
    mask_tmp = []
    for i in range(32):
        mask_tmp.append("0")
    for i in range(int(mask)):
        mask_tmp[i] = ("1")
    mask_bin = "".join(mask_tmp)
    return mask_bin

#サーバアドレスをバイナリに変換（例：10.20.30.→11010000101000001111000000001）
def ip_to_bin(ip):
    ip_num = ip.split(".")
    x = 0
    for i in range(len(ip_num)):
        num = int(ip_num[i]) << (24 - i * 8)
        x = x | num
    ipbin = str(bin(x).replace("0b",""))
    return ipbin

#ip_aとip_bは同じサブネットに属しているかどうかを判断
def if_subnet(ip_a,ip_b,net_mask):
    ip_a_num = int(ip_to_bin(ip_a),2)
    ip_b_num = int(ip_to_bin(ip_b), 2)
    mask_bin = int(mask_to_bin(net_mask),2)
    if (ip_a_num & mask_bin) == (ip_b_num & mask_bin):
        return ip_a_num & mask_bin
    else:
        return 0

#サブネットの範囲を求める（例：10.20.30.1/16→10.20.0.0、0は0-255任意）
def subnet_ip(addr):
    mask = addr.split("/")[1]
    ip = addr.split("/")[0]
    ip_bin = int(ip_to_bin(ip),2)
    mask_bin = int(mask_to_bin(mask),2)
    sub = ip_bin & mask_bin
    subbin = str(bin(sub).replace("0b",""))
    subnet_ip = []
    i = len(subbin)
    while i > 0:
        j = i - 8
        if j < 0:
            j = 0
        x = subbin[j:i]
        x = str(int(x, 2))
        subnet_ip.append(x)
        i = i - 8
    subnet_ip = subnet_ip[::-1]
    subnet = ".".join(subnet_ip)
    return subnet

#サブネットを分類
def subnet_class(add):
    net_bel = [1 for i in range(len(add))]
    subnet = {}
    for i in add:
        addr1 = i
        subnet_name = subnet_ip(addr1)
        subnet[subnet_name] = []

    for i in range(len(add)):
        addr1 = add[i]
        if net_bel[i] != 0:
            subnet_name = subnet_ip(addr1)
            subnet[subnet_name].append(addr1)
            net_bel[i] = 0
            mask_i = int(addr1[addr1.index("/")+1:])
            ip_i = addr1[0:addr1.index("/")]
            for j in range(i+1,len(add)):
                addr2 = add[j]
                mask_j = int(addr2[addr2.index("/") + 1:])
                ip_j = addr1[0:addr1.index("/")]
                if mask_i == mask_j:
                    x = if_subnet(ip_i,ip_j,mask_i)
                    if x == 1:
                        subnet[subnet_name].append(addr2)
                        net_bel[j] = 0

    return subnet

#N回以上連続してタイムアウトした期間を抽出（"99999999999999"とは、ログファイルが終わったがpingの応答がまだ返されない場合、無限とみなす）
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

#サブネット内に二つのネットワークの故障期間を比較し、範囲を縮小、and 縮小した範囲とNに比較
def time_arrange(error_time1,error_time2,N):
    time_arr = []
    for i in range(len(error_time1)):
        et1 = error_time1[i]
        A = int(et1.split("~")[0])
        B = int(et1.split("~")[1])
        for j in range(len(error_time2)):
            et2 = error_time2[j]
            C = int(et2.split("~")[0])
            D = int(et2.split("~")[1])
            if B < C or D < A:
                continue
            else:
                mi = max(A,C)
                ma = min(B,D)
            if (ma - mi) / 99 >= N:
                t = str(mi) + "~" +str(ma)
                time_arr.append(t)
    return time_arr


def question4(N,logdata,subnet):
    add = logdata.keys()
    for i in add:
        time = logdata[i]["time"]
        ping = logdata[i]["ping"]
        logdata[i]["error_time"] = error_time(N, time, ping)
#各サブネット内にN回以上連続でタイムアウト期間を統合
    subnet_name = subnet.keys()
    for i in subnet_name:
        ip_add = subnet[i][0]
        error_time1 = logdata[ip_add]["error_time"]
        for k in range(1,len(subnet[i])):
            ip_add = subnet[i][k]
            error_time2 = logdata[ip_add]["error_time"]
            error_time1 = time_arrange(error_time1,error_time2,N)
        if len(error_time1) != 0 :
            print(i,"サブネットにネットワークの故障期間は",error_time1)
        else:
            print(i,"サブネットにネットワークは故障なし")


add = list(logdata.keys())
subnet = subnet_class(add)
print(subnet)

N = int(input("Nの値を入力してください"))
question4(N,logdata,subnet)

#チェック用(応答結果をリストにprint、連続数を直観的に確認できる)
'''
add = logdata.keys()
for i in add:
    print(i,logdata[i]['ping'])
'''
