from pydub import AudioSegment
from pydub.utils import make_chunks


def sliceWav(segLength, fileName):
	myaudio = AudioSegment.from_file(fileName + ".wav", "wav")
	chunk_length_ms = segLength * 1000
	chunks = make_chunks(myaudio, chunk_length_ms)

	for i, chunk in enumerate(chunks):
    		chunk_name = "slicedAudio/" + fileName + "_{0}-{1}.wav".format(i * segLength, (i + 1) * segLength)
    		print("exporting", chunk_name)
    		chunk.export(chunk_name, format="wav")


for fname in ["Morning1", "Morning2", "Afternoon2", "Night1", "Night2"]:
	sliceWav(4, fname)
