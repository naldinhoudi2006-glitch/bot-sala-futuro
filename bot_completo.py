import os
import time
import requests
import telebot
from playwright.sync_api import sync_playwright

# Configurações do Telegram e da SED
TOKEN_TELEGRAM = "8753031201:AAEC6SLdYqp6G6yWUwAPOjC6uP_uqYGChqU"
USER_LOGIN = "000111343318"
USER_SENHA = "Righetto100%"

bot = telebot.TeleBot(TOKEN_TELEGRAM)

def obter_resposta_gemini(pergunta):
    return f"Resolução automática para: {pergunta}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! O bot da Sala do Futuro está online no Render e pronto para automatizar as tarefas.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    texto_pergunta = message.text
    bot.reply_to(message, "A processar a tarefa via Playwright...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://sed.educacao.sp.gov.br/")
            time.sleep(3)
            
            resposta = obter_resposta_gemini(texto_pergunta)
            bot.reply_to(message, f"Resposta obtida com sucesso:\n{resposta}")
        except Exception as e:
            bot.reply_to(message, f"Erro ao processar na plataforma: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    print("Bot iniciado em segundo plano no Render...")
    bot.infinity_polling()
