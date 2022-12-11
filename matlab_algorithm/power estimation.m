close all; clear all;

% read .mp3 file
[data, fs] = audioread('test.mp3');

% normalize data
data = data / abs(max(data));

% do framing
f_d = 0.025;
frames = framing (data, fs, f_d);