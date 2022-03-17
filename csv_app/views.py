from django.shortcuts import render,redirect
import io
import csv
from django.http import HttpResponse
from .models import Master
import urllib.parse
from django.contrib import messages
from .forms import Masterform


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

        select_maker=request.POST["メーカー"]


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

        #--- エラー表示用 ---
        flag=True
        err=[]

        if select_maker == "キャブ":
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
                reset="OK"
                messages.success(request,"変換後のCSVをダウンロードしました！")
                

        elif select_maker == "トムス":
            maker="TOMS"
            ex_csv=[["品番","カラーコード","サイズコード","数量","OPP袋同送数","備考","お客様注文Ｎｏ"]]

            for line in csv_list:

                if "-" in line[0]:
                    hinban=line[0].split("-")[0]
                else:
                    hinban=line[0]
                
                a=[hinban,line[3],line[5],line[6],"",line[11][:20],line[7]]
                ex_csv.append(a)

            reset="OK"
            messages.success(request,"変換後のCSVをダウンロードしました！")

        elif select_maker == "フェリック":
            maker="フェリック"
            ex_csv=[]

            for line in csv_list:
                a=[line[0],line[3],line[5],line[6]]
                ex_csv.append(a)

            reset="OK"
            messages.success(request,"変換後のCSVをダウンロードしました！")


        elif select_maker == "ボンマックス":
            maker="ボンマックス"
            ex_csv=[["品番","カラー","サイズ","個数","明細摘要"]]

            for line in csv_list:
                a=[line[0],line[3],line[5],line[6],line[11][:20]]
                ex_csv.append(a)

            reset="OK"
            messages.success(request,"変換後のCSVをダウンロードしました！")

        else:
            messages.error(request,"対応していないメーカーのCSVが選択されています！")
            return render(request,"csv_app/index.html",{"filename":filename})

        #-----------------
        #最終結果
        #-----------------
        if flag == True:
            reset="OK"
            messages.success(request,"変換後のCSVをダウンロードしました！")

            #------セッション-----
            request.session["csv_list"]={"file":str(file),"csv":ex_csv}

        else:
            print(err)
            reset="NO"
            messages.error(request,"マスタに登録されていない商品が含まれています！")


        

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
    if 'csv' in request.FILES:
        data = io.TextIOWrapper(request.FILES['csv'].file)
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
            messages.success(request,"マスタCSVの読み込みが完了しました！")
            return redirect('master_kanri')
        else:
            messages.error(request,"マスタCSVの形式が違います！")
            return redirect('master_kanri')
    else:
        messages.error(request,"CSVファイルが選択されていません！")
        return redirect('master_kanri')


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
