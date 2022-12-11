close all; clear all;

% read sound
[data, fs] = audioread('test.mp3');
% normalize data
data = data / abs(max(data));

% do framing
f_d = 0.025;
frames = framing (data, fs, f_d);

% e.g. of ZCR
% x = [1 2 -3 4 5 -6 2 -6 2];
x = frames(110,:);

%% Method 1
ZCR1 = 0;
for i = 1:length(x) - 1
    
    if ((x(i) < 0) && (x(i + 1) > 0 ))
        ZCR1 = ZCR1 + 1;
        
    elseif ((x(i) > 0) && (x(i + 1) < 0))
        ZCR1 = ZCR1 + 1;
    end
end

%% Method 2
%ZCR2 = sum(abs(diff(x > 0)));

%% Method 3
%ZCR3 = sum(x(1 : end - 1) .* x(2:end) <= 0);

%% finding ZCR of all frames
[r, c] = size(frames);

for i = 1 : r
    
    x = frames(i, :);
    %% Method 1
    ZCRf1(i) = 0;
    for k = 1:length(x) - 1
        
        if ((x(k) < 0) && (x(k + 1) > 0 ))
            ZCRf1(i) = ZCRf1(i) + 1;
            
        elseif ((x(k) > 0) && (x(k + 1) < 0))
            ZCRf1(i) = ZCRf1(i) + 1;
        end
    end
    %% Method 2
    %ZCRf2(i) = sum(abs(diff(x > 0)));
    
    %% Method 3
    %ZCRf3(i) = sum(x(1 : end - 1) .* x(2:end) <= 0);
    
    
end

% calculating rate
ZCRr1 = ZCRf1/length(x);
ZCRr1 = ZCRr1/max(ZCRr1);
f_size = round(f_d * fs);
zcr_wave = 0;
for j = 1 : length(ZCRr1)
    l = length(zcr_wave);
    zcr_wave(l : l + f_size) = ZCRr1(j);
end
% plot the ZCR with Signal
t = [0 : 1/fs : length(data)/fs]; % time in sec
t = t(1:end - 1);
t1 = [0 : 1/fs : length(zcr_wave)/fs];
t1 = t1(1:end - 1);

plot(t,data'); hold on;
plot(t1,zcr_wave,'r','LineWidth',2);

% Silence Removal
id = find(ZCRr1 <= 0.2);
fr_ws = frames(id,:); % frames without silence

% reconstruct signal
data_r = reshape(fr_ws',1,[]);
figure;
plot(data);hold on;
plot(data_r,'g'); title('speech without silence');