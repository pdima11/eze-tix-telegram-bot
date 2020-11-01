from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN, APP_PORT, APP_HOST, TRANSPORTERS_CONFIG, JOB_INTERVAL
from transporter import Transporter9911, Transporter618
from utils import build_request
from models import User, RequestStatus, Request
from db import DB, UserSQL, RequestSQL
import logging

transporters = {
    '9911.by': Transporter9911(TRANSPORTERS_CONFIG['9911.by']),
    '618.by': Transporter618(TRANSPORTERS_CONFIG['618.by'])
}

logger = logging.getLogger(__name__)


def init_job_queue(job_queue):
    requests = DB.execute(RequestSQL.get_active_requests)
    logger.info(f'Add next requests to job queue during initialization: {[r["request_id"] for r in requests]}')

    for data in requests:
        request = Request.from_dict(data)
        job_queue.run_repeating(process_request, interval=JOB_INTERVAL, first=0, context=request, name=request.id)


def process_request(context):
    request = context.job.context

    transporter_site = TRANSPORTERS_CONFIG[request.transporter]['site']
    tickets = transporters[request.transporter].find_ticket(request)

    message = f'Following tickets are available for your request *{request.id}*. To order them go to {transporter_site}:'

    if tickets:
        context.bot.send_message(chat_id=request.user_id, text=message, parse_mode='Markdown')
        for ticket in tickets:
            context.bot.send_message(chat_id=request.user_id, text=f'{ticket}')


def request_trip(update, context):
    user = User.from_dict(update.message.from_user)
    DB.execute(UserSQL.save, user.asdict())
    logger.info(f'Starting process find ticket request from {user.username} user: {context.args}')

    request = build_request(user.id, context.args)
    request.id = DB.execute(RequestSQL.create, request.asdict())[0][0]

    message = f'Your request *{request.id}* is processing...'
    context.bot.send_message(user.id, text=message, parse_mode='Markdown')
    context.job_queue.run_repeating(process_request, interval=JOB_INTERVAL, first=0, context=request, name=request.id)

    DB.execute(RequestSQL.update_status_by_id, [RequestStatus.in_progress.value, request.id])
    logger.info(f'Request {request.id} from {user.username} user was successfully added to job queue')


def remove_request(update, context):
    request_id = context.args[0]
    logger.info(f'Starting process of removing {request_id} request id by {update.message.from_user["username"]} user')

    jobs = context.job_queue.get_jobs_by_name(int(request_id))
    message = f'Your request *{request_id}* was successfully closed'
    if jobs:
        for job in jobs:
            job.schedule_removal()
            DB.execute(RequestSQL.update_status_by_id, [RequestStatus.closed.value, request_id])
    else:
        message = f'Unfortunately request *{request_id}* doesn\'t exist'
    context.bot.send_message(update.effective_chat.id, text=message, parse_mode='Markdown')


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    init_job_queue(dispatcher.job_queue)

    request_handler = CommandHandler('request', request_trip)
    stop_handler = CommandHandler('stop', remove_request)
    logger.info(f'All handlers was successfully created')

    dispatcher.add_handler(request_handler)
    dispatcher.add_handler(stop_handler)
    logger.info(f'All handlers was successfully added to dispatcher')

    updater.start_webhook(listen="0.0.0.0", port=int(APP_PORT), url_path=TELEGRAM_TOKEN)
    updater.bot.setWebhook(f'{APP_HOST}{TELEGRAM_TOKEN}')
    logger.info(f'Webhook was started')

    updater.idle()


if __name__ == '__main__':
    main()
