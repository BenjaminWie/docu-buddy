import json

from supabase import Client, create_client

# Initialize Supabase client
SUPABASE_URL = "https://hmuizdwvqkkqgjsnjxxi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtdWl6ZHd2cWtrcWdqc25qeHhpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODk0MDg5MSwiZXhwIjoyMDY0NTE2ODkxfQ.3TreHNUWelbzbmlbIDrigLfN6x8NR3N6MdYD2toIA9k"  # Keep this secret
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_function_complexity(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten and prepare records
    records = []
    for item in data:
        record = {
            "function_name": item["function_name"],
            "file_url": item["file_url"],
            "github_url": item["github_url"],
            "start_line": item["start_line"],
            "end_line": item["end_line"],
            "language": item["language"],
            "combined_complexity_score": item["combined_complexity_score"],
            # rule_ fields
            "rule_cyclomatic_complexity": item["rule_analysis"][
                "cyclomatic_complexity"
            ],
            "rule_nesting_depth": item["rule_analysis"]["nesting_depth"],
            "rule_function_length": item["rule_analysis"]["function_length"],
            "rule_parameter_count": item["rule_analysis"]["parameter_count"],
            "rule_cognitive_complexity": item["rule_analysis"]["cognitive_complexity"],
            "rule_documentation_score": item["rule_analysis"]["documentation_score"],
            "rule_score": item["rule_analysis"]["rule_score"],
            # llm_ fields
            "llm_semantic_complexity": item["llm_analysis"]["semantic_complexity"],
            "llm_cognitive_load": item["llm_analysis"]["cognitive_load"],
            "llm_maintainability": item["llm_analysis"]["maintainability"],
            "llm_documentation_quality": item["llm_analysis"]["documentation_quality"],
            "llm_refactoring_urgency": item["llm_analysis"]["refactoring_urgency"],
            "llm_explanation": item["llm_analysis"]["explanation"],
            "llm_business_description": item["llm_analysis"]["business_description"],
            "llm_developer_description": item["llm_analysis"]["developer_description"],
            "llm_score": item["llm_analysis"]["llm_score"],
            "llm_suggestions": json.dumps(item["llm_analysis"]["suggestions"]),
        }
        records.append(record)

    # Insert into Supabase
    response = supabase.table("function_complexity").insert(records).execute()
    print("Insert response:", response)


# Example usage
upload_function_complexity("llm_analyzed_functions.json")
