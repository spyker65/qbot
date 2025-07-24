import sys
import openai
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QMessageBox
)

# Set your DeepAI API key here
openai.api_key = get_api_key()

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chatbot")
        self.setGeometry(300, 300, 600, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(QLabel("Chat History:"))
        layout.addWidget(self.chat_display)

        # User input
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.user_input)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def handle_message(self):
        user_text = self.user_input.text().strip()
        if not user_text:
            return

        # Show user message
        self.chat_display.append(f"You: {user_text}")
        self.user_input.clear()

        # Generate AI response
        try:
            response = self.get_ai_response(user_text)
            self.chat_display.append(f"AI: {response}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to get response: {e}")

    def get_ai_response(self, prompt):
        # Call DeepAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3.5 or GPT-4 if available
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None,
        )
        answer = response.choices[0].text.strip()
        return answer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotApp()
    window.show()
    sys.exit(app.exec_())
