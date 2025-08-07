from aiogram.types import BotCommand, BotCommandScopeDefault
from handlers.start import router
from create_bot import bot, dp, admins
import asyncio
import logging


#иницилизация логгера
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log")
    ]
)
logger = logging.getLogger(__name__)

#иницилизация команд
async def set_commands():
    try:
        commands = [
            BotCommand(command='start', description='Старт'),
        ]
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        logger.info("Команды успешно установлены")
    except Exception as e:
        logger.error(f"Ошибка при установке команд: {e}", exc_info=True)
        raise


#функция запуска бота
async def on_startup() -> None:
    logger.info("Запуск бота...")
    try:
        await set_commands()
        successful_chats = []
        for chat_id in admins:
            try:
                chat = await bot.get_chat(chat_id)
                await bot.send_message(chat_id=chat_id, text="Бот запущен")
                logger.info(f"Сообщение отправлено в чат {chat_id}")
                successful_chats.append(chat_id)
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения в чат {chat_id}: {e}", exc_info=True)
                continue
        if not successful_chats:
            logger.warning("Ни одному чату (админу/группе) не удалось отправить сообщение")
        else:
            logger.info(f"Сообщения отправлены в чаты: {successful_chats}")
        logger.info("on_startup завершён успешно")
    except Exception as e:
        logger.error(f"Критическая ошибка в on_startup: {e}", exc_info=True)
        raise

#функция выключения бота
async def on_shutdown() -> None:
    logger.info("Остановка бота...")
    try:
        successful_chats = []
        for chat_id in admins:
            try:
                chat = await bot.get_chat(chat_id)
                await bot.send_message(chat_id=chat_id, text="Бот остановлен")
                logger.info(f"Сообщение отправлено в чат {chat_id}")
                successful_chats.append(chat_id)
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения в чат {chat_id}: {e}", exc_info=True)
                continue
        if not successful_chats:
            logger.warning("Ни одному чату (админу/группе) не удалось отправить сообщение об остановке")
        await bot.session.close()
        logger.info("Сессия бота закрыта")
    except Exception as e:
        logger.error(f"Ошибка в on_shutdown: {e}", exc_info=True)


#взаимодействие с telegram
async def main() -> None:
    logger.info("Инициализация приложения...")
    try:


        dp.include_router(router)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, pool_interval = 10)

    except Exception as e:
        logger.error(f"Ошибка в main: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())