import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from typing import List, Dict, Optional
from app.core.config import settings
from app.utils.logger import logger
from app.utils.cache import cache_manager


class AIService:
    """AI service for handling different AI providers"""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.model = settings.AI_MODEL
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        
        # Initialize based on provider
        if self.provider == "gemini":
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai.GenerativeModel(self.model)
            logger.info("Gemini AI initialized")
            
        elif self.provider == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("OpenAI initialized")
            
        elif self.provider == "groq":
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("Groq AI initialized")
        else:
            logger.error(f"Unknown AI provider: {self.provider}")
            raise ValueError(f"Unknown AI provider: {self.provider}")
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        system_prompt: Optional[str] = None,
        custom_context: Optional[str] = None
    ) -> str:
        """
        Generate AI response based on provider
        
        Args:
            user_message: Current user message
            conversation_history: List of previous messages
            system_prompt: Custom system prompt
            custom_context: Additional context (for RAG)
        
        Returns:
            AI generated response
        """
        try:
            # Check cache first
            cache_key = f"ai_response:{hash(user_message)}"
            cached_response = cache_manager.get(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return cached_response
            
            # Generate response based on provider
            if self.provider == "gemini":
                response = await self._generate_gemini(
                    user_message, conversation_history, system_prompt, custom_context
                )
            elif self.provider == "openai":
                response = await self._generate_openai(
                    user_message, conversation_history, system_prompt, custom_context
                )
            elif self.provider == "groq":
                response = await self._generate_groq(
                    user_message, conversation_history, system_prompt, custom_context
                )
            else:
                response = "Sorry, AI service is not available."
            
            # Cache response for 1 hour
            cache_manager.set(cache_key, response, expire=3600)
            
            return response
            
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            return "Sorry, I encountered an error. Please try again."
    
    async def _generate_gemini(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str],
        custom_context: Optional[str]
    ) -> str:
        """Generate response using Gemini"""
        try:
            # Build prompt
            prompt = self._build_prompt(
                user_message, conversation_history, system_prompt, custom_context
            )
            
            # Generate response
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise
    
    async def _generate_openai(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str],
        custom_context: Optional[str]
    ) -> str:
        """Generate response using OpenAI"""
        try:
            # Build messages
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                })
            
            # Add custom context if provided
            if custom_context:
                messages.append({
                    "role": "system",
                    "content": f"Context: {custom_context}"
                })
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-settings.MAX_CONVERSATION_HISTORY:]:
                    messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise
    
    async def _generate_groq(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str],
        custom_context: Optional[str]
    ) -> str:
        """Generate response using Groq"""
        try:
            # Build messages (same as OpenAI format)
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                })
            
            if custom_context:
                messages.append({
                    "role": "system",
                    "content": f"Context: {custom_context}"
                })
            
            if conversation_history:
                for msg in conversation_history[-settings.MAX_CONVERSATION_HISTORY:]:
                    messages.append(msg)
            
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise
    
    def _build_prompt(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str],
        custom_context: Optional[str]
    ) -> str:
        """Build complete prompt for Gemini"""
        parts = []
        
        # Add system prompt
        if system_prompt:
            parts.append(f"System: {system_prompt}\n")
        else:
            parts.append("System: You are a helpful AI assistant.\n")
        
        # Add custom context
        if custom_context:
            parts.append(f"\nContext: {custom_context}\n")
        
        # Add conversation history
        if conversation_history:
            parts.append("\nConversation History:\n")
            for msg in conversation_history[-settings.MAX_CONVERSATION_HISTORY:]:
                role = "User" if msg["role"] == "user" else "Assistant"
                parts.append(f"{role}: {msg['content']}\n")
        
        # Add current message
        parts.append(f"\nUser: {user_message}\n")
        parts.append("Assistant:")
        
        return "".join(parts)
    
    async def get_embedding(self, text: str) -> List[float]:
        """
        Get text embedding for RAG
        Currently supports OpenAI embeddings
        """
        try:
            if self.provider == "openai" or settings.OPENAI_API_KEY:
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=text
                )
                return response.data[0].embedding
            else:
                logger.warning("Embeddings not supported for this provider")
                return []
                
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            return []