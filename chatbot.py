import re
import json
import datetime
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import random

class CustomerServiceChatbot:
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        self.escalation_threshold = 3  
        self.unresolved_count = 0
        self.intents = self._load_intents()
        self.responses = self._load_responses()
        self.faq = self._load_faq()
        self.patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\bgreetings\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|farewell|exit|quit)\b',
                r'\btalk to you later\b'
            ],
            'order_status': [
                r'\border\b.*\b(status|track|where|when)\b',
                r'\btrack\b.*\border\b',
                r'\bwhere is my order\b',
                r'\border number\b.*\d+'
            ],
            'refund': [
                r'\b(refund|money back|return|cancel order)\b',
                r'\bget my money back\b'
            ],
            'shipping': [
                r'\b(shipping|delivery|ship|deliver)\b',
                r'\bhow long.*deliver\b',
                r'\bshipping cost\b'
            ],
            'product_info': [
                r'\bproduct\b.*\b(info|details|specification|features)\b',
                r'\btell me about\b',
                r'\bwhat is\b.*\bproduct\b'
            ],
            'complaint': [
                r'\b(complaint|problem|issue|wrong|broken|defective)\b',
                r'\bnot working\b',
                r'\bbad quality\b'
            ],
            'human_agent': [
                r'\b(human|agent|representative|person|talk to someone)\b',
                r'\bspeak to.*person\b'
            ]
        }
    
    def _load_intents(self) -> Dict:
        return {
            'greeting': {
                'keywords': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'],
                'confidence_threshold': 0.6
            },
            'order_inquiry': {
                'keywords': ['order', 'track', 'status', 'delivery', 'shipped', 'tracking number'],
                'confidence_threshold': 0.7
            },
            'product_info': {
                'keywords': ['product', 'item', 'features', 'specifications', 'details', 'price'],
                'confidence_threshold': 0.6
            },
            'refund_return': {
                'keywords': ['refund', 'return', 'money back', 'cancel', 'exchange'],
                'confidence_threshold': 0.7
            },
            'shipping_info': {
                'keywords': ['shipping', 'delivery', 'cost', 'time', 'free shipping'],
                'confidence_threshold': 0.6
            },
            'complaint': {
                'keywords': ['problem', 'issue', 'complaint', 'broken', 'defective', 'wrong'],
                'confidence_threshold': 0.7
            },
            'human_escalation': {
                'keywords': ['human', 'agent', 'representative', 'person', 'manager'],
                'confidence_threshold': 0.8
            }
        }
    
    def _load_responses(self) -> Dict:
        return {
            'greeting': [
                "Hello! Welcome to our customer service. How can I help you today?",
                "Hi there! I'm here to assist you with any questions or concerns.",
                "Good day! What can I help you with today?"
            ],
            'goodbye': [
                "Thank you for contacting us! Have a great day!",
                "Goodbye! Feel free to reach out if you need any more help.",
                "Take care! We're always here if you need assistance."
            ],
            'order_inquiry': [
                "I'd be happy to help you with your order! Could you please provide your order number?",
                "To check your order status, I'll need your order number. It usually starts with #ORD.",
                "Let me help you track your order. Please share your order number or email address."
            ],
            'product_info': [
                "I can help you with product information! Which product are you interested in?",
                "What specific product details would you like to know about?",
                "I'm here to help with product questions. What would you like to learn about?"
            ],
            'refund_return': [
                "I understand you'd like to return or get a refund. Let me help you with that process.",
                "I can assist you with returns and refunds. Could you tell me more about your order?",
                "Our return policy allows returns within 30 days. What item would you like to return?"
            ],
            'shipping_info': [
                "I can provide shipping information! What would you like to know?",
                "For shipping details, I can help! Are you asking about costs, delivery time, or tracking?",
                "We offer various shipping options. What specific shipping information do you need?"
            ],
            'complaint': [
                "I'm sorry to hear about the issue you're experiencing. Let me help resolve this for you.",
                "I apologize for any inconvenience. Could you please describe the problem in detail?",
                "I understand your concern and I'm here to help. What specific issue are you facing?"
            ],
            'human_escalation': [
                "I'll connect you with a human agent right away. Please hold on.",
                "Let me transfer you to one of our customer service representatives.",
                "I'm escalating your request to a human agent who can better assist you."
            ],
            'default': [
                "I understand your question, but I might need more information to help you better.",
                "Could you please rephrase that? I want to make sure I help you correctly.",
                "I'm not sure I fully understand. Could you provide more details?"
            ],
            'escalation_offer': [
                "I notice we haven't been able to resolve your issue yet. Would you like to speak with a human agent?",
                "Since I haven't been able to help you fully, would you prefer to talk to one of our representatives?",
                "I can connect you with a human agent who might better assist with your specific needs."
            ]
        }
    
    def _load_faq(self) -> Dict:
        return {
            "what are your business hours": "Our customer service is available Monday-Friday 9AM-6PM EST, and Saturday 10AM-4PM EST.",
            "how do i return an item": "You can return items within 30 days of purchase. Visit our returns page or I can help you start the process.",
            "what is your refund policy": "We offer full refunds within 30 days of purchase for unused items in original packaging.",
            "how much does shipping cost": "Standard shipping is $5.99, free on orders over $50. Express shipping is $12.99.",
            "how long does shipping take": "Standard shipping takes 3-5 business days, express shipping takes 1-2 business days.",
            "can i change my order": "If your order hasn't shipped yet, we can modify it. Please provide your order number.",
            "do you ship internationally": "Yes, we ship to most countries. International shipping costs vary by location.",
            "how do i track my order": "You can track your order using the tracking number sent to your email, or provide your order number here."
        }
    
    def preprocess_text(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\?\!\.]', '', text)
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                     'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                     'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                     'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                     'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                     'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                     'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
                     'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                     'further', 'then', 'once', 'can', 'could', 'would', 'should'}
        
        words = text.split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        return SequenceMatcher(None, text1, text2).ratio()
    
    def match_pattern(self, user_input: str) -> Optional[str]:
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return intent
        return None
    
    def detect_intent(self, user_input: str) -> Tuple[str, float]:
        preprocessed_input = self.preprocess_text(user_input)
        keywords = self.extract_keywords(preprocessed_input)
        pattern_match = self.match_pattern(preprocessed_input)
        if pattern_match:
            return pattern_match, 0.9
        best_intent = 'default'
        best_score = 0.0
        for intent, intent_data in self.intents.items():
            score = 0.0
            intent_keywords = intent_data['keywords']
            for keyword in keywords:
                for intent_keyword in intent_keywords:
                    similarity = self.calculate_similarity(keyword, intent_keyword)
                    if similarity > 0.8:  
                        score += similarity
            if len(intent_keywords) > 0:
                score = score / len(intent_keywords)
            
            if score > best_score and score >= intent_data['confidence_threshold']:
                best_score = score
                best_intent = intent
        
        return best_intent, best_score
    
    def check_faq(self, user_input: str) -> Optional[str]:
        preprocessed_input = self.preprocess_text(user_input)
        
        best_match = None
        best_score = 0.0
        
        for question, answer in self.faq.items():
            similarity = self.calculate_similarity(preprocessed_input, question)
            if similarity > best_score and similarity > 0.6:
                best_score = similarity
                best_match = answer
        
        return best_match
    
    def extract_order_number(self, text: str) -> Optional[str]:
        patterns = [
            r'#?ORD\d+',
            r'order\s+(?:number\s+)?#?(\w+)',
            r'#(\d{6,})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)
        return None
    
    def generate_response(self, intent: str, user_input: str) -> str:
        faq_response = self.check_faq(user_input)
        if faq_response:
            self.unresolved_count = 0  
            return faq_response
        if intent == 'order_inquiry':
            order_num = self.extract_order_number(user_input)
            if order_num:
                return f"I found order number {order_num}. Let me check the status... Your order is currently being processed and will ship within 1-2 business days."
        response_templates = self.responses.get(intent, self.responses['default'])
        response = random.choice(response_templates)
        if intent == 'default':
            self.unresolved_count += 1
            if self.unresolved_count >= self.escalation_threshold:
                escalation_response = random.choice(self.responses['escalation_offer'])
                return f"{response} {escalation_response}"
        else:
            self.unresolved_count = 0
        
        return response
    
    def log_conversation(self, user_input: str, bot_response: str, intent: str, confidence: float):
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': bot_response,
            'detected_intent': intent,
            'confidence': confidence
        }
        self.conversation_history.append(log_entry)
    
    def get_response(self, user_input: str) -> str:
        if not user_input.strip():
            return "I didn't receive any input. How can I help you today?"
        intent, confidence = self.detect_intent(user_input)
        response = self.generate_response(intent, user_input)
        self.log_conversation(user_input, response, intent, confidence)
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history
    
    def reset_conversation(self):
        self.conversation_history = []
        self.user_context = {}
        self.unresolved_count = 0

def main():
    print("🤖 CUSTOMER SERVICE CHATBOT")
    print("================================")
    print("Hello! I'm your virtual assistant. I can help with:")
    print("• Order tracking and status")
    print("• Product information")
    print("• Returns and refunds")
    print("• Shipping information")
    print("• General customer service questions")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("="*60)
    
    chatbot = CustomerServiceChatbot()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 Bot: Thank you for using our customer service! Have a great day! 👋")
                break
            
            response = chatbot.get_response(user_input)
            print(f"\n🤖 Bot: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Thank you for using our customer service! Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n🤖 Bot: I apologize, but I encountered an error. Please try again or contact human support.")
            print(f"Error details: {str(e)}")

if __name__ == "__main__":
    main()