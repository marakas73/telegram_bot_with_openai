# in this case i use gpt3.5 model

import openai


class ChatGPT:
    def __init__(self, openai_api_key: str, org_id: str) -> None:
        # initialize important variables
        openai.api_key = openai_api_key
        openai.organization = org_id
        self.model = "gpt-3.5-turbo"

    # return history (list) with latest message as response from assistant
    def generate_openai_json_answer(self, user_prompt: str, history: list) -> list:
        # check if question_content is empty 
        assert user_prompt, "question_content cannot be empty"
        
        # add current user prompt as last message in history
        user_prompt_message = {"role": "user", "content": user_prompt}
        history.append(user_prompt_message)

        # get an openai answer to a question
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=history,
            temperature=0,
        )

        # get only text of answer
        response_content = response["choices"][0]["message"]["content"]

        # create structured response and add it to the history
        structured_response = {"role": "assistant", "content": response_content}
        history.append(structured_response)

        return history