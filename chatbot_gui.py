import tkinter
import pyperclip
import google.generativeai as genai
from bot_person_list import person_list, person_list_for_gui, no_specified_bot_role
from tkinter import *
import tkinter.font as tkFont

from my_api_key_file import my_google_api_key


chat_history_to_print = []
# copy here your google_api_key and comment line 8
my_api_key = my_google_api_key
genai.configure(api_key=my_api_key)
geminiModel=genai.GenerativeModel("gemini-1.5-flash")
chat = geminiModel.start_chat(history=[])
chat_history_str_question = ""
bot_person_list =person_list_for_gui
default_text_for_chat_title_lbl = f"You are chatting with general chatbot."
default_chatbot_name = "bot"
speaking_person_to_say_goodbye = default_chatbot_name

# font sizes and families
font_list = ["Comic Sans MS", "Chalkduster", "Papyrus", "Curlz MT", "Harrington", "Kristen ITC", "Jokerman",
             "Giddyup Std", "Bradley Hand ITC", "Helvetica" ]

font_index = 4
font_family = font_list[font_index]
title_font_size =15
chat_font_size = 10
choose_person_font_size = 11
button_font_size = 11

# colors
main_window_color = '#90ee90'
chat_field_color = "#CBFBCB"
font_color = "#074607"
button_color = "#60C660"
button_color_on_focus = "#ffff4d"



def get_initial_message_for_ai():
    # global chat_history_to_display
    global speaking_person
    if speaking_person.get()==default_chatbot_name:
        speaking_person_str = ""
    else:
        speaking_person_str = f"speak like {speaking_person.get()}, "


    initial_message_for_ai = f"{speaking_person_str} {chat_history.get()}"
    return initial_message_for_ai

def person_chosen(chosen_person):
    global speaking_person
    global speaking_person_to_say_goodbye
    chat_history.set("")

    if (chosen_person == no_specified_bot_role or chosen_person==default_chatbot_name):
        speaking_person_lbl_text = default_text_for_chat_title_lbl
        speaking_person.set(default_chatbot_name)
    else:
        speaking_person_lbl_text =  f"You are chatting with {chosen_person}"
        speaking_person.set(chosen_person)
    chat_title_lbl.config(text=speaking_person_lbl_text)
    speaking_person_to_say_goodbye = chosen_person
    # activating widgets
    send_question_button.config(state=tkinter.NORMAL)
    question_entry.config(state=NORMAL)
    end_chat_button.config(state=tkinter.NORMAL)
    question_entry.focus_set()
    return None

def block_buttons_after_question():
    asked_question.set("")
    question_entry.config(state=tkinter.NORMAL)
    question_entry.delete('1.0', tkinter.END)
    question_entry.config(state=tkinter.DISABLED)
    send_question_button.config(state=tkinter.DISABLED)
    end_chat_button.config(state=tkinter.DISABLED)
    new_chat_button.config(state=tkinter.DISABLED)

def unblock_buttons_after_answer():
    asked_question.set("")
    question_entry.config(state=tkinter.NORMAL)
    question_entry.delete('1.0', tkinter.END)
    send_question_button.config(state=tkinter.NORMAL)
    end_chat_button.config(state=tkinter.NORMAL)
    new_chat_button.config(state=tkinter.DISABLED)


def ask_your_question():
    # asking boot a question
    global chat_history_str_question
    asked_question.set(question_entry.get('1.0','end'))
    user_question = asked_question.get()
    user_question = str(user_question)
    user_question = user_question.strip()
    if (len(asked_question.get())>1):
        asked_question_str = "YOU: " + user_question
        chat_history_str_start = chat_history.get()
        chat_history_str_question = f'''{chat_history_str_start}
{asked_question_str}'''
        chat_history_str_question = str(chat_history_str_question)
        chat_history_str_question = chat_history_str_question.strip()
        chat_history.set(chat_history_str_question)
        asked_question.set("")
        question_entry.focus_set()
        return True
    else:
        asked_question.set("")
        return False



def count_speaking_person_in_bots_ans(bot_ans, speaking_person):
    speaking_person = str(speaking_person).strip()
    speaking_person_upper = speaking_person.upper()
    count = bot_ans.count(speaking_person)
    return count
def get_answer_from_AI(initial_feed_for_AI):
    global speaking_person

    speaking_person_str = speaking_person.get()
    speaking_persons_list = [default_chatbot_name,  no_specified_bot_role]
    if (speaking_person_str in speaking_persons_list):
        speaking_person_str = default_chatbot_name
    len_speaking_person = len(speaking_person_str)
    chat_history_str = chat_history.get()


    output_text = ""
    genai.configure(api_key=my_google_api_key)

    model = genai.GenerativeModel('gemini-1.5-flash-002')
    generation_config = genai.GenerationConfig(
        stop_sequences=None,
        temperature=0.7,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens= 500
    )

    responses = model.generate_content(
        contents=initial_feed_for_AI,
        generation_config=generation_config,
        stream=False,
    )
    speaking_person_str_upper_case = speaking_person_str.upper()
    speaking_person_str_upper_case = speaking_person_str_upper_case.strip()
    speaking_person_bot_answer_beginning = f'{speaking_person_str_upper_case}: '
    len_speaking_person_bot_answer_beginning = len(speaking_person_bot_answer_beginning)
    bot_ans = str(responses.text)
    bot_ans = bot_ans.strip()
    bot_ans_beginning = bot_ans[0:len_speaking_person_bot_answer_beginning]
    speaking_person_in_bot_answer = (bot_ans_beginning.strip()).title() == (speaking_person_bot_answer_beginning.strip()).title()
    while speaking_person_in_bot_answer:
        temp_bot_ans = bot_ans[len_speaking_person + 1:]
        bot_ans_beginning = temp_bot_ans[0:len_speaking_person_bot_answer_beginning]
        temp_bot_ans = temp_bot_ans.replace("  ", " ")
        bot_ans = temp_bot_ans
        speaking_person_in_bot_answer = (bot_ans_beginning.strip()).title() == (speaking_person_bot_answer_beginning.strip()).title()
    bot_ans_has_speaking_person = bot_ans.startswith(speaking_person_bot_answer_beginning.strip())
    if not  bot_ans_has_speaking_person:
        bot_ans = speaking_person_bot_answer_beginning + bot_ans
    bot_ans = str(bot_ans.strip())
    count_of_speaking_persons = count_speaking_person_in_bots_ans(bot_ans=bot_ans,
                                                                  speaking_person=speaking_person_bot_answer_beginning)

    while (count_of_speaking_persons > 1):
        bot_ans = bot_ans.replace(bot_ans, speaking_person_bot_answer_beginning, 1)
        count_of_speaking_persons = count_speaking_person_in_bots_ans(bot_ans=bot_ans,
                                                                      speaking_person=speaking_person_bot_answer_beginning)

    bot_response = str(bot_ans)

    chat_history_str = f"""{chat_history_str}
{bot_response}"""
    chat_history_str = str(chat_history_str)
    chat_history_str = chat_history_str.strip()
    chat_history_str = f"""{chat_history_str}
"""
    chat_history.set(chat_history_str)

    for response in responses:
        if len(response.text) > 0:
            output_text = output_text + response.text + "\n"
            output_text = str(output_text)
    return output_text


def send_question_and_get_answer():
    global chat_history_str_question
    bot_person_dropdown.config(state=tkinter.DISABLED)
    question_entry.config(state=DISABLED)
    send_question_button.config(state=DISABLED)
    end_chat_button.config(state=NORMAL)
    # asking question
    if ask_your_question():
        block_buttons_after_question()
        feed_for_ai = get_initial_message_for_ai()
        # getting answer
        get_answer_from_AI(initial_feed_for_AI=feed_for_ai)
    unblock_buttons_after_answer()


def end_chat():
    main_chat_lbl.config(font=chat_font_big)
    main_chat_lbl.config(justify="center")
    send_question_button.config(state=NORMAL)
    asked_question.set("")

    speaking_person_str = speaking_person.get()
    if speaking_person_str == default_chatbot_name or speaking_person_str == no_specified_bot_role:
        speaking_person_str = "our chatbot"

    goodbye_message = f'''Thank you for your conversation with {speaking_person_str}.
See you soon.
'''
    chat_history.set("")
    main_chat_lbl.update_idletasks()
    root.update_idletasks()

    # Schedule an update to the UI
    root.after(500, lambda: main_chat_lbl.config(textvariable=chat_history))

    # Set the goodbye message in chat history
    chat_history.set(goodbye_message)

    # Ensure the goodbye message is set correctly
    # Force update the UI to ensure the label is visible
    main_chat_lbl.update_idletasks()
    root.update_idletasks()

    # Schedule an update to the UI
    root.after(1000, lambda: main_chat_lbl.config(textvariable=chat_history))


    # Reset UI elements
    speaking_person.set(no_specified_bot_role)
    chosen_bot_person.set(no_specified_bot_role)
    bot_person_dropdown.config(state=tkinter.DISABLED)
    end_chat_button.config(state=DISABLED)
    question_entry.config(state=tkinter.NORMAL)
    question_entry.delete('1.0', tkinter.END)
    question_entry.config(state=tkinter.DISABLED)
    send_question_button.config(state=DISABLED)
    copy_chat_button.config(state=DISABLED)
    new_chat_button.config(state=NORMAL)
    chat_title_lbl.config(text="        ")


def new_chat():
    main_chat_lbl.config(font=chat_font)
    main_chat_lbl.config(justify="left")
    question_entry.delete('1.0', tkinter.END)
    send_question_button.config(state=tkinter.NORMAL)
    question_entry.config(state=tkinter.NORMAL)
    end_chat_button.config(state=NORMAL)
    copy_chat_button.config(state=NORMAL)
    bot_person_dropdown.config(state=tkinter.NORMAL)
    new_chat_button.config(state=tkinter.DISABLED)
    chat_history.set("")
    chat_title_lbl.config(text=default_text_for_chat_title_lbl)
    question_entry.focus_set()


def show_copy_chat_popup():
    popup = tkinter.Toplevel(background=main_window_color)
    popup.title("Chat copied")
    label = tkinter.Label(popup, bg= main_window_color, foreground=font_color,font=(font_family, button_font_size, "bold"),#  font=("Chalkduster", 15, "bold"),#   popup_font,
                          text="\n\n\n    Chat has been copied to system clipboard    \n\n\n")
    label.config(pady=10, padx=10)
    label.pack(fill=BOTH, expand=True)

    # Calculate the position to center the popup
    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (popup.winfo_reqwidth() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (popup.winfo_reqheight() // 2)
    popup.geometry(f"+{x}+{y}")

    popup.after(3000, popup.destroy)  # Close the popup after 3000 milliseconds (3 seconds)
def copy_chat_history_to_clipboard():
    '''copy chat to system clipboard'''
    pyperclip.copy(chat_history.get())
    show_copy_chat_popup()

# hover mouse on buttons
def on_enter(e):
    if (e.widget['state']==tkinter.NORMAL):
        e.widget['background'] = button_color_on_focus
def on_leave(e):
    e.widget['background'] = button_color

def focus_on_next_element(event):
    if (event.widget['state']==tkinter.NORMAL):
        event.widget.tk_focusNext().focus()
    return "break"



def update_wraplength(e):
    # Set the wraplength to the current width of the root window
    wraplength_width = get_wraplength_width()
    main_chat_lbl.config(wraplength=wraplength_width)




root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 0.3 * screen_width
window_width = int(window_width)
window_height = 0.8 * screen_height
window_height = int(window_height)
button_width = int(0.4 * window_width)
button_height = 10
label_width = int(0.6*window_width)
wraplength_width = int(0.9*window_width)

def get_wraplength_width():
    root_width = root.winfo_width()
    wr = int(0.9 * root_width)
    return wr



# fonts
title_font = tkFont.Font(family=font_family, size=title_font_size, weight="bold")
choose_person_font = tkFont.Font(family=font_family, size=choose_person_font_size, weight="bold")
button_font =  tkFont.Font(family=font_family, size=button_font_size, weight="bold")
chat_font = tkFont.Font(size=chat_font_size)
chat_font_big = tkFont.Font(family=font_family, size=(title_font_size+2), weight="bold")
root.title("AI powered chatbot")
root.geometry(f'{window_width}x{window_height}')
root.configure(bg=main_window_color)
# root.resizable(False, True)
root.resizable(True, True)
root.minsize(window_width, window_height)

speaking_person = tkinter.StringVar()
speaking_person.set(default_chatbot_name)

top_frame = Frame(root, bg=main_window_color)
top_frame.pack(fill=tkinter.X, expand=False, side=TOP)

welcome_lbl = Label(master=top_frame, bg=main_window_color, foreground=font_color, font=title_font,
                    text ="Welcome to the General Chat Bot")
welcome_lbl.pack(fill=tkinter.X, expand=False,  side=tkinter.TOP)


bot_person_frame = Frame(master=top_frame, bg=main_window_color)
bot_person_frame.pack(fill=tkinter.X, expand=False, side=tkinter.TOP)

bot_person_lbl = Label(master=bot_person_frame,bg=main_window_color, text ="Choose chatbot person",
                       foreground=font_color, font=choose_person_font)
bot_person_lbl.pack(side=tkinter.LEFT, anchor="w")


chosen_bot_person = tkinter.StringVar(master=bot_person_frame)
chosen_bot_person.set(no_specified_bot_role)
bot_person_dropdown =OptionMenu(bot_person_frame, chosen_bot_person, *bot_person_list, command=person_chosen)
bot_person_dropdown.config(background=main_window_color, width=button_width, foreground=font_color,
                           font=button_font, activebackground=button_color_on_focus)
chosen_person = chosen_bot_person.get()
bot_person_dropdown.pack(side=tkinter.RIGHT, anchor='e')

bot_person_dropdown.config(state=DISABLED)



chat_frame = Frame(master=root, bg=main_window_color)
chat_frame.pack(fill=tkinter.BOTH, expand=True)

speaking_person_lbl_text = tkinter.StringVar()

chat_title_lbl = Label(master=chat_frame, background=main_window_color, text="      ", foreground=font_color, font=button_font)
chat_title_lbl.pack(fill=tkinter.X, side=TOP)

canvas = Canvas(master=chat_frame, background=chat_field_color)
scrollbar = Scrollbar(chat_frame, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)


scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

chat_window_frame = Frame(canvas, background=chat_field_color)
canvas.create_window((0, 0), window=chat_window_frame, anchor='nw')


chat_history = StringVar()

main_chat_lbl = Label(master=chat_window_frame, background=chat_field_color, textvariable=chat_history, justify=LEFT,
                      wraplength= get_wraplength_width()
                      )
main_chat_lbl.config(font=chat_font)
main_chat_lbl.config(padx=7)
main_chat_lbl.pack(fill=BOTH, expand=True)



# Configure the canvas scroll region
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

chat_window_frame.bind("<Configure>", on_frame_configure)

# scroll mouse wheel
def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Bind the <Configure> event of the root window to the update_wraplength function
root.bind('<Configure>', update_wraplength)



bottom_frame = Frame(master=root, background=main_window_color)
bottom_frame.pack(side=BOTTOM, fill=X)

asked_question = tkinter.StringVar()

question_entry = Text(master=bottom_frame, height=3, wrap=WORD)
question_entry.pack(fill=tkinter.X, expand=True)
question_entry.config(state=DISABLED)

send_question_button = Button(master=bottom_frame, text="Send question", command=send_question_and_get_answer,
                              background=button_color, foreground=font_color,
                              font=button_font, activebackground=button_color_on_focus)
send_question_button.pack(fill=tkinter.X, expand=False)
send_question_button.config(state=DISABLED)

end_chat_button = Button(master=bottom_frame, text="End chat", command=end_chat, background=button_color,
                         foreground=font_color, font=button_font, activebackground=button_color_on_focus)
end_chat_button.pack(fill=tkinter.X, expand=False)
end_chat_button.config(state=tkinter.DISABLED)

copy_chat_button = Button(master=bottom_frame, text="Copy chat to system clipboard",
                          command=copy_chat_history_to_clipboard, background=button_color,
                         foreground=font_color, font=button_font, activebackground=button_color_on_focus)

copy_chat_button.pack(fill=tkinter.X, expand=False)
copy_chat_button.config(state=tkinter.DISABLED)

new_chat_button = Button(master=bottom_frame, text="Start a new chat", command=new_chat, background=button_color,
                         foreground=font_color, font=button_font, activebackground=button_color_on_focus)
new_chat_button.pack(fill=tkinter.X, expand=False)
new_chat_button.config(state=tkinter.NORMAL)



# Bind the enter and leave events to the buttons
send_question_button.bind("<Enter>", on_enter)
send_question_button.bind("<Leave>", on_leave)

end_chat_button.bind("<Enter>", on_enter)
end_chat_button.bind("<Leave>", on_leave)

copy_chat_button.bind("<Enter>", on_enter)
copy_chat_button.bind("<Leave>", on_leave)

new_chat_button.bind("<Enter>", on_enter)
new_chat_button.bind("<Leave>", on_leave)

# Bind the Tab key to move focus to the next widget
widgets = [bot_person_dropdown, question_entry, send_question_button, end_chat_button, copy_chat_button, new_chat_button]

for widget in widgets:
    widget.bind("<Tab>", focus_on_next_element)

# Bind focus in and focus out events to change button colors
buttons = [send_question_button, end_chat_button, copy_chat_button, new_chat_button]
for button in buttons:
    button.bind("<FocusIn>",on_enter)
    button.bind("<FocusOut>", on_leave)

for button in buttons:
    button.bind('<Return>', lambda event, btn=button: btn.invoke())

def run_chat():
    try:
    # Execute Tkinter
        root.mainloop()
    except Exception as err:
        print("Error:", str(err))
        input("Press ENTER to exit")
