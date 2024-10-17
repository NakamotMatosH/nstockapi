import requests

#참고한 문서 :https://blog.bizspring.co.kr/%ED%85%8C%ED%81%AC/telegram-bot-api-system-monitoring/

def send_message_telegram(token, chat_id, text):
    """
    특정 채널(chat_id 기준)에 메시지를 보내는 함수입니다.
    Sends a message to a specific Telegram channel/chat using a bot token and chat ID.

    Parameters:
        token (str): 텔레그램 봇 토큰.
                     Telegram bot token.
        chat_id (str): 채널 또는 채팅의 ID.
                       Channel or chat ID.
        text (str): 전송할 메시지 내용.
                    The message text to send.

    Returns:
        response (requests.Response): 요청에 대한 응답 객체.
                                      Response object from the request.

    Usage:
        이 함수는 이 프로젝트에서 텔레그램 알림을 자동으로 전송하기 위해 사용됩니다. 
        예를 들어, 특정 이벤트가 발생했을 때 사용자에게 즉각적으로 알림을 보내는 용도로 활용됩니다.
        This function is used in this project to automatically send notifications via Telegram. 
        For instance, it is used to notify users instantly when specific events occur.
    """
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=payload)
    return response

# 예시 사용법
# Example usage
token = 'xxxxxx'  # 가상 텔레그램 토큰
chat_id = 'yyyyy'  # 가상 채널 ID
text = '안녕하세요'  # 전송할 메시지

response = send_message_telegram(token, chat_id, text)
print(response.json())
