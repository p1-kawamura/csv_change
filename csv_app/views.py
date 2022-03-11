from django.shortcuts import render,redirect
import io
import csv
from django.http import HttpResponse
from .models import Master
import urllib.parse
from django.contrib import messages


def index(request):
    messages.warning(request,"変換するCSVを選択してください。")
    return render(request,"csv_app/index.html")

def master(request):
    if 'csv' in request.FILES:
        data = io.TextIOWrapper(request.FILES['csv'].file)
        csv_content = csv.reader(data)

        header =next(csv_content) #タイトルを読み飛ばす

        for i in csv_content:
            Master.objects.update_or_create(
                jan = i[7],
                defaults={
                    "brand": i[0],
                    "hinban": i[1],
                    "hinmei": i[2],
                    "color_no": i[3],
                    "color_name": i[4],
                    "size_no": i[5],
                    "size_name": i[6],
                    "jan": i[7],
                }  
            )
        return redirect('index')
    else:
        return redirect('index')


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

        if select_maker == "キャブ":
            maker="CAB"
            ex_csv=[]

            for line in csv_list:
                a=[]
                item=Master.objects.get(jan=line[8]+" ")

                a.append(item.hinban)
                a.append(item.color_no)
                a.append(item.size_no)
                a.append(line[6])
                ex_csv.append(a)


        elif select_maker == "トムス":
            maker="TOMS"
            ex_csv=[["品番","カラーコード","サイズコード","数量","OPP袋同送数","備考","お客様注文Ｎｏ"]]

            for line in csv_list:
                a=[]
                item=Master.objects.get(jan=line[8])

                a.append(item.hinban)
                a.append(item.color_no)
                a.append(item.size_no)
                a.append(line[6])
                a.append("")
                a.append(line[11])
                a.append(line[7])
                ex_csv.append(a)


        elif select_maker == "フェリック":
            maker="フェリック"
            ex_csv=[]

            for line in csv_list:
                a=[line[0],line[3],line[5],line[6]]
                ex_csv.append(a)


        elif select_maker == "ボンマックス":
            maker="ボンマックス"
            ex_csv=[["品番","カラー","サイズ","個数","明細摘要"]]

            for line in csv_list:
                a=[line[0],line[3],line[5],line[6],""]
                ex_csv.append(a)

        else:
            messages.error(request,"対応していないメーカーのCSVが選択されています！")
            return render(request,"csv_app/index.html",{"filename":filename})




        reset="OK"
        messages.success(request,"変換後のCSVをダウンロードしました！")

        #------セッション-----
        request.session["csv_list"]={"file":str(file),"csv":ex_csv}

        return render(request,"csv_app/index.html",
            {"dict":dict,"mitsumori":mitsumori,"maker":maker,"reset":reset,"filename":filename})

    
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