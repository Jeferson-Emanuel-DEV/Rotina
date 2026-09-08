from plyer import notification

def enviar_notificacao(titulo, mensagem):
    try:
        notification.notify(
            title=titulo,
            message=mensagem,
            app_name='Minha Rotina',
            timeout=5
        )
    except Exception as e:
        print(f"Erro de notificação: {e}")