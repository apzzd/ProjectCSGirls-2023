

## Title Page

### [device]
Ada Pezzuti Dyer
Homeschool in Albuquerque, New Mexico
[Video Link]()


## Introduction

Brief intro to your tech
How does it adress your problem 
Whats the problem



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

To create the [device], I repurposed the AIY Voice Box, a do-it-yourself virtual assistant that uses AI created by Google[^1]. This device is mainly comprised of a Pi Zero, an AIY Voice Bonnet, a speaker, a microphone, and a color-changing button. 

When the [device] records sounds, the button turns yellow, and the device checks the noise level - measured in RMS - every 0.3 seconds. If the RMS exceeds [threshold], then the device makes a 5-second recording that hopefully captures the source of the noise.

[Write about the ML Model]

The code for the [device] was written in Python inside a Jupyter Notebook, [talk abt code used for MLM]

#### I. Recording sound clips

[this part hasn't been done yet ->] As soon the [device] is turned on, it starts measuring the sound level of its environment. The variables `recdur` (the duration of the recording) and `threshold` (the RMS threshold for recoring sounds) are set. An "audio stream" is started - this is a period of time in which the [device] listens to its environment - and the button turns yellow to indicate this.

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

*See the full code in the [Appendix](##Appendix), or look at it on [Github](github lnk).*

#### II. Identifying sources of noise

[Write about the ML Model, Teachable Machine]

#### III. Putting it all together

[Uploading ML Model onto the device, using it]

#### IV. Making it self-contained

[Removing dependency on wifi]

## Results

How well does tech work
Go ahead and admit failures
Show the data + analyze it
Graphs + results




## Appendix

Sources
Source Code
Big diagrams
Footnotes from earlier in the essay

..

