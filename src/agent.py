import os
import re
from typing import Dict, Any, Tuple
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

from src.prompts import CODE_GENERATION_PROMPT, INSIGHTS_PROMPT

load_dotenv()

class BIAgent:
    def __init__(self, api_key: str = None):
        """Initializes the BI Agent with Google Gemini client."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required. Please set it in .env or pass to constructor.")
        
        genai.configure(api_key=self.api_key)
        self.model_name = self._resolve_active_model()

    def _resolve_active_model(self) -> str:
        """Discovers available generateContent models based on your exact API key access."""
        try:
            available_models = [
                m.name.replace("models/", "") 
                for m in genai.list_models() 
                if "generateContent" in m.supported_generation_methods
            ]
            
            # Prioritized list matching your available models
            priority_models = [
                "gemini-3.8-flash",
                "gemini-3.5-flash",
                "gemini-2.5-flash",
                "gemini-flash-latest",
                "gemini-1.5-flash"
            ]
            
            for candidate in priority_models:
                if candidate in available_models:
                    return candidate
            
            if available_models:
                return available_models[0]
                
        except Exception:
            pass
            
        return "gemini-3.8-flash"

    def _clean_code(self, raw_code: str) -> str:
        """Strips markdown formatting if the LLM includes markdown code fences."""
        cleaned = re.sub(r'```python\s*', '', raw_code)
        cleaned = re.sub(r'```\s*', '', cleaned)
        return cleaned.strip()

    def generate_pandas_code(self, question: str, schema_info: Dict[str, Any]) -> str:
        """Generates Python code based on schema context and user question."""
        prompt = CODE_GENERATION_PROMPT.format(
            columns=schema_info["columns"],
            dtypes=schema_info["dtypes"],
            sample_rows=schema_info["sample_rows"],
            question=question
        )
        
        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"temperature": 0.0}
        )
        response = model.generate_content(prompt)
        return self._clean_code(response.text)

    def execute_code(self, code_str: str, df: pd.DataFrame) -> Tuple[Any, Any, str]:
        """
        Executes generated code in a controlled local scope.
        Returns: (result_df, fig, error_message)
        """
        local_scope = {
            "customer_orders_df": df.copy(),
            "pd": pd
        }
        
        try:
            exec(code_str, local_scope, local_scope)
            
            result_df = local_scope.get("result_df", None)
            fig = local_scope.get("fig", None)
            
            if result_df is None and fig is None:
                return None, None, "Code executed successfully but did not produce 'result_df' or 'fig'."
                
            return result_df, fig, None

        except Exception as e:
            return None, None, f"Python Execution Error: {str(e)}"

    def generate_insights(self, question: str, result: Any) -> str:
        """Generates structured narrative explanation and business recommendations."""
        if isinstance(result, (pd.DataFrame, pd.Series)):
            result_summary = result.to_string()
        else:
            result_summary = str(result)
            
        prompt = INSIGHTS_PROMPT.format(
            question=question,
            result_summary=result_summary
        )
        
        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"temperature": 0.2}
        )
        response = model.generate_content(prompt)
        return response.text

    def run_pipeline(self, question: str, df: pd.DataFrame, schema_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        End-to-End Execution Pipeline:
        1. Code Generation
        2. Local Pandas Execution & Visual Extraction
        3. LLM Insight Generation
        """
        code_str = self.generate_pandas_code(question, schema_info)
        result_df, fig, error = self.execute_code(code_str, df)
        
        if error:
            return {
                "success": False,
                "error": error,
                "code": code_str,
                "result": None,
                "fig": None,
                "insights": None
            }
            
        insights = self.generate_insights(question, result_df if result_df is not None else "Visualization Generated")
        
        return {
            "success": True,
            "error": None,
            "code": code_str,
            "result": result_df,
            "fig": fig,
            "insights": insights
        }