import json
import sys

import pydantic.v1 as pydantic
import pydantic_argparse
import requests


class Arguments(pydantic.BaseModel):
    # Required Args
    url_host: str = pydantic.Field(description="Url host points to the server", aliases=["-u"])
    repeat: int = pydantic.Field(description="Number of iterations", aliases=["-r"])
    input: str = pydantic.Field(description="Path to the input file", aliases=["-i"])
    output: str = pydantic.Field(description="Path to output file", aliases=["-o"])


def main() -> None:
    # Create Parser and Parse Args
    parser = pydantic_argparse.ArgumentParser(
        model=Arguments,
        prog="CacheCli",
        description="Script for testing caching backend",
        version="0.0.1",
        add_help=True,
    )
    args = parser.parse_typed_args()
    input_data = []
    with open(args.input, "rb") as f:
        for line in f:
            input_data.append(line.rstrip())

    with open(args.output, 'w') as sys.stdout:
        for  i in range(args.repeat):
            for line in input_data:
                create_response = requests.post(
                    f"http://{args.url_host}/api/transform_list",
                    data=line.decode("utf8"),
                    headers={"Content-Type": "application/json"},
                )
                if create_response.status_code == 200:
                    answer = requests.get(f"http://{args.url_host}/api/transform_list/{int(create_response.text)}/")
                    print(answer.text)


if __name__ == "__main__":
    main()