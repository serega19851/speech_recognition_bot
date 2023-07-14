from environs import Env
import json
from google.cloud import dialogflow
import argparse
from pathlib import Path
import os


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


def gets_args():
    parser = argparse.ArgumentParser("accepts optional args")
    parser.add_argument(
        "-jp", "--json_path",
        help="in enter your path to the file",
        default=os.path.join(Path.cwd(), "phrases_file.json")

    )
    args = parser.parse_args()
    return args


def main() -> None:
    env = Env()
    env.read_env()
    project_id = env.str("PROJECT_ID")

    path_json = gets_args().json_path
    with open(path_json, "r") as file:
        text = json.loads(file.read())

    for topic, phrases in text.items():
        create_intent(project_id, topic,
                      phrases["questions"], [phrases["answer"]])


if __name__ == "__main__":
    main()
