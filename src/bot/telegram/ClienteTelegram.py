"""Cliente IFRN/SGA para Telegram"""
import logging
import sys

from bot import consts, texto
from bot.Cliente import Cliente

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, MessageHandler, Updater, ConversationHandler)

#from bot.database.bd_singleton import bd_singleton

#from bot.database.bd_MySQL import bd_singleton
from bot.database.bd_singleton import bd_singleton
from . import botoesTelegram

allowedUsernames = []
historico = []
NUMEROINTERACOESBOTFILENAME = "numeroInteracoesBot.txt"
NUMEROSUSUARIOSBOTFILENAME="numeroUsuariosBot.txt"
AVALIARSATISFACAOBOM = "SatisfacaoUsuarioBom.txt"
AVALIARSATISFACAORUIM = "SatisfacaoUsuarioRuim.txt"
AVALIARSATISFACAONORMAL = "SatisfacaoUsuarioNormal.txt"
NUMERODEUSUARIOS = 0

buttons = [
    [
        InlineKeyboardButton("🟢 confimar".upper(), callback_data="yes"),
        InlineKeyboardButton("🔴 Cancelar".upper(), callback_data="no")
    ]
]

class ClienteTelegram(Cliente):
    connection = bd_singleton()


    handler = None
    userName = ""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    def print_to_stdout(*a):

        # Here a is the array holding the objects
        # passed as the argument of the function
        print(*a, file=sys.stdout)

################################################################################################
    def salvar_metrica_avaliar_bom(self):
        try:
            satisfacao_do_usuario_bom_file = open(AVALIARSATISFACAOBOM, "r", encoding="utf-8")
        except FileNotFoundError:
            open(AVALIARSATISFACAOBOM, "x")
            satisfacao_do_usuario_bom_file = open(AVALIARSATISFACAOBOM, "r", encoding="utf-8")

        satisfacao_do_usuario_bom = satisfacao_do_usuario_bom_file.read()
        satisfacao_do_usuario_bom_file.close()
        if satisfacao_do_usuario_bom == "":
            satisfacao_do_usuario_bom = 0
        else:
            satisfacao_do_usuario_bom = int(satisfacao_do_usuario_bom)

        self.connection.gravar_avaliar_bom(satisfacao_do_usuario_bom + 1)

        arquivo = open(AVALIARSATISFACAOBOM, "w", encoding="utf-8")

        satisfacao_do_usuario_bom = str(satisfacao_do_usuario_bom + 1)
        arquivo.write(satisfacao_do_usuario_bom)
        arquivo.close()

    def salvar_metrica_avaliar_ruim(self):
        try:
            satisfacao_do_usuario_ruim_file = open(AVALIARSATISFACAORUIM, "r", encoding="utf-8")
        except FileNotFoundError:
            open(AVALIARSATISFACAORUIM, "x")
            satisfacao_do_usuario_ruim_file = open(AVALIARSATISFACAORUIM, "r", encoding="utf-8")

        satisfacao_do_usuario_ruim = satisfacao_do_usuario_ruim_file.read()
        satisfacao_do_usuario_ruim_file.close()
        if satisfacao_do_usuario_ruim == "":
            satisfacao_do_usuario_ruim = 0
        else:
            satisfacao_do_usuario_ruim = int(satisfacao_do_usuario_ruim)

        self.connection.gravar_avaliar_ruim(satisfacao_do_usuario_ruim + 1)

        arquivo = open(AVALIARSATISFACAORUIM, "w", encoding="utf-8")

        satisfacao_do_usuario_ruim = str(satisfacao_do_usuario_ruim + 1)
        arquivo.write(satisfacao_do_usuario_ruim)
        arquivo.close()

    def salvar_metrica_avaliar_normal(self):
        try:
            satisfacao_do_usuario_normal_file = open(AVALIARSATISFACAONORMAL, "r", encoding="utf-8")
        except FileNotFoundError:
            open(AVALIARSATISFACAONORMAL, "x")
            satisfacao_do_usuario_normal_file = open(AVALIARSATISFACAONORMAL, "r", encoding="utf-8")

        satisfacao_do_usuario_normal = satisfacao_do_usuario_normal_file.read()
        satisfacao_do_usuario_normal_file.close()
        if satisfacao_do_usuario_normal == "":
            satisfacao_do_usuario_normal = 0
        else:
            satisfacao_do_usuario_normal = int(satisfacao_do_usuario_normal)

        self.connection.gravar_avaliar_normal(satisfacao_do_usuario_normal + 1)

        arquivo = open(AVALIARSATISFACAONORMAL, "w", encoding="utf-8")

        satisfacao_do_usuario_normal = str(satisfacao_do_usuario_normal + 1)
        arquivo.write(satisfacao_do_usuario_normal)
        arquivo.close()

#####################################################################################

    def salvar_metrica_numero_de_interacoes(self):
        #TODO: Alterar docstring """Salva métricas com o numero de interacoes que já usou o bot. Essa funcao é chamada quando o usuario manda um /start"""
        try:
            numero_de_interacoes_file = open(NUMEROINTERACOESBOTFILENAME, "r", encoding="utf-8")
        except FileNotFoundError:
            open(NUMEROINTERACOESBOTFILENAME, "x")
            numero_de_interacoes_file = open(NUMEROINTERACOESBOTFILENAME, "r", encoding="utf-8")

        numero_de_interacoes = numero_de_interacoes_file.read()
        numero_de_interacoes_file.close()
        if numero_de_interacoes == "":
            numero_de_interacoes = 0
        else:
            numero_de_interacoes = int(numero_de_interacoes)

        self.connection.gravar_n_interacoes(numero_de_interacoes + 1)

        arquivo = open(NUMEROINTERACOESBOTFILENAME, "w", encoding="utf-8")

        interacoes_do_bot = str(numero_de_interacoes + 1)
        arquivo.write(interacoes_do_bot)
        arquivo.close()

    def save_metrica_usuario_atendido_banco(self):
        """Salva métricas com o numero de usuarios que já usou o bot. Essa funcao é chamada quando o usuario manda um /start"""
        try:
            numero_de_usuarios_file = open(NUMEROSUSUARIOSBOTFILENAME, "r", encoding="utf-8")
        except FileNotFoundError:
            open(NUMEROSUSUARIOSBOTFILENAME, "x")
            numero_de_usuarios_file = open(NUMEROSUSUARIOSBOTFILENAME, "r", encoding="utf-8")

        numero_de_usuarios = numero_de_usuarios_file.read()
        numero_de_usuarios_file.close()
        if numero_de_usuarios == "":
            numero_de_usuarios = 0
        else:
            numero_de_usuarios = int(numero_de_usuarios)

        self.connection.gravar_n_usuarios(numero_de_usuarios + 1)

        # context.bot.send_message(
        #     # -1001795732349
        #     chat_id=-1001565692647,
        #     text=f"{numero_de_usuarios + 1}",
        # )

        arquivo = open(NUMEROSUSUARIOSBOTFILENAME, "w", encoding="utf-8")

        usuarios_do_bot = str(numero_de_usuarios + 1)
        arquivo.write(usuarios_do_bot)
        arquivo.close()

    def save_metrica_usuario_atendido(self,update):
        print(update.effective_chat.username)
        print(allowedUsernames)
        print(update.effective_chat.username not in allowedUsernames)
        if update.effective_chat.username not in allowedUsernames:
             allowedUsernames.append(update.effective_chat.username)
             self.save_metrica_usuario_atendido_banco()

    def start(self, update: Update, context: CallbackContext) -> None:
        historico.clear()
        self.logger.info("start")
        # qunatidade de usuários diferentes iniciaram o bot:
        # if update.effective_chat.username not in alloweUsernames:
        #     alloweUsernames.append(update.effective_chat.username)
        #     self.salvar_metrica_numero_de_usuarios(context)
        self.save_metrica_usuario_atendido(update)
        self.userName = update.effective_user.full_name
        if update.effective_user is not None:
            if update.effective_message is not None:
                context.bot.send_photo(
                    chat_id=update.effective_message.chat_id,
                    photo=open(consts.IMAGEPATH, "rb"),
                    caption=f"Olá, {update.effective_user.full_name}! que ótimo ter você por aqui 😀",
                )
                context.bot.send_message(
                    chat_id=update.effective_message.chat_id,
                    text=texto.start_texto,
                    reply_markup=botoesTelegram.start_lines(),
                )

    def sendResposta(self, text, reply_markup):
        """
        Envia resposta para o usuário.
            Parameters:
                text(string): Texto a ser enviado
                reply_markup: Botões que pode ser enviado na mensagem
        """
        if text != "":
            if self.handler is not None:
                self.handler.edit_message_text(text=text, reply_markup=reply_markup)

    def responsehistorico(self, opcao):
        historico.append(opcao)
        return botoesTelegram.regressar_setor_line(historico)

    def getReplyMarkup(self, option):
        self.salvar_metrica_numero_de_interacoes()
        replyMarkup = {
            texto.BOM:botoesTelegram.resposta_avaliacao(),
            texto.RUIM:botoesTelegram.resposta_avaliacao(),
            texto.NORMAL:botoesTelegram.resposta_avaliacao(),
            texto.AVALIAR: botoesTelegram.buttons_avaliar(),
            texto.HOME: botoesTelegram.start_lines(),
            texto.ESTRUTURA_ADMINISTRATIVA: botoesTelegram.setor_line(),
            texto.SEAC_SGA: botoesTelegram.menu_seac(),
            texto.VOLTAR_FAQ_SEAC: botoesTelegram.faq_seac(),
            texto.CONTATO_SEAC: self.responsehistorico(texto.SEAC_SGA),
            texto.COEX_SGA: botoesTelegram.menu_coex(),
            texto.CONTATO_COEX: self.responsehistorico(texto.COEX_SGA),
            texto.FAQ_SEAC: botoesTelegram.faq_seac(),
            **dict.fromkeys(
                [
                    texto.FAQSEAC1,
                    texto.FAQSEAC2,
                    texto.FAQSEAC3,
                    texto.FAQSEAC4,
                    texto.FAQSEAC5,
                    texto.FAQSEAC6,
                    texto.FAQSEAC7,
                    texto.FAQSEAC8,
                    texto.FAQSEAC9,
                    texto.FAQSEAC_10
                ],
                self.responsehistorico(texto.VOLTAR_FAQ_SEAC),
            ),
            texto.FAQ_COEX: self.responsehistorico(texto.COEX_SGA),
        }
        return replyMarkup.get(option)

    def getResponseText(self, option, update):
        text = {
            texto.BOM: texto.txt_avaliar_agradecimento, texto.RUIM: texto.txt_avaliar_agradecimento, texto.NORMAL: texto.txt_avaliar_agradecimento,
            texto.AVALIAR: texto.txt_avaliar,
            texto.SUGERIR: texto.txt_sugestao,
            texto.HOME: f"Olá! " + self.userName + "\n" + texto.start_texto,
            texto.ESTRUTURA_ADMINISTRATIVA: "Escolha uma opção disponível para continuar 👇",
            texto.SEAC_SGA: texto.txt_seac,
            texto.VOLTAR_FAQ_SEAC: texto.txt_seac + texto.FAQ,
            texto.CONTATO_SEAC: texto.txt_seac + texto.seac_contato,
            texto.COEX_SGA: texto.txt_coex,
            texto.CONTATO_COEX: texto.txt_coex + texto.coex_contato,
            texto.FAQ_SEAC: texto.txt_seac + texto.FAQ,
            texto.FAQSEAC1: texto.txt_faq_seac1,
            texto.FAQSEAC2: texto.txt_faq_seac2,
            texto.FAQSEAC3: texto.txt_faq_seac3,
            texto.FAQSEAC4: texto.txt_faq_seac4,
            texto.FAQSEAC5: texto.txt_faq_seac5,
            texto.FAQSEAC6: texto.txt_faq_seac6,
            texto.FAQSEAC7: texto.txt_faq_seac7,
            texto.FAQSEAC8: texto.txt_faq_seac8,
            texto.FAQSEAC9: texto.txt_faq_seac9,
            texto.FAQSEAC_10: texto.txt_faq_seac_10,
            texto.FAQ_COEX: texto.txt_coex + texto.FAQ,
        }

        return text.get(option)

    def getResponseTextReplyMarkup(self, option, update):
        return [self.getResponseText(option, update), self.getReplyMarkup(option)]

    def menu_avaliar (self, update: Update, context: CallbackContext) -> None:
        context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=texto.txt_avaliar,
        reply_markup=botoesTelegram.buttons_avaliar()
        )

    def balloon(self, update: Update, context: CallbackContext) -> None:

        query = update.callback_query
        self.handler = query
        self.handler.answer()

        if (query.data == texto.SUGERIR):
            return self.sugerir(update, context)

        if(query.data==texto.HOME):
            self.salvar_metrica_numero_de_interacoes()
        argumentos = self.getResponseTextReplyMarkup(query.data, update)
        self.sendResposta(argumentos[0], argumentos[1])

        if (query.data == texto.BOM):
            self.salvar_metrica_avaliar_bom()

        if (query.data == texto.RUIM):
            self.salvar_metrica_avaliar_ruim()

        if (query.data == texto.NORMAL):
            self.salvar_metrica_avaliar_normal()

    def sugerir(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=texto.txt_sugestao)
        return self.comentar

    def comentar(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=texto.txt_confirmar_sugestao)
        update.effective_message.reply_text(text=update.effective_message.text,
                                            reply_markup=InlineKeyboardMarkup(buttons))
        return self.confimar

    def confimar(self, update: Update, context: CallbackContext):
        query = update.callback_query
        handler = query
        handler.answer()

        if "yes" == query.data:
            usuario = f"{update.effective_user.full_name}"
            msg = f'{update.effective_message.text}'
            if self.connection.gravar_sugestao(usuario, msg) is None:
                handler.edit_message_text("A sugestão não pode ser compreendida!")
                return ConversationHandler.END
            # connectPostgreSQL.gravar_sugestao(usuario, msg)
            argumentos = self.getResponseTextReplyMarkup(texto.HOME, texto.HOME)
            handler.edit_message_text(
                text=texto.txt_sugestao_agradecimento + "\n\n" + argumentos[0], reply_markup=argumentos[1])
            # self.sendResposta(argumentos[0], argumentos[1])

        if "no" == query.data:
            argumentos = self.getResponseTextReplyMarkup(texto.HOME, texto.HOME)
            handler.edit_message_text(
                text=texto.txt_sugestao_cancelada + "\n\n" + argumentos[0], reply_markup=argumentos[1])


        return ConversationHandler.END

    def send_home(self, update, context):
        self.sendResposta(texto.HOME, texto.HOME)
        return ConversationHandler.END

    def cancel(update: Update, context: CallbackContext):
        pass

    def timeout(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_message.chat_id, text='out time has ended. good bye')

    def exc(self, update: Update, context: CallbackContext) -> None:
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text=f'{update.effective_user.full_name} sugiro que utilize / para acessar o menu e funções.')

    def iniciar(self) -> None:
        token = "5241177916:AAHZUC5gimNEyosHBngN5-KELqBSYauthok"

        updater = Updater(token)
        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("sugerir", self.sugerir),
                CallbackQueryHandler(self.balloon)],
            states={
                self.comentar: [MessageHandler(Filters.text, self.comentar)],
                self.confimar: [CallbackQueryHandler(self.confimar)],
                ConversationHandler.TIMEOUT: [CallbackQueryHandler(self.confimar, self.timeout),
                                              MessageHandler(Filters.text, self.timeout)],
                self.send_home: [MessageHandler(Filters.text, self.send_home)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
            conversation_timeout=10
        )
        dispatcher.add_handler(conv_handler)
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("avaliar", self.menu_avaliar))
        dispatcher.add_handler(MessageHandler(Filters.all, self.exc))
        #        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.salvar_sugestao))
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    print("inicio")
    clienteTelegram = ClienteTelegram()
    clienteTelegram.print_to_stdout("OIIII")
    clienteTelegram.iniciar()
    
    
