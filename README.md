# Unbelievable Tony

Unbelievable Tony is a bot that listens to episodes of *Kill Tony* and detects Tony Hinchcliffe's signature phrases: 
- "unbelievable" 
- "oh shit"
- "absolutely incredible"
- "insane"
- "holy shit"
- "holy fucking shit"
- "what the fuck"
- "wow"
- "jesus christ"
- "incredible"
- "that was wild"
- "that was amazing"
- "oh my god"

It counts occurrences and posts a summary as a YouTube comment + a r/KillTony post.

## Features
- Automatically detects instances of Tony's phrases in *Kill Tony* episodes
- Uses WhisperX for speech-to-text and speaker diarization
- Uses a keras model to detect Tony's voice
- Posts a humorous summary as a YouTube comment and a reddit post

## How It Works
1. The bot downloads the audio of an episode of *Kill Tony*.
2. It diarizes the audio using WhisperX.
3. A model detects Tony Hinchcliffe's voice.
4. Based on the output of the model, all speakers attributed as Tony are joined into a single audio file
5. The "Tony" audio file is transcribed
4. The bot counts occurrences of the catch phrases.
5. It generates a fun comment summarizing the count.
6. The comment is posted to YouTube and reddit automatically.

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/unbelievable-tony.git
cd unbelievable-tony

# Install dependencies
python3.12 -m venv .venv
source .venv/bin/activate
poetry env use 3.12
poetry install
```

## Usage
```bash
un_believable count --youtube-link https://www.youtube.com/watch\?v\=z-21SI0mtv4 --hf-token hf_token
```
## Example output
```
{
    "unbelievable": 10,
    "oh shit": 1,
    "absolutely incredible": 3,
    "insane": 0,
    "holy shit": 5,
    "holy fucking shit": 0,
    "what the fuck": 5,
    "wow": 20,
    "jesus christ": 1,
    "incredible": 13,
    "that was wild": 0,
    "that was amazing": 0,
    "oh my god": 6
}
```
## Configuration
Modify `src/un_believable/utils/config.py`

## Future Improvements
- Integrate a database for tracking phrase counts over multiple episodes
- Expand detection to other phrases / people
- Improve Tony's voice model for higher accuracy

## Contributions
Feel free to open issues and submit pull requests!

## License
MIT License

