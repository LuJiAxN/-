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

設問2
----
"Nの値を入力してください"を示している。

入力用のテストデータは、以下なので、連続する最大数は4で、1から5まで全パターンが含まれていると思う。　　

10.20.30.1/16 ['2', '-', '-', '-', '-', '14']
10.20.30.2/16 ['-', '-', '2', '7', '74', '-']
192.168.1.1/24 ['10', '8', '642', '-', '4', '24']
192.168.1.2/24 ['5', '15', '64', '-', '-', '-']
