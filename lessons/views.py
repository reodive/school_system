import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_ask(request):
    """
    生徒の質問を受け取り、AIからの回答を返す API ビュー
    """
    if request.method == "POST":
        question = request.POST.get('question')
        if not question:
            return JsonResponse({'error': '質問が入力されていません。'}, status=400)

        api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": question,
            "max_tokens": 150,
        }
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            answer = response.json().get("choices")[0].get("text").strip()
            return JsonResponse({'answer': answer})
        else:
            return JsonResponse({'error': 'AIサービスに接続できませんでした。'}, status=500)
    return JsonResponse({'error': 'POST リクエストが必要です。'}, status=405)

def ai_chat_view(request):
    """
    AIレッスンチャット画面の表示
    """
    return render(request, 'lessons/ai_chat.html')
