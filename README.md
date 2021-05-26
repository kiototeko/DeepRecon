## [Preprint] Security Analysis of Deep Neural Networks Operating in the Presence of Cache Side-Channel Attacks

This repository includes the code for the paper </br>
[_Security Analysis of Deep Neural Networks Operating in the Presence of Cache Side-Channel Attacks_](https://arxiv.org/abs/1810.03487)

**Authors:** [Sanghyun Hong](http://sanghyun-hong.com), Michael Davinroy, [Yigitcan Kaya](http://www.cs.umd.edu/~yigitcan), Stuart Nevans Locke, Ian Rackow, Kevin Kulda, [Dana Dachman-Soled](https://user.eng.umd.edu/~danadach/), and [Tudor Dumitras](http://users.umiacs.umd.edu/~tdumitra/). </br>
**Contact:** [Sanghyun Hong](mailto:shhong@cs.umd.edu), [Michael Davinroy](mailto:michael.davinroy@gmail.com)


## About

DeepRecon is an exemplary attack that reconstructs the architecture of the victim's DNN by using the internal information extracted via Flush+Reload, a cache side-channel technique. DeepRecon observes function invocations that map directly to architecture attributes of the victim network so that the attacker can reconstruct the victim's entire network architecture from her observations.

---

## Prerequisites


### 1. Runtime Environment

 - Python 2.7
 - TensorFlow 1.10.0
 - Mastik v0.0.2
 - Keras 2.2
 - Pillow
 - libdwarf



#### 2. Compile the Attack Source

Our attack reconstructs the DNN's architecture from the extracted attributes via Flush+Reload. We first build Mastik library that implements side-channel attacks and incorporate the library into the extraction code.

##### 2.1 Build Mastik

      $ ./build_mastik.sh


##### 2.2 Build Attack Code

      $ cd attacks
      $ make

----

#### 3. Find functions being called

The shared library used by Tensorflow is in **/home/USER/miniconda3/envs/tense/lib/python2.7/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so** if you are using conda.

You can find the symbol names of all functions that can be possibly used by tensorflow, by running the following code:
`nm /home/USER/miniconda3/envs/tense/lib/python2.7/site-packages/tensorflow/python/_pywrap_tensorflow_internal.so`

The function names you see as output are the mangled names of C++ functions, if you want to see how they are actually named on the source files, use the -C flag or pipe the output through c++filt

Now to find which functions are being used, first run one of the models found on *models* with gdb, for example:
`gdb python`
and when the prompt appears use `run vgg16.py`

These programs have an input function before the model is actually used for inference, so when the program asks for input, instead stop it by using CTRL+Z and then it's time to use some breakpoints.

You can use rbreak to put a breakpoint in all functions that match the regular expression. For example, we could use `rbreak .*Conv2DOp.*` to find all functions that have that have that string. Then you could just use `continue` and see if there is any interruption in the execution of the code.

Once you know which functions are being called, you can insted put a breakpoint on that function, for example: we know *_ZN10tensorflow11MklConv2DOpIN5Eigen16ThreadPoolDeviceEfLb1EE7ComputeEPNS_15OpKernelContextE* corresponds to the Convolution in 2D, so we just use `break _ZN10tensorflow11MklConv2DOpIN5Eigen16ThreadPoolDeviceEfLb1EE7ComputeEPNS_15OpKernelContextE` to interrupt when this function is called.


## Running DeepRecon

Run the inference with the model using a sample (mug.jpg).
[Note that in the real-attack, we do not need to query the victim model; this can be achieved by a user's query while we are passively monitoring the cache behaviors.]

      $ cd models
      $ python vgg16.py
      Using TensorFlow backend.
      0 iteration, press any key to perform...

      (wait until the extraction is ready.)

After that, run the DeepRecon attack code (specify the location to store the output file).</br>
**[Note: in the flush_reload.c, the thresholds and monitor parameters should be tuned in advance.]**

      $ cd attacks
      $ ./flush_reload .
      ------------ Monitor -------------
       Searching [ 0] for [_ZN10tensorflow12_GL]: : the func. offset [   4f8be5f]
       Searching [ 1] for [_ZN10tensorflow6Bias]: : the func. offset [   7a38bb6]
       Searching [ 2] for [_ZN10tensorflow9Soft]: : the func. offset [   7e99738]
       Searching [ 3] for [_ZN10tensorflow18Una]: : the func. offset [   7e4d57a]
       Searching [ 4] for [_ZN10tensorflow7Unar]: : the func. offset [   96dc50a]
       Searching [ 5] for [_ZN10tensorflow7Unar]: : the func. offset [   957f404]
       Searching [ 6] for [_ZN10tensorflow18Una]: : the func. offset [   7e4d172]
       Searching [ 7] for [_ZN10tensorflow18Una]: : the func. offset [   7ebe46c]
       Searching [ 8] for [_ZN10tensorflow18Una]: : the func. offset [   7eea696]
       Searching [ 9] for [_ZN10tensorflow18Una]: : the func. offset [   7e4b942]
       Searching [10] for [_ZN10tensorflow18Una]: : the func. offset [   7e4bd4a]
       Searching [11] for [_ZN10tensorflow14Lau]: : the func. offset [   9d72242]
       Searching [12] for [_ZN10tensorflow8MatM]: : the func. offset [   7759dfa]
       Searching [13] for [_ZN10tensorflow12Max]: : the func. offset [   97baa4e]
       Searching [14] for [_ZN10tensorflow8Bina]: : the func. offset [   898505e]
       Searching [15] for [_ZN10tensorflow12Avg]: : the func. offset [   975f21a]
       Searching [16] for [_ZN10tensorflow12Con]: : the func. offset [   5519e1a]
       Searching [17] for [_ZN10tensorflow14Lau]: : the func. offset [   9d722c2]
      ------------- Total --------------
       Monitored: [18]
      ----------------------------------
      Do analysis of collected data

The extracted data stored into the *accesses.raw.csv* file.

      ...
      3487174,17,30,hit,End Conv
      3487190,17,28,hit,End Conv
      3487206,17,30,hit,End Conv
      3487218,2,198,hit,Softmax
      ...

----

----

## Cite This Work

You are encouraged to cite our paper if you use **DeepRecon** for academic research.

```
@article{Hong19DeepRecon,
  author    = {Sanghyun Hong and
               Michael Davinroy and
               Yigitcan Kaya and
               Stuart Nevans Locke and
               Ian Rackow and
               Kevin Kulda and
               Dana Dachman{-}Soled and
               Tudor Dumitras},
  title     = {Security Analysis of Deep Neural Networks Operating in the Presence
               of Cache Side-Channel Attacks},
  journal   = {CoRR},
  volume    = {abs/1810.03487},
  year      = {2018},
  url       = {http://arxiv.org/abs/1810.03487},
  archivePrefix = {arXiv},
  eprint    = {1810.03487},
  timestamp = {Tue, 30 Oct 2018 10:49:09 +0100},
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

**Fin.**
