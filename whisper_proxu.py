import whisper_timestamped as whisper
from datetime import timedelta
import random, string
import audio


def generate_name(number : int) :
    return ''.join([string.ascii_letters[random.randint(0, 10)]+str(random.randint(0, 5)) for _ in range(number)])

def transcribe_audio(video_path : str,  language_src : str, language_dest : str, type : str, horo_name : str ):
    audio_name = generate_name(8)
    audio_path = audio.extract_audio(video_path, audio_name, 'wav')
    model = whisper.load_model(type)
    transcribe = whisper.transcribe(model, audio_path, language= language_src)
    segments = transcribe['segments']
    
    texte = ""
    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        texte += segment
    generate = audio.vague(texte)
    res = ""
    for portion in generate :
        trans = audio.translate_with_language(portion, language_dest = language_dest, language_src = language_src)
        res += trans
        
    url = f'Transcribe/{horo_name}.srt'
    with open(url, 'w', encoding='utf-8') as srtFile:
            srtFile.write(audio.epure(res))
    return url

def traduct_srt(srt_path : str, lang_src : str, lang_dest : str) :
    data = open(srt_path, "r").read()
    generate = audio.vague(data)
    res = ""
    for portion in generate :
        trans = audio.translate_with_language(portion, language_dest = lang_dest, language_src = lang_src)
        res += trans
    src_path = srt_path.split('/')[-1].split('.')[0]
    with open(f'Transcribe/{src_path}_{lang_dest}.srt', 'w', encoding='utf-8') as srtFile:
            srtFile.write(audio.epure(res))
    return srt_path

if __name__ == "__main__" :
    #name = audio.extract_audio("/home/chikatsi/Téléchargements/Shawn Mendes, Camila Cabello - Señorita (Lyrics).mp4", generate_name(8), "wav")
    #transcribe_audio(name, "fr", "en", "small", "seniorita")    
    traduct_srt("Transcribe/seniorita.srt", "en", 'fr')