% This function is used to split entire speech in frames of specific time
% duration in msec. (in this we don't do frame overlapping)
% 
% 

function [frames] = framing(x,fs,f_d)

% x:input speech signal
% fs: Sampling Frequency
% f_d: Frame duration (in sec)
% frames: returns Matrix in which each row represents a frame of specific
%         duration

f_size = round(f_d * fs);  % frame size

% do zero padding in signal in case total samples don't fit in integer no.
% of frames
l_s = length(x);    % speech length
n_f = floor(l_s/f_size); % no. of frames
% don't do zero padding
% x((l_s + 1) : (n_f + 1) * f_size) = 0; % zero padding

% creating frmes
temp = 0;
for i = 1 : n_f
    frames(i,:) = x(temp + 1 : temp + f_size);
    temp = temp + f_size;
end

end