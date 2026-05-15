import json

def mock_llm_tool_caller(prompt: str) -> list:
    """
    Simulates an LLM's ability to plan and suggest tool calls based on a prompt.
    In a real scenario, this would involve an actual LLM API call and parsing its response
    for tool function calls (e.g., OpenAI function calling, LangChain agents).
    """
    print(f"Agent's thought process (simulated LLM call for prompt):\n'{prompt}'")
    print("  (This simulates the LLM deciding which tools to use and with what arguments)")

    if "weather in London" in prompt.lower() and "notify" in prompt.lower():
        # Simulate a multi-step plan: get weather, then notify using that weather.
        print("  Simulated LLM suggests a multi-step plan: get weather, then notify.")
        return [
            {"tool": "get_weather", "args": {"location": "London"}},
            {"tool": "send_notification", "args": {"message_template": "Weather update for London: {weather_info}"}}
        ]
    elif "weather in Paris" in prompt.lower():
        print("  Simulated LLM suggests getting weather for Paris.")
        return [
            {"tool": "get_weather", "args": {"location": "Paris"}}
        ]
    elif "send a reminder" in prompt.lower():
        print("  Simulated LLM suggests sending a notification.")
        return [
            {"tool": "send_notification", "args": {"message": "Reminder: Meeting at 3 PM!"}}
        ]
    else:
        print("  Simulated LLM cannot find a suitable tool for this request.")
        return []

def get_weather(location: str) -> str:
    """
    Simulates a tool that fetches weather information.
    """
    print(f"  Tool: Calling get_weather for {location}...")
    if location.lower() == "london":
        return "Sunny, 22°C"
    elif location.lower() == "paris":
        return "Cloudy, 18°C"
    else:
        return "Unknown weather"

def send_notification(message: str) -> None:
    """
    Simulates a tool that sends a notification.
    """
    print(f"  Tool: Sending notification: '{message}'")
    print(f"  [NOTIFICATION SENT: {message}]")

class AutonomousAgent:
    def __init__(self, llm_tool_caller_func):
        self.llm_tool_caller = llm_tool_caller_func
        self.tools = {
            "get_weather": get_weather,
            "send_notification": send_notification,
        }
        self.context = {} # To store results from previous tool calls

    def run_task(self, task_description: str):
        print(f"\n--- Agent received task: '{task_description}' ---")
        self.context = {} # Reset context for new task

        # Step 1: Agent uses LLM to plan actions (Tool Calling)
        # This is where the agent "thinks" about what to do, based on the task and current context.
        suggested_actions = self.llm_tool_caller(task_description)

        if not suggested_actions:
            print("Agent could not plan any actions for this task.")
            return

        # Step 2: Agent executes the planned actions
        # This is where the agent "acts" based on its plan.
        print("\nAgent executing planned actions:")
        for i, action in enumerate(suggested_actions):
            tool_name = action.get("tool")
            tool_args = action.get("args", {})
            print(f"  Step {i+1}: Agent is using tool '{tool_name}' with args: {tool_args}")

            if tool_name in self.tools:
                tool_function = self.tools[tool_name]
                
                if tool_name == "get_weather":
                    result = tool_function(tool_args.get("location"))
                    self.context["weather_info"] = result # Store result in context for subsequent steps
                    print(f"  Tool '{tool_name}' returned: {result}")
                elif tool_name == "send_notification":
                    message = tool_args.get("message")
                    if "message_template" in tool_args:
                        # Fill template with context info, e.g., weather_info from a previous step
                        message = tool_args["message_template"].format(weather_info=self.context.get("weather_info", "N/A"))
                    tool_function(message)
                else:
                    # Generic tool call for other tools if they existed
                    tool_function(**tool_args) 
            else:
                print(f"  Error: Unknown tool '{tool_name}'")
        print("\nAgent finished task.")

# --- Main execution ---
if __name__ == "__main__":
    print("--- Demonstrating an Autonomous AI Agent ---")
    print("This example showcases an autonomous agent that can interpret a high-level goal,")
    print("plan a sequence of actions using a simulated LLM, and then execute predefined 'tools'")
    print("to achieve the task, including multi-step operations and passing context between tools.")
    print("This goes beyond simple chatbots by enabling 'thinking' (planning) and 'acting' (tool use).\n")

    agent = AutonomousAgent(mock_llm_tool_caller)

    # Example 1: Multi-step task (get weather, then notify)
    agent.run_task("Find out today's weather in London and then notify me.")

    # Example 2: Single-step task (get weather)
    agent.run_task("What's the weather like in Paris?")

    # Example 3: Single-step task (send notification)
    agent.run_task("Send a reminder for the meeting at 3 PM.")

    # Example 4: Task without a defined tool (simulating LLM not finding a plan)
    agent.run_task("Write a poem about cats.")
