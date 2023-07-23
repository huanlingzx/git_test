import openai
import json

import time

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

# Step 1, send model the user query and what functions it has access to
def run_conversation():

    # 开始计时
    start_time = time.time()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]
    
    print(response)
    
    # 结束计时
    end_time = time.time()

    # 计算运行时间
    run_time = end_time - start_time

    print("Step 1运行时间为：%.2f秒" % run_time)

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        
        print(function_name)

        # Step 3, call the function
        # Note: the JSON response from the model may not be valid JSON
        function_response = get_current_weather(
            location=message.get("location"),
            unit=message.get("unit"),
        )
        
        # 结束计时
        end_time2 = time.time()

        # 计算运行时间
        run_time = end_time2 - end_time

        print("Step 2 and Step 3运行时间为：%.2f秒" % run_time)

        # Step 4, send model the info on the function call and function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": "What is the weather like in boston?"},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        
        # 结束计时
        end_time3 = time.time()

        # 计算运行时间
        run_time = end_time3 - end_time2

        print("Step 4运行时间为：%.2f秒" % run_time)
        
        return second_response

import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:33211'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:33211'
openai.api_key = "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"


# 开始计时
start_time = time.time()

print(run_conversation())

# 结束计时
end_time = time.time()

# 计算运行时间
run_time = end_time - start_time

print("run_conversation运行时间为：%.2f秒" % run_time)