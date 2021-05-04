# bot to fetch covid vaccine data from the india gov public API
# by @Lynnsane

# logging
import logging

# telegram
from aiogram import Bot, Dispatcher, executor, types

import requests
from datetime import date

#import of local files
import credentials

logging.basicConfig(level=logging.INFO)
# token is taken from local credentials file
bot = Bot(token=credentials.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# base API url
api_base = "https://cdn-api.co-vin.in/api"

# listen to incoming messages
@dp.message_handler()
async def plainMessageHandling(message: types.Message):
    commandText = message.get_command()
    commandArguments = message.get_args()

    # get current date as date object, using server time
    today = date.today()
    # gov.in requests the date formatted as day-monthmonth-yearyearyearyear
    # format today as such
    today_date = today.strftime("%d-%m-%Y")

    # when commandText is present the incoming message is a command (starts with /)
    if commandText: 
        # commands
        if '/start' == commandText:
            await bot.send_message(message['chat']['id'], 'Welcome\n/help for information.')

        if '/help' == commandText"
            await bot.send_message(message['chat']['id'], 'Use /pin (pincode) to view current vaccine data corresponding to the pin.')

        if '/pin' == commandText:
            if commandArguments:
                response = requests.get(f"{api_base}/v2/appointment/sessions/public/findByPin/?pincode={commandArguments}&date={today_date}")
                json_data = response.json()
                return_message = f"Vaccine Data on {today_date} using pin: <code>{commandArguments}</code>"
                for session in json_data['sessions']:
                    return_message += f"\n---"
                    return_message += f"\nMinimum Age: {session['min_age_limit']}"
                    return_message += f"\nName: {session['name']}"
                    return_message += f"\nAddress: {session['address']}"
                    return_message += f"\nDistrict: {session['district_name']}"
                    return_message += f"\nCharges: {session['fee_type']}, {session['fee']}"
                    return_message += f"\nAvailable Capacity: {session['available_capacity']}"
                    return_message += f"\nVaccine: {session['vaccine']}"

                return_message += f"\n\nRequery: <code>/pin {commandArguments}</code>"
                await bot.send_message(message['chat']['id'], return_message)

            else:
                await bot.send_message(message['chat']['id'], 'Invalid pin supplied')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)