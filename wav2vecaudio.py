# -*- coding: utf-8 -*-
"""wav2vecaudio.ipynb

Automatically generated by Colaboratory.

Original file is run in Google Colab: available upon request. 
"""

# pip install datasets transformers
!pip install https://github.com/kpu/kenlm/archive/master.zip
!pip install pyctcdecode
!pip install datasets
!pip install transformers

import os
import numpy as np
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
# y, s = librosa.load(r"/content/drive/My Drive/thesistest/fn001001.wav", sr=16000)
y, s = librosa.load(r"fn001169.wav", sr=16000)
y2,s2 = librosa.load(r"fn001410.wav", sr=16000)

y3,s3 = librosa.load(r"fn001030.wav", sr=16000)
y4,s4 = librosa.load(r"fn001078.wav", sr=16000)
y5,s5 = librosa.load(r"fn001101.wav", sr=16000)
y6,s6 = librosa.load(r"fn001080.wav", sr=16000)
y7,s7 = librosa.load(r"fn001093.wav", sr=16000)
y8,s8 = librosa.load(r"fn001076.wav", sr=16000)
y9,s9 = librosa.load(r"fn001113.wav", sr=16000)
y10,s10 = librosa.load(r"fn001160.wav", sr=16000)

audio = np.array(y)
audio = np.append(audio, y2)

audio = np.append(audio, y3)
audio = np.append(audio, y4)
audio = np.append(audio, y5)
audio = np.append(audio, y6)
audio = np.append(audio, y7)
audio = np.append(audio, y8)
audio = np.append(audio, y9)
audio = np.append(audio, y10)

print(len(audio))

# torch.cuda.is_available()/



t1 = 0
t2 = 0
import torch

MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-dutch"
# MODEL_ID = "/vol/tensusers/lboves/huggingface_finetuned_with-mask/checkpoint-300"

processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)  #cpu
# model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID).to("cuda") #gpu
while(((t2+10)*s) < len(audio)):
# while(t2 < 100):
  print("start loop at: ", t1, " seconds")
  t1 = t2
  windowlength = 10
  t2 = t1 + windowlength



  inputs = processor(audio[t1*s:t2*s],sampling_rate = s, return_tensors="pt",output_hidden_states=True)
  # inputs = inputs.to("cuda")


  with torch.no_grad():
    hidden_states = model(**inputs,output_hidden_states=True).hidden_states
    logits = model(**inputs).logits

  processor.tokenizer.get_vocab()
  # print(hidden_states[0].shape)
  # print(hidden_states[0][0][0])
  hidden_layer_24 = hidden_states[0][0][0]

  predicted_ids = torch.argmax(logits, dim=-1)
  transcription = processor.batch_decode(predicted_ids) # aaaaaapppppppp   mmmmmeeeeennnnsss

  transcription[0].lower()

  # print(transcription[0].lower())
  # logits = logits.cpu()
  # hidden_states = hidden_states.cpu()
  if t1 == 0:
    full_logits = np.array(logits)
  else:
    full_logits = np.concatenate((full_logits, logits),axis=1)

  if t1 == 0:
    hiddenstates0 = np.array(hidden_states[0])
    hiddenstates6 = np.array(hidden_states[6])
    hiddenstates12 = np.array(hidden_states[12])
    hiddenstates18 = np.array(hidden_states[18])
    hiddenstates24 = np.array(hidden_states[24])

  else:
    hiddenstates0 = np.concatenate((hiddenstates0, np.array(hidden_states[0])), axis=1)
    hiddenstates6 = np.concatenate((hiddenstates6, np.array(hidden_states[6])), axis=1)
    hiddenstates12 = np.concatenate((hiddenstates12, np.array(hidden_states[12])), axis=1)
    hiddenstates18 = np.concatenate((hiddenstates18, np.array(hidden_states[18])), axis=1)
    hiddenstates24 = np.concatenate((hiddenstates24, np.array(hidden_states[24])), axis=1)

" ".join(sorted(processor.tokenizer.get_vocab()))

import matplotlib.pyplot as plt
logits_bool = False
print(full_logits[0].shape)
print(hiddenstates0.shape)
for i in range(0,len(full_logits[0])):
  # print(full_logits[0][i])

  # plt.bar(np.arange(0,39), full_logits[0][i])
  # plt.show()
  # plt.bar(np.arange(7,33), logits_example2[7:33],tick_label = list(string.ascii_lowercase))
  if (any(full_logits[0][i][1:39] > 5)):
    # print("index frame: ", i)
    if(not(logits_bool)):
      logits_spikes = np.array(full_logits[0][i], ndmin=2)
      logits_bool = True
      hidden_spikes0 = np.array(hiddenstates0[0][i],ndmin=2)
      hidden_spikes6 = np.array(hiddenstates6[0][i],ndmin=2)
      hidden_spikes12 = np.array(hiddenstates12[0][i],ndmin=2)
      hidden_spikes18 = np.array(hiddenstates18[0][i],ndmin=2)
      hidden_spikes24 = np.array(hiddenstates24[0][i],ndmin=2)

    else:
      logits_spikes = np.concatenate((logits_spikes, np.array(full_logits[0][i],ndmin=2)))
      hidden_spikes0 = np.concatenate((hidden_spikes0, np.array(hiddenstates0[0][i],ndmin=2)))
      hidden_spikes6 = np.concatenate((hidden_spikes6, np.array(hiddenstates6[0][i],ndmin=2)))
      hidden_spikes12 = np.concatenate((hidden_spikes12, np.array(hiddenstates12[0][i],ndmin=2)))
      hidden_spikes18 = np.concatenate((hidden_spikes18, np.array(hiddenstates18[0][i],ndmin=2)))
      hidden_spikes24 = np.concatenate((hidden_spikes24, np.array(hiddenstates24[0][i],ndmin=2)))
# print(logits_spikes)
print(logits_spikes.shape)
print(hidden_spikes0.shape)
print(hidden_spikes0)
# print(logits_spikes)
# # print(full_logits[0][i].shape)
# for i in range(0,len(logits_spikes)):
#   plt.bar(np.arange(0,39), logits_spikes[i])
#   plt.show()

# define network architecture
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import Dense

# MLP0 = Sequential()
# MLP0.add(InputLayer(input_shape=(1024, ))) # input layer

# MLP0.add(Dense(256, activation='relu')) # hidden layer 3
# MLP0.add(Dense(128, activation='relu')) # hidden layer 4
# # MLP.add(Dense(2, activation='softmax')) # output layer binary
# MLP0.add(Dense(38, activation='softmax')) # output layer non-binary

# # summary
# MLP0.summary()

# # optimization
# MLP0.compile(loss='categorical_crossentropy',
#             optimizer='adam',
#             metrics=['accuracy'])

# MLP6 = Sequential()
# MLP6.add(InputLayer(input_shape=(1024, ))) # input layer

# MLP6.add(Dense(256, activation='relu')) # hidden layer 3
# MLP6.add(Dense(128, activation='relu')) # hidden layer 4
# # MLP.add(Dense(2, activation='softmax')) # output layer binary
# MLP6.add(Dense(38, activation='softmax')) # output layer non-binary

# # summary
# MLP6.summary()

# # optimization
# MLP6.compile(loss='categorical_crossentropy',
#             optimizer='adam',
#             metrics=['accuracy'])

# MLP12 = Sequential()
# MLP12.add(InputLayer(input_shape=(1024, ))) # input layer

# MLP12.add(Dense(256, activation='relu')) # hidden layer 3
# MLP12.add(Dense(128, activation='relu')) # hidden layer 4
# # MLP.add(Dense(2, activation='softmax')) # output layer binary
# MLP12.add(Dense(38, activation='softmax')) # output layer non-binary

# # summary
# MLP12.summary()

# # optimization
# MLP12.compile(loss='categorical_crossentropy',
#             optimizer='adam',
#             metrics=['accuracy'])

# MLP18 = Sequential()
# MLP18.add(InputLayer(input_shape=(1024, ))) # input layer

# MLP18.add(Dense(256, activation='relu')) # hidden layer 3
# MLP18.add(Dense(128, activation='relu')) # hidden layer 4
# # MLP.add(Dense(2, activation='softmax')) # output layer binary
# MLP18.add(Dense(38, activation='softmax')) # output layer non-binary

# # summary
# MLP18.summary()

# # optimization
# MLP18.compile(loss='categorical_crossentropy',
#             optimizer='adam',
#             metrics=['accuracy'])

MLP24 = Sequential()
MLP24.add(InputLayer(input_shape=(1024, ))) # input layer

MLP24.add(Dense(256, activation='relu')) # hidden layer 3
MLP24.add(Dense(128, activation='relu')) # hidden layer 4
# MLP.add(Dense(2, activation='softmax')) # output layer binary
MLP24.add(Dense(38, activation='softmax')) # output layer non-binary

# summary
MLP24.summary()

# optimization
MLP24.compile(loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])

split_val = int(0.75 * len(logits_spikes))
print(split_val)

# hidden_spikes12 = hidden_spikes12_random

hiddenstates18_train = hidden_spikes18[0:split_val]
hiddenstates18_test = hidden_spikes18[split_val:len(hidden_spikes18)]

hiddenstates0_train = hidden_spikes0[0:split_val]
hiddenstates0_test = hidden_spikes0[split_val:len(hidden_spikes0)]

hiddenstates12_train = hidden_spikes12[0:split_val]
hiddenstates12_test = hidden_spikes12[split_val:len(hidden_spikes12)]

hiddenstates6_train = hidden_spikes6[0:split_val]
hiddenstates6_test = hidden_spikes6[split_val:len(hidden_spikes6)]

hiddenstates24_train = hidden_spikes24[0:split_val]
hiddenstates24_test = hidden_spikes24[split_val:len(hidden_spikes24)]
# for i in range(0,split_val):
#   train_audio.append(hidden_states[24][0][i].tolist())
# # print(train_audio)
# for i in range(split_val,len(logits[0])):
#   test_audio.append(hidden_states[24][0][i].tolist())
# # print(test_audio)
print(hiddenstates12_train.shape)
print(hiddenstates12_test.shape)
print(hidden_spikes12.shape)

# hidden_spikes0_copy = hidden_spikes0
# logits_spikes_copy = logits_spikes
# import random
# temp = list(zip(hidden_spikes0_copy, logits_spikes_copy))
# random.shuffle(temp)
# hidden_spikes0_shuffled, logits_spikes_shuffled = zip(*temp)

# hiddenstates0_train = hidden_spikes0_shuffled[0:split_val]
# hiddenstates0_test = hidden_spikes0_shuffled[split_val:len(hidden_spikes0_shuffled)]

train_audio_labels_24 = [] #(0.75*len(logits_spikes),1)
test_audio_labels_24 = [] #(0.25*len(logits_spikes),1)

for i in range(0,split_val):
  # if(int((np.argmax(logits_spikes[i][1:39])+1)==11)):
  #   train_audio_labels.append((1,0))
  # else:
  #   train_audio_labels.append((0,1))

  # train_audio_labels.append(int(np.argmax(logits_spikes[i][1:39])))
  zerolist = np.zeros(38, dtype=float)
  zerolist[(np.argmax(logits_spikes[i][1:39])+1)] = 1
  zerotuple = tuple(zerolist)
  train_audio_labels_24.append(zerotuple)






for i in range(split_val,len(logits_spikes)):
  # if(int((np.argmax(logits_spikes[i][1:39])+1)==11)):
  #   test_audio_labels.append((1,0))
  # else:
  #   test_audio_labels.append((0,1))
  # test_audio_labels.append(int(np.argmax(logits_spikes[i][1:39])))
  zerolist = np.zeros(38, dtype=float)
  zerolist[(np.argmax(logits_spikes[i][1:39])+1)] = 1
  zerotuple = tuple(zerolist)
  test_audio_labels_24.append(zerotuple)

print(train_audio_labels_0[0])
print(len(train_audio_labels_0))
print(len(hiddenstates0_train))
print(hiddenstates0_train[0:100])
print(len(hiddenstates0_train[0]))

# train (fit)
MLP24.fit(hiddenstates24_train.tolist(), train_audio_labels_24,
        epochs=20, batch_size=128)

# evaluate performance
test_loss, test_acc = MLP24.evaluate(hiddenstates24_test.tolist(), test_audio_labels_24,
                                   batch_size=128,
                                   verbose=0)
print("Test loss:", test_loss)
print("Test accuracy:", test_acc)

MLP0_backup = MLP0
MLP6_backup = MLP6
MLP12_backup = MLP12
MLP18_backup = MLP18
MLP24_backup = MLP24

# MLP.weights
MLP0.summary()

pred_array_0 = MLP0.predict(hidden_spikes0.tolist())
pred_array_6 = MLP6.predict(hidden_spikes6.tolist())
pred_array_12 = MLP12.predict(hidden_spikes12.tolist())
pred_array_18 = MLP18.predict(hidden_spikes18.tolist()) #dit is fout! moet MLP van specifiek laag 18 zijn natuurlijk.
pred_array_24 = MLP24.predict(hidden_spikes24.tolist())

print(pred_array_18[0])
print(len(pred_array_18))

exp1_preds = []
exp1_preds = np.array(hiddenstates12[0][2099], ndmin=2)
for i in range(2100,2120):
  # print((hiddenstates12[0][i]))
  exp1_preds = np.concatenate((exp1_preds, np.array(hiddenstates12[0][i],ndmin=2)))
# exp1_preds = MLP.predict

exp1_preds_result = MLP.predict(exp1_preds.tolist())
# print(exp1_preds_result)

import matplotlib.pyplot as plt
print(exp1_preds_result[4])
print(exp1_preds_result[:,4])
for i in range(0,10):
  plt.plot(range(0,21),exp1_preds_result[:,i])

  plt.xticks(np.arange(0,21,step=1))
  plt.yscale("log")
  plt.show()
for i in range(0,10):
  plt.plot(range(0,21),exp1_preds_result[:,i])

  plt.xticks(np.arange(0,21,step=1))
  # plt.yscale("log")
  plt.show()

" ".join(sorted(processor.tokenizer.get_vocab()))


print(len(pred_array_12))
print(len(pred_array_12[0]))


pred_array_18_full = MLP.predict(hiddenstates18[0].tolist())

# print(len(pred_array_0_full))
# print(len(pred_array_0_full[0]))
# print(pred_array_0_full)



argmax_array = []
argmax_array_2ndplace = []
# print(np.argsort(pred_array_12_full[5][7:]))
# print(pred_array_12_full[5][7:])
for i in range(0,len(pred_array_12)):
  # sorted_array = np.argsort(pred_array_12_full[i])
  # argmax_array.append(sorted_array[37])
  # argmax_array_2ndplace.append(sorted_array[36])
  # sorted_array = np.argsort(pred_array_0[i][6:])
  # argmax_array.append(sorted_array[31])
  # argmax_array_2ndplace.append(sorted_array[30])
  # sorted_array = np.argsort(pred_array_6[i][6:])
  # argmax_array.append(sorted_array[31])
  # argmax_array_2ndplace.append(sorted_array[30])
  sorted_array = np.argsort(pred_array_12[i][6:])
  argmax_array.append(sorted_array[31])
  argmax_array_2ndplace.append(sorted_array[30])
#   sorted_array = np.argsort(pred_array_18[i][6:])
#   argmax_array.append(sorted_array[31])
#   argmax_array_2ndplace.append(sorted_array[30])
#   sorted_array = np.argsort(pred_array_18[i][6:])
#   argmax_array.append(sorted_array[31])
#   argmax_array_2ndplace.append(sorted_array[30])
#   sorted_array = np.argsort(pred_array_24[i][6:])
#   argmax_array.append(sorted_array[31])
#   argmax_array_2ndplace.append(sorted_array[30])
# # print(argmax_array)
# print(argmax_array_2ndplace)
# print(np.argmax(argmax_array))

print(len(sorted_array))
# print(len)

for i in range(0,32):
  if i not in argmax_array and i not in argmax_array_2ndplace:
    print(i)

print(sorted(processor.tokenizer.get_vocab())[11])

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(argmax_array, argmax_array_2ndplace)
disp = ConfusionMatrixDisplay(confusion_matrix=cm) #(a,e) = 320 (s,t) = 240

# disp.plot()

# plt.show()

cm_test = confusion_matrix([1,1,4,5,4,5,3], [2,2,5,2,1,2,7])
print(cm_test)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_test) #(a,e) = 320 (s,t) = 240

disp.plot()

plt.show()

print(len(cm))
np.set_printoptions(threshold=np.inf)


# cm_test = confusion_matrix([1,1], [2,2])
print(cm)

#Entropy calculaten per laag
# print(pred_array_18[0]) #10916x38

from scipy.stats import entropy

print(len(pred_array_18))
print(len(pred_array_18[0]))

h_18 = entropy(pred_array_18, axis=1)



print(h_18)
print(len(h_18))
#average pakken? nee! zie notes

h_0 = entropy(pred_array_0, axis=1)
h_6 = entropy(pred_array_6, axis=1)
h_12 = entropy(pred_array_12, axis=1)
h_18 = entropy(pred_array_18, axis=1)
h_24 = entropy(pred_array_24, axis=1)

print(len(h_24))
print(h_24[402])

#entropy = disorder, uncertainty
entropycount_0 = 0
entropycount_1 = 0
for i in range (0, len(h_0)):
  if h_12[i] > h_18[i]:
    entropycount_0 += 1
  else:
    entropycount_1 += 1
print(entropycount_0,entropycount_1, entropycount_0+entropycount_1)

print(h_18[3000:3100])
print(h_24[3000:3100])