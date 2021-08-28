from django.shortcuts import render

# Create your views here.
# 参考文献
# https://note.nkmk.me/python-requests-usage/
# https://ebi-works.com/django-view/
from django.views.generic import TemplateView
import requests
import json

# 関数ベースで書く際に第１引数にrequestを渡すのは決まっています。
def index_view(request):
  # ここでURLを取得して
    url = 'https://api.mobilize.us/v1/events'
    # response変数にGETしたURLのAPIを格納
    return_json = json.loads(requests.get(url).text)
    response = return_json['data'] 
    # contexという辞書型を作る。list_dataという変数にresponse（API）入れていく
    # 参考文献
    # https://note.nkmk.me/python-requests-usage/
    # Webページの内容を取得したい場合はこのtext属性を使う。
    # for分でsummaryを回していますがその内容をリストに格納して、そのリストをlist_dataのバリューにすればいい
    summary_list = []
    for summary in response:
      summary_list.append(summary)
    context = {
      'list_data': summary_list, 
    }
    # summary_listはリスト型。
    # そこから辞書を取り出して、さらに任意のキーの値を抽出（ここではidキー）
    # 参考文献
    # https://note.nkmk.me/python-dict-list-values/
    summary_id = [each_summary_id.get('id') for each_summary_id in summary_list]
    print(summary_id)
    # return render(request, 'index.html', ここには辞書型しか置けない)ので上記で辞書型に変換
    # list_dataのValueであるsummary_listはリスト型、そしてそのリストに辞書が入っている
    return render(request, 'index.html', context)


# こちらのコードも使用できる
# 関数ベースで書く際に第１引数にrequestを渡すのは決まっています。
# def index_view(request):
#   # ここでURLを取得して
#     url = 'https://api.mobilize.us/v1/events'
#     # response変数にGETしたURLのAPIを格納
#     response = requests.get(url)
#     # contexという辞書型を作る。list_dataという変数にresponse（API）入れていく
#     # 参考文献
#     # https://note.nkmk.me/python-requests-usage/
#     # Webページの内容を取得したい場合はこのtext属性を使う。
#     context = {
#     'list_data': response.json(), 
#     }
#     # return render(request, 'index.html', ここには辞書型しか置けない)ので上記で辞書型に変換
#     return render(request, 'index.html', context)