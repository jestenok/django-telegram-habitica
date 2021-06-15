unlock_secret_room = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           "*Users*: {user_count}\n" \
           "*24h active*: {active_24}"

share_location = "Would you mind sharing your location?"
thanks_for_location = "Thanks for 🌏🌎🌍"

github_button_text = "GitHub"
secret_level_button_text = "Secret level🗝"

start_created = "Sup, {first_name}!"
start_not_created = "Welcome back, {first_name}!"

broadcast_command = '/broadcast'

broadcast_no_access = "Sorry, you don't have access to this function."
broadcast_header = "This message will be sent to all users.\n\n"
confirm_broadcast = "Confirm✅"
decline_broadcast = "Decline❌"
message_is_sent = "Message is sent✅\n\n"
declined_message_broadcasting = "Message broadcasting is declined❌\n\n"

error_with_markdown = "Can't parse your text in Markdown style."
specify_word_with_error = " You have mistake with the word "

secret_admin_commands = "⚠️ Secret Admin commands\n" \
                        "/stats - bot stats"

def task_text(task):
    task_text = task.text.split(' # ', maxsplit=1)
    text = f'Задача № {task.task_number}\n'\
           f'{task_text[0]}\n<pre language="python>">{task_text[1]}\n</pre>'\

    if task.completed:
        text += f'завершена!\n'
    else:
        text += f'принята в работу.\n' \
                f'При ее завершении будет отправлено уведомление!\n'

    if task.notes != '':
        text += f'Комментарий: <pre language="python>">{task.notes}</pre>'

    return text


def message_answer(question):
    question = question.lower()
    answers = {'привет': 'Привет, солнышко',
               'спокойной ночи': 'Сладких снов :*', }
    if question in answers:
        return answers[question]
    else:
        return ''
