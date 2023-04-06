from pydub import AudioSegment
from pydub.utils import make_chunks

print(AudioSegment)

myaudio = AudioSegment.from_file("myAudio.wav", "wav")
chunk_length_ms = 4000
chunks = make_chunks(myaudio, chunk_length_ms)

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

# TODO:
#  - put all spliced files in a directory to get rid of the mess
#  - loop through the training data
