フィックスポイントプログラミング試験
====
Python3.9.2　　

各設問1,2,3,4は、それぞれQ1.py, Q2.py, Q3.py, Q4,pyに対応している。　　

テストデータも名前に応じて各設問に対応している。（Q1_test.log→Q1.py）　　

.pyファイルを直接に実行する。プログラム内にログファイル自動的に読み込む。　　

プログラムはQ1,2,3,4を完成した。　　

データ保存方式
--------
読み込んだログファイルをネストされた辞書に保存　　

（形式は{"address1":{"time":[],"ping":[]},"address2":{"time":[],"ping":[]}}...）　　

該当アドレスのtimeリストとpingリストを処理する　　

結果の正しさを確認について
--------
各プログラムの最後に、#チェック用(応答結果をリストにprint、連続数を直観的に確認できる)''' ... ''''　部分を追加した。　　

'''を消して、サーバアドレスごとにpingの応答結果を直観的に順にリストで確認できる

設問1
----
保存されたデータ(logdata)から、サーバアドレスごとにpingの応答結果リストを確認。　　

含まれていない場合は故障なし。`-`を含まれている場合故障期間の判断を開始（開始位置はst）。

次の応答結果(ed = st + 1)は`-`かどうかを判断した上で、故障期間を確認。　　

一回の故障を確認した後は、次の`-`位置を探し、開始位置をもう一度stに設定、最後まで繰り返し。　　

注：ログファイル最後記録されたその回は、`-`の場合、次にpingの応答がいつ返るのはわからないので、故障期間を"ログファイル最後までpingの応答がまだ返されないので、不明"として出力する。　　

入力用のテストデータは、以下になる。　　

10.20.30.1/16 ['2', '-', '-', '-', '58', '14']　　

10.20.30.2/16 ['-', '1', '2', '7', '74', '-']　　

192.168.1.1/24 ['10', '8', '642', '-', '4', '24']　　

192.168.1.2/24 ['5', '15', '64', '54', '-', '-']


設問2
----
"Nの値を入力してください"を示している。

入力用のテストデータは、連続する最大数は4で、入力は1から5まででは、全パターンが含まれていると思う。　　

Q2は、N回以上連続してタイムアウトした期間を抽出する機能を関数として作成した。　　

ここでは、前問と違って、ログファイル最後記録されたその回は、`-`の場合が、"99999999999999"を記録されている。原因としては、Q4の各サブネット毎にネットワークの連続数を数えるためで、ここにログファイルが終わったがpingの応答がまだ返されない場合を無限大に設定した。意味は、Q1と同じで、次にpingの応答がいつ返るのはわからない。　　

Q1のプログラムを拡張してカウンター変数（cnt）を使用し、Nと比較して故障期間を判断する。　　

最後N回以上連続してタイムアウトしたサーバと期間を出力する。

入力用のテストデータは、以下に添付する。　　

10.20.30.1/16 ['2', '-', '-', '-', '-', '14']　　

10.20.30.2/16 ['-', '-', '2', '7', '74', '-']　　

192.168.1.1/24 ['10', '8', '642', '-', '4', '24']　　

192.168.1.2/24 ['5', '15', '64', '-', '-', '-']　　

設問3
----
"mの値を入力してください"と"tの値を入力してください"を示している。　　

私から結果を確認用のm,tは3，300です。

Q2は、`-`を返すpingの応答時間が長すぎとみますので、`-`を含まれている直近m回の平均応答時間を直接にtミリ秒を超えたことに判断する。　　

期間をm回に限定されたので、出力した過負荷状態となっている期間は、重複がある。例えば、時刻2が`-`すると、m = 3 の場合、時刻1→3 ,2→4両方出力された。　　

m回以内で`-`を含まれていない場合は、m回のping応答結果を累加して、平均値を算出して、tと比較した上で、過負荷状態となっている期間を判断する。

最後過負荷状態となっているサーバと期間を出力する。

入力用のテストデータは、以下に添付する。　

10.20.30.1/16 ['2', '-', '-', '-', '58', '14']　　

10.20.30.2/16 ['-', '1', '2', '7', '74', '-']　　

192.168.1.1/24 ['10', '26', '642', '504', '4', '24']　　

192.168.1.2/24 ['5', '15', '64', '54', '-', '-']

設問4
----
"Nの値を入力してください"を示している。

サブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）同時刻の連続数を3まで設定されているので、入力は2から4まででは、全パターンが含まれていると思う。　　

入力のデータについて、サブネット内のサーバ数を3台に増加した。　　

Q4のプログラムは、7個の関数を作成した。　　

5個は、サブネットの算出に関する関数です。

mask_to_bin関数は、"10.20.30.1/16"の16サブネットマスクをバイナリに変換する目的です。（例：24→11111111111111111111111100000000）　　　

ip_to_bin関数は、"10.20.30.1/16"のサーバアドレスをバイナリに変換する目的です。（例：10.20.30.1→11010000101000001111000000001）　　　　

if_subnet関数は、二つのipアドレスは同じサブネットに属しているかどうかを判断する機能です。　　

subnet_ip関数は、サブネットの範囲を求める目的です。（例：10.20.30.1/16→10.20.0.0、0は0-255任意）最後出力されたサブネットを代表する意味です。　　

subnet_class関数は、サブネットをグループに分けている機能です。同じサブネットに属しているかどうかを判断した上で、グループを分ける。　　

それ以外のerror_time関数は、Q2抽出された機能（N回以上連続してタイムアウトした期間を判断と抽出）です。

time_arrange関数は、サブネット内に二つのネットワークの故障期間を比較して、期間範囲を縮小する目的です。縮小した範囲もNに比較する必要がある。ここには、入力のデータをサーバごとに確認日時の差が固定するように考えられる。（20201019133124→20201019133224、差が1分を固定）なので、最後縮小した範囲の差を99（100であれば、サブネット内にネットワークも差があるので、結果が間違い）で割って、Nに比較する。　　

最後各サブネット毎にネットワークの故障期間を出力する。ネットワーク故障なしの場合、"故障なし"を出力する。


入力用のテストデータは、以下に添付する。　

10.20.30.1/16 ['2', '-', '-', '-', '58', '14']　　

10.20.30.2/16 ['-', '-', '-', '-', '74', '-']　　

10.20.30.3/16 ['98', '-', '-', '-', '-', '-']　　

192.168.1.1/24 ['10', '8', '642', '-', '-', '24']　　

192.168.1.2/24 ['5', '15', '64', '-', '-', '-']　　

192.168.1.3/24 ['5', '15', '-', '-', '-', '-']　　
