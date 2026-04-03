# Path.iterdir()
from typing import Annotated
from pathlib import Path
from collections import Counter
import typer, json
import subprocess

app = typer.Typer()


def get_data(dir_path: Path) -> list[dict]:

    SUBPROCESS_MODULE_NAME = "txt_analyzer"

    result_list = []

    for file_path in dir_path.iterdir():
        
        if not file_path.is_file(): 
            continue
            
        try:             
            process_result = subprocess.run(
                ["uv", "run", "python", "-m", SUBPROCESS_MODULE_NAME],
                input = str(file_path) + '\n',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            result_json_str = process_result.stdout.strip()
            result_stderr = process_result.stderr.strip()

            if result_stderr:
                typer.echo(f'Subprocess Error: {result_stderr}', err=True)

            if result_json_str:
                result = json.loads(result_json_str)
                result_list.append(result)

            
        except subprocess.CalledProcessError as e:
            typer.echo(f'Error: subprocess failed with {str(e)}', err=True)
            raise typer.Exit(1)

        except json.JSONDecodeError as e:
            typer.echo(f'Error: invalid json data from subprocess stdout: {e.msg}', err=True)
            raise typer.Exit(1)
            
    return result_list        

def analyze(data: list[dict]) -> str:
    
    result = {
        'files': 0,
        'words' : 0,
        'chars' : 0,
        'lines' : 0
    }

    most_common_words_counter = Counter()
    most_common_chars_counter = Counter()

    for elem in data:
        result['files'] += 1
        word = elem.get('most_common_word')
        if word:
            most_common_words_counter.update([word]) 
        char = elem.get('most_common_char')
        if char:
            most_common_chars_counter.update(char)
        for param in ['words', 'chars', 'lines']:
            result[param] += elem.get(param)

    result['most_common_word'] = most_common_words_counter.most_common(1)[0][0] if  most_common_words_counter else None
    result['most_common_char'] = most_common_chars_counter.most_common(1)[0][0] if  most_common_chars_counter else None

    return json.dumps(result, indent=3)

    


@app.command()
def dir_analyzer(path_str: Annotated[str, typer.Argument()]):
    
    path = Path(path_str.strip())
    
    if not path.is_dir():
        typer.echo(f'Error: {path} is not a directory', err=True)
        raise typer.Exit(1)
    
    data = get_data(path)
    result = analyze(data)
    typer.echo(result)
    

if __name__ == "__main__":
    app()
    
