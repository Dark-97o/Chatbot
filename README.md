# Customer Service Chatbot

A Python-based customer service chatbot designed to handle common customer inquiries such as order tracking, refunds, shipping information, and product details. The chatbot uses natural language processing techniques to detect user intents, match FAQ responses, and escalate unresolved issues to human agents when necessary.

## Features

- **Intent Detection**: Identifies user intents (e.g., greeting, order inquiry, refund request) using regex patterns and keyword similarity matching.
- **FAQ Matching**: Responds with pre-defined answers for frequently asked questions.
- **Order Number Extraction**: Parses order numbers from user input for order status queries.
- **Conversation Logging**: Maintains a history of user interactions with timestamps, intents, and confidence scores.
- **Escalation Mechanism**: Offers escalation to a human agent after multiple unresolved queries.
- **Error Handling**: Gracefully handles empty inputs, keyboard interrupts, and unexpected errors.

## Requirements

- Python 3.6+
- Standard library modules: `re`, `json`, `datetime`, `typing`, `difflib`, `random`

No external dependencies are required.

## Installation

Clone or download the project repository.

1. Ensure Python 3.6 or higher is installed.
2. Place the script (`chatbot.py`) in your desired directory.

## Usage

1. Run the script using Python:

   ```bash
   python chatbot.py
   ```
2. Interact with the chatbot by typing your queries.
3. Type `quit`, `exit`, `bye`, or `goodbye` to end the session.

Example interaction:

```
🤖 CUSTOMER SERVICE CHATBOT
================================
Hello! I'm your virtual assistant. I can help with:
• Order tracking and status
• Product information
• Returns and refunds
• Shipping information
• General customer service questions

Type 'quit' or 'exit' to end the conversation.
================================

👤 You: Where is my order #ORD12345?

🤖 Bot: I found order number ORD12345. Let me check the status... Your order is currently being processed and will ship within 1-2 business days.

👤 You: What is your refund policy?

🤖 Bot: We offer full refunds within 30 days of purchase for unused items in original packaging.

👤 You: exit

🤖 Bot: Thank you for using our customer service! Have a great day! 👋
```

## Project Structure

- `chatbot.py`: The main script containing the `CustomerServiceChatbot` class and command-line interface.
- `README.md`: This file, providing project documentation.

## How It Works

1. **Initialization**: The chatbot loads predefined intents, response templates, FAQ data, and regex patterns.
2. **Text Preprocessing**: User input is cleaned (lowercase, punctuation removal, whitespace normalization).
3. **Intent Detection**:
   - Matches user input against regex patterns for quick intent identification.
   - If no pattern matches, uses keyword extraction and similarity scoring to determine the best intent.
4. **Response Generation**:
   - Checks FAQ for direct matches.
   - Extracts order numbers for order inquiries.
   - Selects a random response from the appropriate intent's template.
   - Escalates to human agent if multiple queries remain unresolved.
5. **Conversation Logging**: Stores each interaction with timestamp, input, response, intent, and confidence.

## Customization

- **Intents**: Modify `_load_intents()` to add or adjust intents and their keywords/confidence thresholds.
- **Responses**: Update `_load_responses()` to change response templates or add new ones.
- **FAQ**: Edit `_load_faq()` to include additional questions and answers.
- **Patterns**: Adjust `patterns` dictionary to refine regex-based intent detection.
- **Escalation Threshold**: Change `escalation_threshold` to control when human escalation is offered.

## Limitations

- Lacks external API integration for real-time order or shipping data.
- Intent detection may struggle with ambiguous or complex queries.
- No persistent storage for conversation history or user context.
- Limited to English language processing.

## Future Improvements

- Integrate with a database or API for real-time order tracking.
- Implement machine learning for improved intent classification.
- Add multi-language support.
- Include persistent storage for conversation history.
- Enhance FAQ matching with advanced NLP techniques.

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a clear description of changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.