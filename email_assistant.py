import tkinter as tk
from tkinter import messagebox
import requests


# ============================================================
# OLLAMA SETTINGS
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"


# ============================================================
# FAQ KNOWLEDGE BASE
# ============================================================

faq = {
    "pricing": "Our basic plan starts at $10/month with premium options.",
    "refund": "Refunds are available within 30 days of purchase. Please share your order ID.",
    "support": "You can reach our support team at support@example.com, 24/7.",
    "delivery": "Standard delivery usually takes 3 to 5 business days.",
    "payment": "We accept major credit cards, debit cards and online payment methods.",
    "cancellation": "You can cancel your order before it is shipped.",
}


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []


# ============================================================
# FAQ CHECK
# ============================================================

def check_faq(email_text):

    email_text = email_text.lower()

    for keyword, answer in faq.items():

        if keyword in email_text:
            return answer

    return None


# ============================================================
# OLLAMA AI RESPONSE
# ============================================================

def ollama_response(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:

            return response.json().get(
                "response",
                ""
            ).strip()

        return "Ollama Error: " + response.text

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to Ollama.\n\n"
            "Please make sure Ollama is running."
        )

    except Exception as e:

        return "Error: " + str(e)


# ============================================================
# EMAIL ASSISTANT
# ============================================================

def email_assistant(email_text):

    # Check FAQ first
    faq_answer = check_faq(email_text)

    if faq_answer:

        reply = (
            "Dear Customer,\n\n"
            + faq_answer
            + "\n\n"
            "Please let us know if you need any further assistance."
            "\n\n"
            "Best regards,\n"
            "Support Team"
        )

        response_type = "FAQ Reply"

    else:

        # Previous conversation
        history = "\n".join(conversation_history)

        prompt = f"""
You are a professional email assistant.

Previous conversation:
{history}

Incoming email:
{email_text}

Write a polite, professional and helpful email reply.

Requirements:
- Keep the reply concise.
- Use professional English.
- Answer the customer's concern clearly.
- Do not mention that you are an AI.
- Do not invent company policies or information.
"""

        reply = ollama_response(prompt)

        response_type = "AI Generated Reply"

    # Store conversation
    conversation_history.append(
        "Customer: " + email_text
    )

    conversation_history.append(
        "Assistant: " + reply
    )

    return reply, response_type


# ============================================================
# GENERATE REPLY BUTTON
# ============================================================

def generate_reply():

    email_text = email_input.get(
        "1.0",
        tk.END
    ).strip()

    if not email_text:

        messagebox.showwarning(
            "Empty Email",
            "Please enter an email message."
        )

        return

    # Disable button while processing
    generate_button.config(
        state=tk.DISABLED,
        text="Generating..."
    )

    root.update()

    reply, response_type = email_assistant(
        email_text
    )

    # Display reply
    reply_output.config(
        state=tk.NORMAL
    )

    reply_output.delete(
        "1.0",
        tk.END
    )

    reply_output.insert(
        tk.END,
        reply
    )

    reply_output.config(
        state=tk.DISABLED
    )

    # Update status
    status_label.config(
        text="● " + response_type
    )

    # Re-enable button
    generate_button.config(
        state=tk.NORMAL,
        text="Generate Reply"
    )


# ============================================================
# CLEAR BUTTON
# ============================================================

def clear_all():

    email_input.delete(
        "1.0",
        tk.END
    )

    reply_output.config(
        state=tk.NORMAL
    )

    reply_output.delete(
        "1.0",
        tk.END
    )

    reply_output.config(
        state=tk.DISABLED
    )

    status_label.config(
        text="● Ready"
    )


# ============================================================
# EXIT BUTTON
# ============================================================

def exit_application():

    result = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if result:

        root.destroy()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Intelligent Email Assistant"
)

root.geometry(
    "900x700"
)

root.minsize(
    750,
    600
)

root.configure(
    bg="#F4F6F8"
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg="#263238",
    height=90
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title_label = tk.Label(
    header,
    text="🤖 Intelligent Email Assistant",
    font=("Segoe UI", 22, "bold"),
    bg="#263238",
    fg="white"
)

title_label.pack(
    pady=(15, 2)
)


subtitle_label = tk.Label(
    header,
    text="FAQ + Ollama AI + Conversation Memory",
    font=("Segoe UI", 10),
    bg="#263238",
    fg="#CFD8DC"
)

subtitle_label.pack()


# ============================================================
# MAIN CONTAINER
# ============================================================

main_frame = tk.Frame(
    root,
    bg="#F4F6F8"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=20
)


# ============================================================
# EMAIL SECTION
# ============================================================

email_label = tk.Label(
    main_frame,
    text="Incoming Email",
    font=("Segoe UI", 13, "bold"),
    bg="#F4F6F8",
    fg="#263238"
)

email_label.pack(
    anchor="w",
    pady=(0, 8)
)


email_input = tk.Text(
    main_frame,
    height=7,
    font=("Segoe UI", 11),
    wrap="word",
    relief="solid",
    bd=1,
    padx=12,
    pady=10
)

email_input.pack(
    fill="x"
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    main_frame,
    bg="#F4F6F8"
)

button_frame.pack(
    pady=15
)


generate_button = tk.Button(
    button_frame,
    text="Generate Reply",
    command=generate_reply,
    font=("Segoe UI", 11, "bold"),
    bg="#1976D2",
    fg="white",
    activebackground="#1565C0",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

generate_button.pack(
    side="left",
    padx=6
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_all,
    font=("Segoe UI", 11, "bold"),
    bg="#757575",
    fg="white",
    activebackground="#616161",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

clear_button.pack(
    side="left",
    padx=6
)


exit_button = tk.Button(
    button_frame,
    text="Exit",
    command=exit_application,
    font=("Segoe UI", 11, "bold"),
    bg="#D32F2F",
    fg="white",
    activebackground="#B71C1C",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

exit_button.pack(
    side="left",
    padx=6
)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    main_frame,
    text="● Ready",
    font=("Segoe UI", 10, "bold"),
    bg="#F4F6F8",
    fg="#388E3C"
)

status_label.pack(
    anchor="w",
    pady=(0, 8)
)


# ============================================================
# REPLY SECTION
# ============================================================

reply_label = tk.Label(
    main_frame,
    text="Suggested Professional Reply",
    font=("Segoe UI", 13, "bold"),
    bg="#F4F6F8",
    fg="#263238"
)

reply_label.pack(
    anchor="w",
    pady=(5, 8)
)


reply_output = tk.Text(
    main_frame,
    height=12,
    font=("Segoe UI", 11),
    wrap="word",
    relief="solid",
    bd=1,
    padx=12,
    pady=10,
    bg="#FFFFFF"
)

reply_output.pack(
    fill="both",
    expand=True
)

reply_output.config(
    state=tk.DISABLED
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text="Powered by Python • Tkinter • Ollama • Qwen",
    font=("Segoe UI", 9),
    bg="#ECEFF1",
    fg="#607D8B",
    pady=8
)

footer.pack(
    fill="x"
)


# ============================================================
# START GUI
# ============================================================

root.mainloop()
