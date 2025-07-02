from django.shortcuts import render,redirect
import io
import csv
from django.http import HttpResponse
from .models import Master,Trade_hinban,Trade_kyoten
import urllib.parse
from django.contrib import messages
from .forms import Masterform
from django.http import JsonResponse



def index(request):
    messages.warning(request,"変換するCSVを選択してください。")
    return render(request,"csv_app/index.html")


def csv_import(request):

    if 'csv2' in request.FILES:

        #------読込-------
        data = io.TextIOWrapper(request.FILES['csv2'].file , encoding="cp932")
        csv_content = csv.reader(data)
        header=next(csv_content)

        csv_list=list(csv_content)

        #------キープ用CSVに対応（発注用：14項目、キープ用：11項目）------
        if len(csv_list[0]) != 14:
            for i in csv_list:
                i+=["","",""]

        #------HTMLへ------
        dict={}
        i=0

        for line in csv_list:
            dict[i]={
                "hinmei":line[1],
                "num":line[6],
                "sku":line[8],
            }
            i+=1
        
        mitsumori=csv_list[0][7]


        #------出力項目準備(リストの中身)------
        file=request.FILES['csv2']
        filename=str(file)
        maker_list=["キャブ(株)","トムス(株)","フェリック(株)","(株)ボンマックス","株式会社松栄シルク","(株)トレードワークス"]

        if ("KeepOrder" in filename and request.POST["メーカー"]=="(株)トレードワークス") or (filename.split("_")[0]=="(株)トレードワークス" and filename.split("_")[1]=="顧客指定" ):
            file="(株)トレードワークス在庫確認専用.csv"
            filename="(株)トレードワークス在庫確認_株式会社プラスワンインターナショナル 物流センター"
            select_maker="(株)トレードワークス"
        else:
            if not filename.split("_")[0] in maker_list:
                select_maker=request.POST["メーカー"]
            else:
                select_maker=filename.split("_")[0]
        

        #--- エラー表示用 ---
        flag=True
        err=[]

        if select_maker=="キャブ(株)":
            maker="CAB"
            ex_csv=[]
 
            for line in csv_list:
                if len(list(Master.objects.filter(jan=line[8]))) == 0:
                    err.append(line[8])
                    flag=False

            if flag == True:
                for line in csv_list:
                    item=Master.objects.get(jan=line[8])
                    a=[str(item.hinban)+"0"+str(item.kataban),line[3],line[5],line[6]]
                    ex_csv.append(a)
                    print(item.hinban,item.kataban,item.jan)
                

        elif select_maker == "トムス(株)":
            maker="TOMS"
            ex_csv=[["品番(5桁)","カラーコード","サイズコード","数量","備考（納品書・出荷案内書の行備考）","お客様注文Ｎｏ．"]]

            for line in csv_list:

                if "-" in line[0]:
                    hinban=line[0].split("-")[0]
                else:
                    hinban=line[0]
                
                a=[hinban,line[3],line[5],line[6],line[11][:20],line[7]]
                ex_csv.append(a)


        elif select_maker == "フェリック(株)":
            maker="フェリック"
            ex_csv=[]

            for line in csv_list:
                a=[line[0],line[3],line[5],line[6]]
                ex_csv.append(a)


        elif select_maker == "(株)ボンマックス":
            maker="ボンマックス"
            ex_csv=[["品番","カラー","サイズ","数量","明細摘要"]]

            for line in csv_list:
                a=[line[0],line[3],line[5],line[6],line[11][:20]]
                ex_csv.append(a)


        elif select_maker == "株式会社松栄シルク":
            maker="松栄シルク"
            ex_csv=[]

            for line in csv_list:
                a=[line[0],str(line[3]).zfill(3),str(line[5]).zfill(3),line[6]]
                ex_csv.append(a)


        elif select_maker=="(株)トレードワークス":
            maker="トレードワークス"
            ex_csv=[["品番","数量","お届け先会社名","お届け先会社名カナ","部署名","お届け先名（姓）","お届け先名（名）",
            "お届け先郵便番号","お届け先都道府県","お届け先住所1","お届け先住所2","お届け先電話番号","お客様注文番号","荷主名","荷主電話番号","備考"]]
            trade_flag1=True
            trade_flag2=True

            #商品判断
            for line in csv_list:
                if len(list(Trade_hinban.objects.filter(jan=line[8]))) == 0:
                    err.append(line[8])
                    flag=False
                    trade_flag1=False

            #加工場判断
            kakou_name=filename.split("_")[1]
            if len(list(Trade_kyoten.objects.filter(name=kakou_name))) == 0:
                flag=False
                trade_flag2=False

            #CSV作成
            if flag == True:
                
                kakou_send=Trade_kyoten.objects.get(name=kakou_name)

                for line in csv_list:
                    item=Trade_hinban.objects.get(jan=line[8])
                    a=[
                        item.hinban, #品番
                        line[6], #数量
                        kakou_send.company, #会社名
                        "", #会社名カナ
                        "", #部署
                        kakou_send.sei, #姓
                        kakou_send.mei, #名
                        kakou_send.yubin, #郵便番号
                        kakou_send.pref, #都道府県
                        kakou_send.address1, #住所1
                        kakou_send.address2, #住所2
                        kakou_send.tel, #電話番号
                        line[7], #注文番号
                        kakou_send.ninushi_name, #荷主名
                        kakou_send.ninushi_tel, #荷主電話
                        "", #備考
                        ]
                    ex_csv.append(a)

        # else:
        #     messages.error(request,"対応していないメーカーのCSVが選択されています！")
        #     return render(request,"csv_app/index.html",{"filename":filename})



        #-----------------
        #最終結果
        #-----------------
        if flag == True:
            reset="OK"
            messages.success(request,"変換後のCSVをダウンロードしました！")

            #------セッション-----
            request.session["csv_list"]={"file":str(file),"csv":ex_csv}

        else:
            reset="NO"
            err_mess="マスタに登録されていない商品が含まれています！"

            if maker=="トレードワークス":
                if trade_flag1 == False and trade_flag2 == True:
                    err_mess="マスタに登録されていない商品が含まれています！"
                elif trade_flag1 == True and trade_flag2 == False:
                    err_mess="ファイル名に登録されていない加工場が含まれています！"
                elif trade_flag1 == False and trade_flag2 == False:
                    err_mess="マスタに登録されていない商品が含まれています！ファイル名に登録されていない加工場が含まれています！"

            messages.error(request,err_mess)


        

        return render(request,"csv_app/index.html",
            {
            "dict":dict,
            "mitsumori":mitsumori,
            "maker":maker,
            "reset":reset,
            "filename":filename,
            "err":err,
            }
            )

    
    else:
        return redirect('index')



def csv_export(request):
    csv_list=request.session.get("csv_list")
    file_name=csv_list["file"]
    ex_csv=csv_list["csv"]

    quoted_filename = urllib.parse.quote("変換_" + file_name)

    del request.session["csv_list"]

    response = HttpResponse(content_type='text/csv; charset=CP932')
    response['Content-Disposition'] =  "attachment;  filename='{}'; filename*=UTF-8''{}".format(quoted_filename, quoted_filename)
    
    writer = csv.writer(response)
    for line in ex_csv:
        writer.writerow(line)
    return response


def master_kanri(request):
    form2 = Masterform()
    return render(request,"csv_app/master.html",{"form2":form2})



def master(request):
    form2 = Masterform()
    
    if 'csv' in request.FILES:
        data = io.TextIOWrapper(request.FILES['csv'].file, encoding="cp932")
        csv_content = csv.reader(data)
        
        csv_list=list(csv_content)
        if csv_list[0][4]=="SKU" and csv_list[0][5]=="品番" and csv_list[0][6]=="型番":
            
            #1行目を飛ばすため
            h=0
            for i in csv_list:
                if h!=0:
                    Master.objects.update_or_create(
                        jan = i[4],
                        defaults={
                            "jan": i[4],
                            "hinban": i[5],
                            "kataban": i[6],                    
                        }  
                    )
                h+=1   

            csv_message="マスタCSVの読み込みが完了しました！"
            return render(request,"csv_app/master.html",{"csv_message":csv_message,"form2":form2})

        else:
            csv_message="マスタCSVの形式が違います！"
            return render(request,"csv_app/master.html",{"csv_message":csv_message,"form2":form2})

    else:
        csv_message="CSVファイルが選択されていません！"
        return render(request,"csv_app/master.html",{"csv_message":csv_message,"form2":form2})



def master2(request):
    jan=request.POST["jan"]
    try:
        ins=Master.objects.get(jan=jan)
        initial_dict = {"jan":jan,"hinban":ins.hinban,"kataban":ins.kataban}
        form2 = Masterform(initial=initial_dict)
        message="既に存在しているJANコードです。内容を変更しますか？"
        return render(request,"csv_app/master.html",{"message":message,"form2":form2})
    except:
        initial_dict = {"jan":jan,}
        form2 = Masterform(initial=initial_dict)
        message="使用可能なJANコードです。新規登録を行ってください。"
        return render(request,"csv_app/master.html",{"message":message,"form2":form2})



def master3(request):
    jan=request.POST["jan"]
    hinban=request.POST["hinban"]
    kataban=request.POST["kataban"]

    if len(list(Master.objects.filter(jan=jan)))>0:
        Master.objects.filter(jan=jan).update(hinban=hinban,kataban=kataban)
        message="内容を更新しました！"
        form2=Masterform()
        return render(request,"csv_app/master.html",{"message":message,"form2":form2})
    else:
        Master(jan=jan,hinban=hinban,kataban=kataban).save()
        message="新規登録が完了しました！"
        form2=Masterform()
        return render(request,"csv_app/master.html",{"message":message,"form2":form2})



def trade_hinban(request):
    form2 = Masterform()
    
    if 'csv' in request.FILES:
        data = io.TextIOWrapper(request.FILES['csv'].file, encoding="cp932")
        csv_content = csv.reader(data)
        
        csv_list=list(csv_content)
        if csv_list[0][0]=="JANコード" and csv_list[0][1]=="品番":
            
            #1行目を飛ばすため
            h=0
            for i in csv_list:
                if h!=0:
                    Trade_hinban.objects.update_or_create(
                        jan = i[0],
                        defaults={
                            "jan": i[0],
                            "hinban": i[1],                   
                        }  
                    )
                h+=1

            csv_message2="マスタCSVの読み込みが完了しました！"
            return render(request,"csv_app/master.html",{"csv_message2":csv_message2,"form2":form2})

        else:
            csv_message2="マスタCSVの形式が違います！"
            return render(request,"csv_app/master.html",{"csv_message2":csv_message2,"form2":form2})

    else:
        csv_message2="CSVファイルが選択されていません！"
        return render(request,"csv_app/master.html",{"csv_message2":csv_message2,"form2":form2})



def trade_kyoten(request):
    form2 = Masterform()
    
    if 'csv' in request.FILES:
        data = io.TextIOWrapper(request.FILES['csv'].file, encoding="cp932")
        csv_content = csv.reader(data)
        
        csv_list=list(csv_content)
        if csv_list[0][0]=="名称" and csv_list[0][1]=="お届け先郵便番号":
            
            #1行目を飛ばすため
            h=0
            for i in csv_list:
                if h!=0:
                    Trade_kyoten.objects.update_or_create(
                        name = i[0],
                        defaults={
                            "name": i[0],
                            "yubin": i[1],
                            "pref": i[2],
                            "address1": i[3], 
                            "address2": i[4], 
                            "company": i[5], 
                            "sei": i[6], 
                            "mei": i[7], 
                            "tel": i[8], 
                            "ninushi_name": i[9],
                            "ninushi_tel": i[10],                 
                        }  
                    )
                h+=1

            csv_message3="マスタCSVの読み込みが完了しました！"
            return render(request,"csv_app/master.html",{"csv_message3":csv_message3,"form2":form2})

        else:
            csv_message3="マスタCSVの形式が違います！"
            return render(request,"csv_app/master.html",{"csv_message3":csv_message3,"form2":form2})

    else:
        csv_message3="CSVファイルが選択されていません！"
        return render(request,"csv_app/master.html",{"csv_message3":csv_message3,"form2":form2})



def trade_hinban_ajax(request):
    jan=request.POST.get("trade_jan")
    try:
        item=Trade_hinban.objects.get(jan=jan)
        d={
            "hinban":item.hinban,
            "comment":"既に存在しているJANコードです。内容を変更しますか？",
            }
    except:
        d={
            "hinban":"",
            "comment":"使用可能なJANコードです。新規登録を行ってください。",
            }
    return JsonResponse(d)



def trade_hinban2_ajax(request):
    jan=request.POST.get("trade_jan")
    hinban=request.POST.get("trade_hinban")
    if len(list(Trade_hinban.objects.filter(jan=jan)))>0:
        Trade_hinban.objects.filter(jan=jan).update(hinban=hinban)
        d={"comment":"内容を更新しました！"}
    else:
        Trade_hinban(jan=jan,hinban=hinban).save()
        d={"comment":"新規JANと品番を登録しました！"}
    print(d)
    return JsonResponse(d)