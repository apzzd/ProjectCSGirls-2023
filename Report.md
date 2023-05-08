
## Title Page

### Noise Recorder using the Pi Zero (`NRP0`)

Ada Pezzuti Dyer
Homeschool in Albuquerque, New Mexico
[Video Link]()


## Introduction

Brief intro to your tech
How does it address your problem 
Whats the problem



## Technology Summary
---

To create the NRP0, I repurposed the AIY Voice Box, a do-it-yourself virtual assistant that uses AI created by Google. This device is mainly comprised of a Pi Zero, an AIY Voice Bonnet, a speaker, a microphone, and a color-changing button. 



When the NRP0 records sounds, the button turns yellow, and the device checks the noise level - measured in RMS - every 0.3 seconds. If the RMS exceeds 0.5, then the device makes a 5-second recording that hopefully captures the source of the noise.

[Write about the ML Model]

The code for the NRP0 was written in Python inside a Jupyter Notebook, [talk abt code used for MLM]

#### I. Setting up the Voice Box

The first thing I had to do was a bit of assembly. Following the instructions on the [AIY Voice Kit website], I constructed the Voice Box.

Then, to be able to add programs to it, I made a `wpa_supplicant` file with my local network's name and credentials, uploaded it onto the Voice Box's chip, and plugged it in. This step allowed me to access all the code on my Voice Box through a local website it was hosting, named `http://orcspi-voice.local` with a port number of `5555`. 

Now that I was able to code it, I was ready to turn my Voice Box into the NRP0.

#### II. Recording sound clips

[this part hasn't been done yet ->] As soon the NRP0 is turned on, it starts measuring the sound level of its environment. The variables `recdur` (the duration of the recording) and `threshold` (the RMS threshold for recoring sounds) are set. An "audio stream" is started - this is a period of time in which the NRP0 listens to its environment - and the button turns yellow to indicate this.

```
recdur = 5
threshold = 0.5

stream.start_stream()

buttonLight.update(buttonLight.rgb_on((255, 100, 0)))
```

When a loud noise is detected, the button is turned red. The audio stream, which was used to determine the sound level, is closed. An angry print statement is put in the console (for debugging purposes). A timestamped ".wav" file with a duration of `recdur` is recorded and saved.

```
		if (rms > threshold):
            # red light
            buttonLight.update(buttonLight.rgb_on((255, 0, 0)))
            
            # stop stream
            stream.stop_stream()
            stream.close()
            
            # angrily record loud people 
            print("You're being too loud 😡 I will record you!")
            
            date = time.strftime("%Y%m%d-%H%M%S")
            fn = "loud-" + date + ".wav"
            record_file(AudioFormat.CD, filename=fn, filetype='wav',
                wait=lambda: time.sleep(recdur))
```

After it's finished, the button turns yellow again and a new audio stream is opened. 

```
			buttonLight.update(buttonLight.rgb_on((255, 100, 0)))
            
            # start stream
            stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)
```

This cycle is repeated every 0.3 seconds.

```
		# refresh every 0.3 seconds 
        time.sleep(0.3)
```


The main purpose of turning the button red when it is recording was to make the manual identification of sound clips using the `NRP0` easy. When the button turned red, I could write down what I thought the source of the noise was and the time, so I could then use it to train the machine learning model. 

*See the full code in the [Appendix](##Appendix), or look at it on [Github](https://github.com/apzzd/ProjectCSGirls-2023/blob/main/NoiseMeterDemo.ipynb).*

#### III. Identify the sounds Pt. 1

Then next part of my project was to identify the sounds my device recorded. To do this, I made a machine learning model using CreateML using the labeled sound clips I collected to train it.

To create the training data, I recorded MP3 files duing the morning, afternoon, and night. While I was doing this, I wrote down the sources of all the notable sounds I heard during the 5 minutes and the time that they occurred.

Then, I used a Python program I wrote to slice the audio recordings into 4-second chunks, and identified each chunk using what I wrote down while I was recording. Now, full disclosure, this code isn't written in the best possible way, and I realize I could have made it more efficient, but I just wanted to write something quickly that would get the job done.

I begin by importing `pydub`. This Python library is really useful for manipulating sound files.

```
from pydub import AudioSegment
from pydub.utils import make_chunks
```

Then, I create a function called `sliceWav` which takes in the parameters `segLength` and `fileName`. The first thing this function does is retreive an audio file with type `wav` and the name that we pass in and assign it to the variable `myaudio`.

```
myaudio = AudioSegment.from_file(fileName + ".wav", "wav")
```

After that, I convert the chunk length that we pass in to milliseconds.

```
chunk_length_ms = segLength * 1000
```

I then make an array called `chunks` (using the infinitely useful function from the `pydub` library) that is composed of the `wav` file that we retreived sliced into chunks of the desired length.

```
chunks = make_chunks(myaudio, chunk_length_ms)
```

Finally, I loop through the array `chunks` setting the variable `chunk_name` to include the original file name along with the time segment it includes, and describe the folder I want to put it in...

```
chunk_name = "slicedAudio/" + fileName + "_{0}-{1}.wav".format(i * segLength, (i + 1) * segLength)
```

... print out the file name for clarity...

```
print("exporting", chunk_name)
```

... and save the file on my computer.

```
chunk.export(chunk_name, format="wav")
```

Now, I call the function on each of my audio files to create the training data I will use later.

```
for fname in ["Morning1", "Morning2", "Afternoon2", "Night1", "Night2"]:
	sliceWav(4, fname)
```

*See the full code in the [Appendix](##Appendix), or look at it on [Github](https://github.com/apzzd/ProjectCSGirls-2023/blob/main/NoiseMeterDemo.ipynb).*

#### IV. Identify the sounds Pt. 2

Now that I had training data, I made a machine learning model using the Mac application CreateML using the labeled sound clips I collected to train it.

First, I create a new CreateML file with a model type of "Sound Classification".

![[MLMODEL1.png]]
Next, I import my training data that I had previously classified and train my model with it.

![[MLMODEL2.png]]

![[MLMODEL3.png]]
When it finishes processing the files, I can test my model by going to the "Preview" tab and either uploading files for it to classify or starting a live audio screen, depicted in the screenshot below.
![[MLMODEL4.png]]

#### V. Putting it all together

Now with my `NRP0` and MLModel finished, I had a way to collect and analyze data.


#### VI. Making it self-contained [TENTATIVE]

[Removing dependency on wifi]

## Results

How well does tech work
Go ahead and admit failures
Show the data + analyze it
Graphs + results

#### Analyzing the Data

#### Using the Data

#### Informing Authority

#### Improvement

My prototype is definitely not perfect, and so here are some ideas for improvement.





## Appendix

### Links

https://en.wikipedia.org/wiki/Audio_power#Continuous_power_and_%22RMS_power%22

https://stackoverflow.com/questions/36799902/how-to-splice-an-audio-file-wav-format-into-1-sec-splices-in-python

https://github.com/apzzd/ProjectCSGirls-2023/blob/main/NoiseMeterDemo.ipynb
https://github.com/apzzd/ProjectCSGirls-2023/blob/main/soundSplitter/main.py

### Source Code

#### Sound Splitter
```
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
```

#### Sound Recorder

```
import pyaudio  
import time  
from math import log10 import audioop

from IPython.display import clear_output  
from aiy.voice.audio import AudioFormat, play_wav, record_file

import glob  
from aiy.pins import BUTTON_GPIO_PIN from gpiozero import Button  
from aiy.leds import Leds, Color

buttonLight = Leds()

###

p = pyaudio.PyAudio()

WIDTH = 2  
RATE = int(p.get_default_input_device_info()['defaultSampleRate' DEVICE = p.get_default_input_device_info()['index']  
rms = 1

###

def callback(in_data, frame_count, time_info, status): global rms

rms = audioop.rms(in_data, WIDTH) / 32767 return in_data, pyaudio.paContinue

stream = p.open(format=p.get_format_from_width(WIDTH), input_device_index=DEVICE,

channels=1,  
rate=RATE,  
input=True,  
output=False, stream_callback=callback)

###

import time recdur = 5

threshold = 0.5

stream.start_stream()

buttonLight.update(buttonLight.rgb_on((255, 100, 0)))

try:  
	while stream.is_active():
	        # print out the RMS and DB values
			db = 20 * log10(rms)  
			print(f"RMS: {rms:.4f} DB: {db:.1f}") clear_output(wait=True)
	
			if (rms > threshold): 
				# red light
				buttonLight.update(buttonLight.rgb_on((255, 0, 0)))
	
				# stop stream
				stream.stop_stream() stream.close()
	
	            # angrily record loud people
				print("You're being too loud 😡 I will record you!") 
				
				date = time.strftime("%Y%m%d-%H%M%S")
				fn = "loud-" + date + ".wav" record_file(AudioFormat.CD, filename=fn, filetype='wav', wait=lambda: time.sleep(recdur)) 
				buttonLight.update(buttonLight.rgb_on((255, 100, 0))
	
				# start stream
				stream = p.open(format=p.get_format_from_width(WIDTH), input_device_index=DEVICE, channels=1, rate=RATE, input=True,  
	output=False, stream_callback=callback)

	# refresh every 0.3 seconds
	time.sleep(0.3)

except KeyboardInterrupt:
    print('Done')

stream.stop_stream() 
stream.close()

```

#### Today's Loud Sounds

*Note: This code was not featured in the report because it was not essential to the project. It is pretty cool though, so I decided to include it here. :)*

```
today = time.strftime("%Y%m%d") 

global printedSnds
printedSnds = False

def playSounds(): 
	print("Pressed")
	global printedSnds  

	files = glob.glob("loud-" + today + "*.wav") 
	
	for file in files:
		if (not printedSnds): 
			print("Printin' it") 
			print(file)
		else:  
			print("Playin' it") 
			play_wav(file) 
			sleep(2)

	printedSnds = True

with Leds() as buttonLight, Button(BUTTON_GPIO_PIN) as button: 
	if (printedSnds):
		buttonLight.update(buttonLight.rgb_on((0, 0, 255))) 
	else:
		buttonLight.update(buttonLight.rgb_on((255, 0, 255)))
		while True: 
			button.when_pressed=playSounds
```

#### Close and Terminate Stream

```
stream.close()
p.terminate()
```

Sources
Source Code
Big diagrams
Footnotes from earlier in the essay

