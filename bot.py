import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time  # Importando a biblioteca para adicionar o delay
from googlesearch import search  # Biblioteca para buscas no Google

# Substitua pelo seu token do BotFather
CHAVE_API = "8172210834:AAHPOKEEB9RXHzElR7wjfbFdzDdxA_kJBws"
bot = telebot.TeleBot(CHAVE_API)

# Função para verificar se a mensagem é válida (sempre retorna True aqui)
def verificar(mensagem):
    return True

# Função para enviar as opções de ajuda
def enviar_opcoes(mensagem):
    # Mensagem de boas-vindas
    welcome_message = (
        "Olá! Eu sou um bot para ajudar com informações sobre abuso sexual.\n\n"
        "Escolha uma das opções abaixo para obter ajuda:"
    )

    # Criando os botões de opções
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton("O que é abuso sexual?", callback_data="o_que_e_abuso")
    button_2 = InlineKeyboardButton("Como denunciar?", callback_data="como_denunciar")
    button_3 = InlineKeyboardButton("Sinais de abuso", callback_data="sinais_abuso")
    button_4 = InlineKeyboardButton("Onde buscar ajuda?", callback_data="onde_buscar_ajuda")
    button_5 = InlineKeyboardButton("Assistir vídeo sobre abuso sexual", callback_data="assistir_video")
    button_6 = InlineKeyboardButton("Prevenção ao abuso sexual", callback_data="prevencao_abuso")
    button_7 = InlineKeyboardButton("Consequências do abuso sexual", callback_data="consequencias_abuso")
    button_8 = InlineKeyboardButton("Como proteger crianças e adolescentes", callback_data="protecao_criancas")
    button_9 = InlineKeyboardButton("Outras dúvidas", callback_data="outras_duvidas")
    
    # Adiciona os botões ao teclado
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9)

    # Envia a mensagem com as opções de ajuda
    bot.send_message(mensagem.chat.id, welcome_message, reply_markup=keyboard)

# Handler para o botão "Outras dúvidas"
@bot.callback_query_handler(func=lambda call: call.data == "outras_duvidas")
def outras_duvidas_handler(call):
    # Solicita que o usuário digite a dúvida
    bot.send_message(call.message.chat.id, "Por favor, digite sua dúvida abaixo. Vou pesquisar e trazer informações relevantes!")
    # Registra o próximo passo como a função `processar_duvida`
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, processar_duvida)

# Função para processar a dúvida do usuário
def processar_duvida(message):
    query = message.text  # Captura a dúvida do usuário
    bot.send_message(message.chat.id, "Estou pesquisando sua dúvida...")

    try:
        # Busca no Google e retorna os primeiros 3 links
        resultados = list(search(query, num_results=3))
        if resultados:
            resposta = "Aqui estão algumas informações que encontrei:\n\n"
            for i, link in enumerate(resultados, start=1):
                resposta += f"{i}. {link}\n"
            bot.send_message(message.chat.id, resposta)
        else:
            bot.send_message(message.chat.id, "Desculpe, não consegui encontrar informações sobre sua dúvida.")
    except Exception as e:
        bot.send_message(message.chat.id, "Desculpe, algo deu errado ao buscar sua dúvida. Por favor, tente novamente!")
    
    # Após responder, oferecer opções de continuar ou encerrar
    enviar_opcoes_continuar_ou_encerrar(message)

# Função para enviar as opções de continuar ou encerrar a conversa
def enviar_opcoes_continuar_ou_encerrar(mensagem):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton("Desejo continuar", callback_data="continuar")
    button_2 = InlineKeyboardButton("Encerrar conversa", callback_data="encerrar")
    keyboard.add(button_1, button_2)
    bot.send_message(mensagem.chat.id, "Você deseja continuar ou encerrar a conversa?", reply_markup=keyboard)

# Handler para as opções de continuar ou encerrar
@bot.callback_query_handler(func=lambda call: call.data in ["continuar", "encerrar"])
def continuar_ou_encerrar(call):
    if call.data == "continuar":
        enviar_opcoes(call.message)
    elif call.data == "encerrar":
        bot.send_message(call.message.chat.id, "Obrigado por conversar comigo. Estou aqui sempre que precisar!")

# Responder ao usuário com uma mensagem inicial e opções de ajuda
@bot.message_handler(func=verificar)
def responder(mensagem):
    enviar_opcoes(mensagem)

# Função para lidar com as respostas aos botões
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    response = ""  # Garantir que 'response' tenha um valor inicial

    # Respostas para cada opção selecionada
    if call.data == "o_que_e_abuso":
        response = "Abuso sexual é qualquer ato sexual realizado sem o consentimento da pessoa envolvida. Isso inclui toques indesejados, coerção, exploração sexual e estupro."
    elif call.data == "como_denunciar":
        response = "Para denunciar abuso sexual no Brasil, você pode:\n- Ligar para o Disque 100 (Direitos Humanos).\n- Ligar para a Polícia Militar (190).\n- Procurar uma Delegacia da Mulher ou delegacia comum."
    elif call.data == "sinais_abuso":
        response = "Os sinais de abuso sexual podem incluir:\n- Mudanças bruscas de comportamento (isolamento, medo).\n- Dores ou ferimentos inexplicáveis.\n- Relutância em estar perto de certas pessoas.\n- Entre outros comportamentos incomuns."
    elif call.data == "onde_buscar_ajuda":
        response = "Você pode buscar ajuda em:\n- Delegacias especializadas (como Delegacias da Mulher).\n- Centros de atendimento psicossocial (CAPS).\n- ONGs e instituições de apoio às vítimas.\n- Redes de apoio locais, como amigos ou familiares confiáveis."
    elif call.data == "assistir_video":
        # Link do vídeo no YouTube
        video_url = "https://youtu.be/G66gPz02Nl4?si=smKA-J5Q2aSmpM5e"
        response = "Aqui está o vídeo com informações úteis sobre abuso sexual: " + video_url  # Envia o link como texto
        bot.send_message(call.message.chat.id, response)  # Envia o link do vídeo como mensagem de texto

        # Adiciona uma pausa de 2 segundos antes de enviar as opções
        time.sleep(2)
        enviar_opcoes_continuar_ou_encerrar(call.message)
        return  # Evita enviar outra mensagem após esta
    elif call.data == "prevencao_abuso":
        response = "A prevenção ao abuso sexual envolve a educação sobre o corpo, respeito ao outro e limites. Encorajamento de um ambiente seguro e a promoção de relacionamentos respeitosos são fundamentais."
    elif call.data == "consequencias_abuso":
        response = "As consequências do abuso sexual podem incluir traumas psicológicos duradouros, danos físicos, sentimentos de vergonha e culpa, além de problemas de confiança e relações interpessoais."
    elif call.data == "protecao_criancas":
        response = "Proteger crianças e adolescentes envolve educá-los sobre limites pessoais, ensinar como identificar comportamentos inadequados e garantir um ambiente seguro e saudável."

    # Envia a resposta em uma nova mensagem (se houver uma resposta válida)
    if response:
        bot.send_message(call.message.chat.id, response)

    # Adiciona uma pausa de 2 segundos
    time.sleep(2)

    # Após enviar a resposta, envia as opções de continuar ou encerrar
    if call.data not in ["continuar", "encerrar"]:
        enviar_opcoes_continuar_ou_encerrar(call.message)

    # Se a opção for encerrar, se despede
    if call.data == "encerrar":
        time.sleep(1)  # Pausa antes de encerrar
        bot.send_message(call.message.chat.id, "Obrigado por conversar conosco. Se precisar de ajuda novamente, estarei aqui!")

    # Se a opção for continuar, envia novamente as opções do menu
    if call.data == "continuar":
        enviar_opcoes(call.message)

# Inicia o bot
bot.polling() 