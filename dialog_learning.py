from environs import Env
import json
from google.cloud import dialogflow


def create_intent(project_id, display_name,
                  training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main() -> None:
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')

    with open("phrases_file.json", "r") as file:
        phrases = json.loads(file.read())

    questions_text = phrases["Устройство на работу"]["questions"]
    answer_text = [phrases["Устройство на работу"]["answer"]]
    display_name = "My first API key - first API"

    create_intent(project_id, display_name,
                  questions_text, answer_text)


if __name__ == '__main__':
    main()
