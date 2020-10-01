from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN, TRANSPORTERS_CONFIG, JOB_INTERVAL
from transporter.transporter9911 import Transporter9911
from utils import build_request
import uuid

transporters = {
    '9911.by': Transporter9911(TRANSPORTERS_CONFIG['9911.by'])
}


def process_request(context):
    data = context.job.context

    request = data['request']
    transporter_site = TRANSPORTERS_CONFIG[request.transporter]['site']
    tickets = transporters[request.transporter].find_ticket(request)

    message = f'Following tickets are available for your request *{request.id}*. To order them go to {transporter_site}:'

    if tickets:
        context.bot.send_message(chat_id=data['chat_id'], text=message, parse_mode='Markdown')
        for ticket in tickets:
            context.bot.send_message(chat_id=data['chat_id'], text=f'{ticket}')


def request_trip(update, context):
    request_id = str(uuid.uuid4())[:8]
    request = build_request(request_id, context.args)

    data = {
        'request': request,
        'chat_id': update.message.chat_id
    }

    message = f'Your request *{request_id}* is processing...'
    context.bot.send_message(update.effective_chat.id, text=message, parse_mode='Markdown')
    context.job_queue.run_repeating(process_request, interval=JOB_INTERVAL, first=0, context=data, name=request_id)


def remove_request(update, context):
    request_id = context.args[0]

    jobs = context.job_queue.get_jobs_by_name(request_id)
    message = f'Your request *{request_id}* was successfully removed'
    if jobs:
        for job in context.job_queue.get_jobs_by_name(request_id):
            job.schedule_removal()
    else:
        message = f'Unfortunately request *{request_id}* doesn\'t exist'
    context.bot.send_message(update.effective_chat.id, text=message, parse_mode='Markdown')


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    request_handler = CommandHandler('request', request_trip)
    stop_handler = CommandHandler('stop', remove_request)

    dispatcher.add_handler(request_handler)
    dispatcher.add_handler(stop_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
