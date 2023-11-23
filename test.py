import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import openai
import threading
import os

# Replace 'your-api-key-here' with your actual OpenAI API key
# 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
openai.api_key = os.getenv('OPENAI_API_KEY', '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')

class ChatGPTApp:
    def __init__(self, root):
        self.root = root
        root.title("ChatGPT Prompter")

        # Main frame setup
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=15, pady=15, expand=True, fill='both')
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Input field for user prompts
        self.input_text = ttk.Entry(self.main_frame, width=80)
        self.input_text.pack(pady=(0, 10))
        self.input_text.bind("<Return>", self.send_prompt)

        # Send button
        self.send_button = ttk.Button(self.main_frame, text="Send", command=self.send_prompt)
        self.send_button.pack(pady=(0, 10))

        # Conversation history management frame
        self.history_frame = ttk.Frame(self.main_frame)
        self.history_frame.pack(pady=(10, 0), fill='x')
        self.history_frame.grid_columnconfigure(0, weight=1)

        self.save_button = ttk.Button(self.history_frame, text="Save Conversation", command=self.save_conversation)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = ttk.Button(self.history_frame, text="Load Conversation", command=self.load_conversation)
        self.load_button.pack(side=tk.LEFT)

        # Settings frame for model selection and presets
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack(pady=(10, 0), fill='x')
        self.settings_frame.grid_columnconfigure(0, weight=1)

        self.model_label = ttk.Label(self.settings_frame, text="Choose Model:")
        self.model_label.pack(side=tk.LEFT, padx=5)

        self.model_var = tk.StringVar()
        self.models = ['text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001', 'gpt-4']
        self.model_var.set(self.models[0])  # default value
        self.model_dropdown = ttk.OptionMenu(self.settings_frame, self.model_var, *self.models)
        self.model_dropdown.pack(side=tk.LEFT)

        self.preset_label = ttk.Label(self.settings_frame, text="Preset:")
        self.preset_label.pack(side=tk.LEFT, padx=5)

        self.preset_var = tk.StringVar()
        self.presets = ['Default', 'Creative Writing', 'Technical Help', 'Casual Chat']
        self.preset_var.set(self.presets[0])  # default value
        self.preset_dropdown = ttk.OptionMenu(self.settings_frame, self.preset_var, *self.presets)
        self.preset_dropdown.pack(side=tk.LEFT)

        # Response area with scrolling
        self.response_area = scrolledtext.ScrolledText(self.main_frame, height=15, width=80)
        self.response_area.pack(padx=5, pady=5, fill='both', expand=True)

        # Loading indicator (initially hidden)
        self.loading_label = ttk.Label(self.main_frame, text="Loading...", foreground="red")
        self.loading_label.pack(pady=5)
        self.loading_label.pack_forget()  # Hide initially

    def send_prompt(self, event=None):
        prompt_text = self.input_text.get()
        self.input_text.delete(0, tk.END)
        threading.Thread(target=self.fetch_response, args=(prompt_text,)).start()

    def fetch_response(self, prompt):
        self.display_loading(True)
        selected_model = self.model_var.get()
        preset = self.preset_var.get()
        # Add preset logic here if needed
        try:
            response = openai.ChatCompletion.create(model=selected_model, messages=[{"role": "user", "content": prompt}])
            self.display_response(prompt, response.choices[0].message.content)
        finally:
            self.display_loading(False)

    def display_response(self, prompt, response):
        self.response_area.insert(tk.END, f"\nUser: {prompt}\nChatGPT: {response}\n")
        self.response_area.see(tk.END)

    def display_loading(self, loading):
        if loading:
            self.loading_label.pack()
        else:
            self.loading_label.pack_forget()

    def save_conversation(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                conversation_text = self.response_area.get("1.0", tk.END)
                file.write(conversation_text)
                messagebox.showinfo("Success", "Conversation saved successfully.")

    def load_conversation(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                conversation_text = file.read()
                self.response_area.delete("1.0", tk.END)
                self.response_area.insert("1.0", conversation_text)

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    root.geometry("700x500")  # Set initial window size
    app = ChatGPTApp(root)
    root.mainloop()
