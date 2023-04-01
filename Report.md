
## Title Page

### Noise Recorder using the Pi Zero (`NRP0`)

Ada Pezzuti Dyer
Homeschool in Albuquerque, New Mexico
[Video Link]()


## Introduction

Brief intro to your tech
How does it address your problem 
Whats the problem`



## Technology Summary

Labelled diagrams + photos
Explain code
Reiterate purpose of project

1. Explain entire system vaguely
2. Introduce AIY Voice Kit
3. Introduce Jupyter Notebooks
4. Explain Code
5. Explain how to acess .wav files

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


The main purpose of turning the button red when it is recording was to make the manual identification of sound clips easy. [did not happen yet ->] When the button turned red, I could write down what I thought the source of the noise was and the time, so I could then use it to train the machine learning model. 

*See the full code in the [Appendix](##Appendix), or look at it on [Github](https://github.com/apzzd/ProjectCSGirls-2023/blob/main/NoiseMeterDemo.ipynb).*

#### III. Identify the sounds Pt. 1

[EXPLAIN HOW YOU MADE THE DATA WITH THE AWESOME CODE AND EVERYTHING]

Then next part of my project was to identify the sounds my device recorded. To do this, I made a machine learning model using CreateML using the labeled sound clips I collected to train it.

To create the training data, I recorded MP3 files duing the morning, afternoon, and night. While I was doing this, I wrote down the sources of all the notable sounds I heard during the 5 minutes and the time that they occurred.

[do this]

Later, I used a Python program I wrote to slice the audio recordings into 4-second chunks, and identified each chunk using what I wrote down while I was recording.

[explain code]

#### IV. Identify the sounds Pt. 2

Now that I had training data, I made a machine learning model using the Mac application CreateML using the labeled sound clips I collected to train it.



[DESCRIBE THIS STEP]

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

https://en.wikipedia.org/wiki/Audio_power#Continuous_power_and_%22RMS_power%22

https://stackoverflow.com/questions/36799902/how-to-splice-an-audio-file-wav-format-into-1-sec-splices-in-python

https://github.com/apzzd/ProjectCSGirls-2023/blob/main/NoiseMeterDemo.ipynb

```

```

Sources
Source Code
Big diagrams
Footnotes from earlier in the essay

