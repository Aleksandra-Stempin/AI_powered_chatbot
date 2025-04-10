from chatbot_gui import run_chat

try:
    run_chat()
except Exception as e:
    print(f'En error occurred: {str(e)}')