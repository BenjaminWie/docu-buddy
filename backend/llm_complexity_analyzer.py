#!/usr/bin/env python3
"""
Phase 2: LLM-Based Code Complexity Analysis
Uses OpenAI API to provide semantic complexity analysis of the top complex functions
"""

import json
import re
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from openai import OpenAI


@dataclass
class LLMComplexityMetrics:
    """Container for LLM-based complexity analysis"""

    semantic_complexity: int = 0  # 1-10 scale
    cognitive_load: int = 0  # 1-10 scale
    maintainability: int = 0  # 1-10 scale
    documentation_quality: int = 0  # 1-10 scale
    refactoring_urgency: int = 0  # 1-10 scale
    explanation: str = ""
    suggestions: List[str] = None
    final_score: float = 0.0

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


class LLMComplexityAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        """
        Initialize the LLM analyzer

        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens_per_request = 4000  # Adjust based on your model

        # Language-specific patterns for dependency extraction
        self.dependency_patterns = {
            "java": r"\b(\w+)\s*\(",
            "kotlin": r"\b(\w+)\s*\(",
            "typescript": r"\b(\w+)\s*\(",
            "javascript": r"\b(\w+)\s*\(",
            "groovy": r"\b(\w+)\s*\(",
            "python": r"\b(\w+)\s*\(",
            "csharp": r"\b(\w+)\s*\(",
            "cpp": r"\b(\w+)\s*\(",
            "go": r"\b(\w+)\s*\(",
        }

    def extract_function_calls(self, code: str, language: str) -> List[str]:
        """Extract function calls from code"""
        if language not in self.dependency_patterns:
            return []

        pattern = self.dependency_patterns[language]
        matches = re.findall(pattern, code)

        # Filter out common keywords and built-ins
        keywords = {
            "if",
            "for",
            "while",
            "switch",
            "try",
            "catch",
            "return",
            "new",
            "class",
            "function",
            "var",
            "let",
            "const",
            "def",
            "print",
            "console",
            "log",
            "toString",
            "length",
            "size",
        }

        return [match for match in set(matches) if match.lower() not in keywords]

    def find_related_functions(
        self, target_function: Dict[str, Any], all_functions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find functions that are called by the target function"""
        if not target_function.get("function_content"):
            return []

        # Extract function calls from target function
        called_functions = self.extract_function_calls(
            target_function["function_content"], target_function["language"]
        )

        # Find matching functions in the codebase
        related = []
        for func in all_functions:
            if func["function_name"] in called_functions:
                # Limit to same file or same package for relevance
                if func["file_path"] == target_function["file_path"] or os.path.dirname(
                    func["file_path"]
                ) == os.path.dirname(target_function["file_path"]):
                    related.append(func)

        # Limit to top 5 most relevant dependencies
        return related[:5]

    def build_analysis_context(
        self, target_function: Dict[str, Any], related_functions: List[Dict[str, Any]]
    ) -> str:
        """Build comprehensive context for LLM analysis"""

        context_parts = []

        # Add target function
        context_parts.append("=== TARGET FUNCTION FOR ANALYSIS ===")
        context_parts.append(f"Function: {target_function['function_name']}")
        context_parts.append(f"File: {target_function['file_path']}")
        context_parts.append(f"Language: {target_function['language']}")
        context_parts.append(
            f"Lines: {target_function['start_line']}-{target_function['end_line']}"
        )
        context_parts.append("\nPhase 1 Structural Complexity Metrics:")
        for metric, value in target_function["reason_for_complexity"].items():
            context_parts.append(f"  - {metric}: {value}")

        context_parts.append(
            f"\nStructural Complexity Score: {target_function['total_complexity_score']:.2f}"
        )
        context_parts.append("\n=== FUNCTION CODE ===")
        context_parts.append(target_function["function_content"])

        # Add related functions for context
        if related_functions:
            context_parts.append("\n=== RELATED FUNCTIONS (Dependencies) ===")
            for i, func in enumerate(related_functions, 1):
                context_parts.append(
                    f"\n--- Related Function {i}: {func['function_name']} ---"
                )
                context_parts.append(func["function_content"])

        return "\n".join(context_parts)

    def create_analysis_prompt(self, context: str) -> str:
        """Create the prompt for LLM analysis"""

        prompt = f"""You are an expert code reviewer analyzing function complexity. Your goal is to provide DIFFERENTIATED ratings that distinguish between functions of varying complexity levels.

CONTEXT:
{context}

ANALYSIS REQUIREMENTS:

Rate each aspect on a 1-10 scale. BE SPECIFIC and use the FULL RANGE of scores:
- Use 1-3 for simple/excellent code
- Use 4-6 for moderate complexity  
- Use 7-8 for high complexity
- Use 9-10 for extremely complex/problematic code

**IMPORTANT: Functions should receive DIFFERENT scores based on their actual complexity. Avoid giving similar ratings to all functions.**

1. **Semantic Complexity** (1-10): How difficult is the logic to understand?
   - 1-3: Simple logic, clear algorithm, minimal domain knowledge needed
   - 4-6: Moderate logic with some complexity, reasonable algorithm
   - 7-8: Complex business logic, intricate algorithms, domain expertise needed
   - 9-10: Extremely complex logic, multiple interacting algorithms, expert-level domain knowledge

2. **Cognitive Load** (1-10): How much mental effort to comprehend?
   - 1-3: Easy to follow, minimal variable tracking, clear execution flow
   - 4-6: Some mental effort needed, moderate state tracking
   - 7-8: High mental effort, complex state management, difficult to trace execution
   - 9-10: Overwhelming mental effort, too many variables/states to track

3. **Maintainability** (1-10): How difficult would this be to modify safely?
   - 1-3: Easy to change, well-isolated, good testability
   - 4-6: Moderate change difficulty, some coupling
   - 7-8: Risky to change, high coupling, hard to test
   - 9-10: Extremely risky to modify, tightly coupled, change impact unpredictable

4. **Documentation Quality** (1-10): How well documented is this code?
   - 1-3: Excellent docs, clear comments, self-documenting
   - 4-6: Adequate documentation, some gaps
   - 7-8: Poor documentation, minimal comments
   - 9-10: No meaningful documentation, completely unclear

5. **Refactoring Urgency** (1-10): How urgently does this need refactoring?
   - 1-3: No refactoring needed, well-structured
   - 4-6: Minor improvements possible
   - 7-8: Should be refactored soon, causing some problems
   - 9-10: Critical refactoring needed immediately, major technical debt

**CALIBRATION GUIDANCE:**
- Look at the structural metrics provided - they give you baseline complexity indicators
- A function with cyclomatic complexity of 15+ should likely get higher semantic scores
- Functions with 100+ lines should get higher cognitive load scores
- Functions with nesting depth 5+ should get higher maintainability concerns
- Compare this function's complexity to what you'd expect from typical enterprise code

Please respond with ONLY the JSON (no other text):
{{
    "semantic_complexity": <number 1-10>,
    "cognitive_load": <number 1-10>,
    "maintainability": <number 1-10>,
    "documentation_quality": <number 1-10>,
    "refactoring_urgency": <number 1-10>,
    "explanation": "<2-3 sentence explanation of the main complexity drivers and why you gave these specific scores>",
    "suggestions": [
        "<specific actionable suggestion 1>",
        "<specific actionable suggestion 2>",
        "<specific actionable suggestion 3>"
    ]
}}

Focus on what makes THIS SPECIFIC function more or less complex than average code."""

        return prompt

    def call_openai_api(self, prompt: str) -> Dict[str, Any]:
        """Make API call to OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code complexity analyzer. Always respond with valid JSON in the exact format requested. Do not include any text before or after the JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens_per_request,
                temperature=0.1,  # Low temperature for consistent analysis
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON from response if it contains extra text
            content = self._extract_json_from_response(content)

            return json.loads(content)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {content}")
            return self._create_fallback_response()

        except Exception as e:
            print(f"API call error: {e}")
            return self._create_fallback_response()

    def _extract_json_from_response(self, content: str) -> str:
        """Extract JSON from response that might contain extra text"""
        # Try to find JSON block in the response
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            return json_match.group(0)

        # If no JSON found, return the content as-is and let it fail gracefully
        return content

    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response if API fails"""
        return {
            "semantic_complexity": 5,
            "cognitive_load": 5,
            "maintainability": 5,
            "documentation_quality": 5,
            "refactoring_urgency": 5,
            "explanation": "API analysis failed - using fallback scores",
            "suggestions": [
                "Review this function manually",
                "Consider refactoring",
                "Add documentation",
            ],
        }

    def calculate_final_score(
        self, llm_metrics: LLMComplexityMetrics, structural_score: float
    ) -> float:
        """Combine LLM analysis with structural metrics for final score"""

        # Weight LLM metrics
        llm_score = (
            llm_metrics.semantic_complexity * 3.0
            + llm_metrics.cognitive_load * 2.5
            + llm_metrics.maintainability * 2.0
            + llm_metrics.documentation_quality * 1.5
            + llm_metrics.refactoring_urgency * 2.0
        ) / 11.0  # Normalize to 1-10 scale

        # Combine with structural score (60% LLM, 40% structural)
        final_score = (llm_score * 0.6) + (min(structural_score / 10, 10) * 0.4)

        return final_score

    def analyze_function(
        self, target_function: Dict[str, Any], all_functions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze a single function with LLM"""

        print(f"Analyzing function: {target_function['function_name']}")

        # Find related functions for context
        related_functions = self.find_related_functions(target_function, all_functions)

        # Build context
        context = self.build_analysis_context(target_function, related_functions)

        # Create prompt
        prompt = self.create_analysis_prompt(context)

        # Call LLM
        llm_response = self.call_openai_api(prompt)

        # Parse response into metrics
        llm_metrics = LLMComplexityMetrics(
            semantic_complexity=llm_response.get("semantic_complexity", 5),
            cognitive_load=llm_response.get("cognitive_load", 5),
            maintainability=llm_response.get("maintainability", 5),
            documentation_quality=llm_response.get("documentation_quality", 5),
            refactoring_urgency=llm_response.get("refactoring_urgency", 5),
            explanation=llm_response.get("explanation", ""),
            suggestions=llm_response.get("suggestions", []),
        )

        # Calculate final score
        final_score = self.calculate_final_score(
            llm_metrics, target_function["total_complexity_score"]
        )
        llm_metrics.final_score = final_score

        # Combine with original data
        enhanced_function = target_function.copy()
        enhanced_function.update(
            {
                "llm_analysis": {
                    "semantic_complexity": llm_metrics.semantic_complexity,
                    "cognitive_load": llm_metrics.cognitive_load,
                    "maintainability": llm_metrics.maintainability,
                    "documentation_quality": llm_metrics.documentation_quality,
                    "refactoring_urgency": llm_metrics.refactoring_urgency,
                    "explanation": llm_metrics.explanation,
                    "suggestions": llm_metrics.suggestions,
                    "final_score": llm_metrics.final_score,
                },
                "combined_complexity_score": final_score,
                "related_functions_analyzed": len(related_functions),
            }
        )

        return enhanced_function

    def analyze_top_functions(
        self, complex_functions_file: str, top_n: int = 20
    ) -> List[Dict[str, Any]]:
        """Analyze top N most complex functions with LLM"""

        # Load Phase 1 results
        with open(complex_functions_file, "r") as f:
            all_functions = json.load(f)

        if len(all_functions) == 0:
            print("No functions found in input file")
            return []

        # Take top N functions
        top_functions = all_functions[:top_n]

        print(f"Starting LLM analysis of top {len(top_functions)} functions...")

        # Analyze each function
        enhanced_results = []
        for i, func in enumerate(top_functions, 1):
            print(f"Progress: {i}/{len(top_functions)}")

            try:
                enhanced_func = self.analyze_function(func, all_functions)
                enhanced_results.append(enhanced_func)
            except Exception as e:
                print(f"Error analyzing {func['function_name']}: {e}")
                # Add original function with error marker
                func["llm_analysis"] = {"error": str(e)}
                enhanced_results.append(func)

        # Re-sort by combined score
        enhanced_results.sort(
            key=lambda x: x.get("combined_complexity_score", 0), reverse=True
        )

        return enhanced_results


def main():
    """Main execution function for Phase 2"""

    # Configuration
    API_KEY = os.getenv("OPENAI_API_KEY")  # Set your API key as environment variable
    if not API_KEY:
        print("Please set OPENAI_API_KEY environment variable")
        return

    MODEL = "gpt-3.5-turbo"  # or "gpt-4" or "gpt-4-turbo"
    INPUT_FILE = "complex_functions.json"  # Output from Phase 1
    OUTPUT_FILE = "llm_analyzed_functions.json"
    TOP_N = 8  # Number of functions to analyze
    # TOP_N = 20

    # Initialize analyzer
    analyzer = LLMComplexityAnalyzer(API_KEY, MODEL)

    # Run analysis
    try:
        results = analyzer.analyze_top_functions(INPUT_FILE, TOP_N)

        # Save results
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2)

        # Print summary
        print(f"\n{'='*80}")
        print(f"LLM ANALYSIS COMPLETE - Top {len(results)} Functions")
        print(f"{'='*80}")

        for i, func in enumerate(results[:10], 1):  # Show top 10
            llm = func.get("llm_analysis", {})
            print(
                f"\n{i}. {func['function_name']} (Combined Score: {func.get('combined_complexity_score', 0):.2f})"
            )
            print(f"   File: {func['file_path']}:{func['start_line']}")
            print(f"   Structural Score: {func['total_complexity_score']:.2f}")
            if "final_score" in llm:
                print(f"   LLM Score: {llm['final_score']:.2f}")
            if "explanation" in llm:
                print(f"   Analysis: {llm['explanation']}")
            if "suggestions" in llm and llm["suggestions"]:
                print(f"   Top Suggestion: {llm['suggestions'][0]}")

        print(f"\nDetailed results saved to: {OUTPUT_FILE}")
        print(f"API calls made: {len(results)}")

    except FileNotFoundError:
        print(f"Input file {INPUT_FILE} not found. Please run Phase 1 first.")
    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    main()
