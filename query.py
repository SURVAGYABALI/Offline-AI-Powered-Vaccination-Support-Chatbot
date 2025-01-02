import requests
import json
def query_ollama_streaming(prompt, model="llama3.2"):
    # Define the API endpoint
    url = f"http://localhost:11434/api/generate"
    
    # Payload with the model and prompt
    payload = {
        "model": model,
        "prompt": prompt
    }
    
    try:
        # Send POST request with streaming enabled
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Process each chunk of data
            print("Model Response:")
            ans = ''
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    # Parse and print the chunk
                    data = chunk.strip()
                    parsed_json = json.loads(data.decode('utf-8'))
                  
                    ans += parsed_json['response']
                    # print(ans)
            return ans
    
    except requests.exceptions.RequestException as e:
        return e
        # print(f"Error: {e}")



