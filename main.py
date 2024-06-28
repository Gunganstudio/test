import os
import paramiko
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

# Telegram bot API token
TOKEN = os.getenv('7390012761:AAFBEWqm09gCtMX2QxP0EJtXxypgcC4AUps')  # Fetch token from environment variable

# tmate.io SSH details (replace with your tmate.io session details)
TMATE_SSH_HOST = 'lon1.tmate.io'
TMATE_SSH_PORT = 22  # Use the port provided by tmate.io, often 22
TMATE_SSH_USERNAME = 'uGc29DH3EZeKeht3UeQgnTyEH'  # Example username from your command

# Function to handle the /ssh command
def run_ssh_command(update: Update, context: CallbackContext) -> None:
    # Get the chat ID to reply back
    chat_id = update.message.chat_id

    # Extract the command from the message
    command = update.message.text.replace('/ssh ', '')

    # Establish SSH connection to tmate.io
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to tmate.io SSH server
        ssh_client.connect(hostname=TMATE_SSH_HOST, port=TMATE_SSH_PORT, username=TMATE_SSH_USERNAME)

        # Execute the command
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Read and format command output
        output = stdout.read().decode('utf-8')

        # Send output back to Telegram
        context.bot.send_message(chat_id=chat_id, text=f'Command executed:\n{command}\n\nOutput:\n{output}')

        # Close SSH connection
        ssh_client.close()

    except paramiko.AuthenticationException:
        context.bot.send_message(chat_id=chat_id, text='Authentication failed. Please check your SSH credentials.')
    except paramiko.SSHException as e:
        context.bot.send_message(chat_id=chat_id, text=f'SSH error occurred: {str(e)}')
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f'Error occurred: {str(e)}')

# Set up the Telegram bot handlers and start polling
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handler for /ssh
    dispatcher.add_handler(CommandHandler('ssh', run_ssh_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
